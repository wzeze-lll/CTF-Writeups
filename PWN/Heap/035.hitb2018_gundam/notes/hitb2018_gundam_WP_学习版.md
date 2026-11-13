---
tags: [pwn, writeup, heap, uaf, tcache, unsorted-bin, glibc]
created: 2026-09-29
status: 待附件复现
learning_level: L1（公开材料已整理；尚无附件与 GDB 复现证据）
---

# hitb2018_gundam — 一个悬空 `name` 指针如何串起泄露与旧版 tcache（学习版）

> [!important] 本页的边界
> 本页只用于公开 CTF 的本地学习。公开复盘把这题放在 Ubuntu 18 / glibc 2.27 的旧环境中，但你下载附件后仍要用实际 loader、libc、mapping 和 GDB 重新确认。没有附件前，下面的 chunk 数量、泄露偏移和最终目标都只是**待核验的推导模型**，不是可以直接复制的 EXP。

横向辨别三题的漏洞与 allocator 分支差异：`旧版tcache三题对照`。

## 0. 这题到底在练什么

它表面上像是“tcache double free 改 `__free_hook`”，但我认为真正的主线是：

```text
对象还活着时：factory[i] ──> Gundam 结构体 ──> name chunk

destroy(i) 后：结构体仍在，name 指针还在
                          │
                          ├─ destroy 再次把同一地址交给 free：Double Free 候选
                          └─ 后续 build 若复用旧 chunk，而读取又没有覆盖完整用户区：
                             visit 可能打印 allocator 留下的残留数据
```

也就是说，**程序把“结构体是否在用”和“name 指向的内存是否还有效”混成了一件事**。`flag=0` 只限制了部分菜单逻辑，并没有替代 `name = NULL`。

```text
Input / 菜单
  ↓
destroy 释放 name，却留下旧地址
  ↓
大块绕开或填满 tcache 后进入 unsorted bin
  ↓
后续 build 重新拿到该 chunk；短写没有抹掉 fd/bk 残留 → visit 输出 libc 内地址
  ↓
Primitive 2：旧环境下再次释放同一 name → tcache 链被错误复用
  ↓
让一次 build 的写入落到“已验证的目标槽”
  ↓
旧 libc 的可选终点：hook 写入 + 后续 free 触发
```

## 1. 从公开资料还原题目对象

公开反编译资料把对象概括为：一个全局 `factory[9]` 保存结构体指针；结构体有在用标记、`name` 指针和 `type` 字段。`name` 的读取长度约为 100 字节，`visit` 会显示 name；`destroy` 会 `free(name)` 却没有清空该指针。[公开复盘](https://www.cnblogs.com/wudiiv11/p/buuctf-gundam.html)

可以先用这张**概念图**分析，不要把字段偏移当作已验证事实：

```text
factory[i]
   │
   ▼
+-------------------------+
| used / flag              |
| name  ───────────────────┼──> [ 用户输入的 name bytes ]
| type                     |
+-------------------------+

destroy(i):  free(name)；flag 变为未使用
遗漏：        name 没有置 NULL
```

`blow_up` 的角色也容易被看错。它会回收已不用的**结构体**并清掉工厂表项；它不是直接修复 name 的生命周期问题。公开路线中，它常用于腾出对象槽，再 build 出新对象。这样新 `name` 的 `malloc` 才可能取回之前进入 unsorted 的那块内存。

### 拿到附件后的第一轮证据

```bash
file ./gundam
checksec ./gundam
readelf -lW ./gundam
readelf -dW ./gundam
```

再在 IDA/Ghidra 或 GDB 中回答：

1. `name` 的真实请求大小是多少，读取函数是否补 NUL？
2. `destroy` 后 `name`、`factory[i]`、`flag` 分别发生什么？
3. `visit` 检查的是 `flag`、指针，还是两者？
4. `blow_up` 释放的到底是结构体、name，还是两个都释放？

只有这四项明确，才有资格说 UAF / double free 的路线成立。

## 2. 第一阶段：为什么要九个对象、八次释放

公开路线常见“build 9 个、destroy 前 8 个、最后 visit”这个操作。它不是神秘配方，而是在旧 tcache 默认每个 size class 可暂存 7 个节点的条件下，尝试让第 8 个同尺寸 free 不再被当前 tcache 接收，转而出现在 unsorted-bin 路径。[公开复盘](https://www.cnblogs.com/wudiiv11/p/buuctf-gundam.html)

第 9 个对象是 guard：避免待观察的最后一个 name chunk 紧贴 top chunk 后被合并，导致你看到的不是想研究的 unsorted 状态。

```text
申请后（概念）：
[ name0 ][ name1 ] ... [ name7 ][ name8: guard ][ top ]

依次 free name0..name7：
前 7 个：若实际进入 tcache，则填满对应链
第 8 个：才有机会按该环境路径进入 unsorted bin
name8：仍在使用，阻止 name7 向后与 top 合并
```

这里有三个**必须现场核验**的条件：

- `name` 的实际 chunk size 必须落在可观察的那条 tcache size class；
- 当前 tcache 计数上限、glibc 补丁和 tunable 必须与假设相符；
- 被观察 chunk 必须没有被合并或被其他分配立即取走。

### 为什么 unsorted bin 能帮你泄露 libc

free 后，allocator 可能复用 freed chunk 的用户区开头来放链表字段。若 A 真进入 unsorted bin，它的 `fd/bk` 会关联 arena 中的 bin 头；arena 位于 libc 映射内。这里不能直接假设 `visit(A)` 会成功：公开反编译显示 `visit` 有对象状态检查。更合理的模型是重建同尺寸对象；若新的 `name` 恰好复用 A，且本次输入只覆盖了前几个字节，A 中未被抹掉的 `fd/bk` 残留才可能被 `visit` 输出。它仍是**libc 内运行时指针**，不是 libc base。

```text
A 原来是 name 的用户区
free(A) 后（概念）：

A_user ──> [ fd: 指向 arena/bins 附近 ][ bk: ... ][ 原 name 残留 ... ]
                  │
                  └─ 这是 leak，不是 libc base

libc_base = leaked_pointer - verified_offset_in_the_given_libc
```

不要把网上的 `0x3ebca0` 复制进脚本。它只描述某一份 2.27 构建中某个字段的位置；字段来源、发行版 patch 与题给 libc 一变，常数就可能错。

### GDB 观察点

```gdb
# 释放前：记录 A 的用户地址；在目标 free 入口看它是否就是 A
break __libc_free
continue
p/x $rdi
x/4gx $rdi-0x10
continue

# 释放返回后
bins
vis_heap_chunks
x/4gx <A_user>
info proc mappings
```

你要得到的结论不是“看到一个像 0x7f 的数”，而是：

```text
A 进入 unsorted bin
→ A_user 开头的字段指向 libc mapping
→ 新 build 的 name 实际复用了 A_user，且短写保留了这部分字段
→ visit(新对象) 的输出确实包含该字段
→ 用题给 libc 的精确偏移相减，base 与 mapping 对得上
```

## 3. 第二阶段：旧 tcache double free 是怎样把“悬空”放大的

假设小 name chunk 为 S，且附件证明：重复 `destroy` 最终把**同一个 S_user**交给旧 tcache 路径两次，并且目标库没有中止程序。概念上的链会像这样：

```text
第一次 free(S)：head → S → NULL
第二次 free(S)：head → S ─┐
                             └── 回到 S
```

这时连续同尺寸 `build` 会多次把 S 交给程序。第一次重用 S 时，程序写入 name 的前 8 字节可能覆盖 allocator 下一次会读取的 `next` 字段；后续分配才有机会走到你设置的位置。

```text
build #1 得到 S：写入“下一节点的目标值”（需满足版本编码/检查）
build #2 得到 S：消耗重复节点
build #3：若链表状态与目标检查都合法，才可能返回目标附近的可写位置
```

这不是“UAF = arbitrary write”。要逐一记录：

| 要证明的点 | 最小证据 |
|---|---|
| 两次释放的是同一块 | 两次进入 `free` 时 `$rdi` 都等于 S_user |
| 它真的进 tcache | `bins` / 用户区字段与实际版本对应 |
| 第一次重用能覆盖链字段 | 输入长度覆盖 S_user 开头，`x/gx S_user` 写前后改变 |
| 目标值的格式正确 | 目标版本是否 Safe-Linking、目标是否对齐、完整性检查是否通过 |
| malloc 真按预期取链 | 每一次 build 都记录返回 user 指针 |

> [!warning] 版本不是装饰
> tcache 在 glibc 2.26 引入；重复释放检查、Safe-Linking 和旧 hooks 都随版本/发行版补丁变化。即使同叫“2.27”，也应以题给 `libc.so.6` 与运行时 GDB 观察为准。先读 `glibc版本差异` 与 `Tcache_Attack`。

## 4. 终点只是旧版可选项：为什么是 `free("/bin/sh")`

在题给的旧 libc 仍存在 hook 分支，且你已证明一次 build 的写入真实落在 hook 槽时，公开路线会选：

```text
[ __free_hook 的内存槽 ] = system 的运行时地址

name_chunk ───> "/bin/sh\x00"
destroy(name_chunk)
        ↓
旧 __libc_free 的 hook 分支
        ↓
近似 system(name_chunk)
```

注意两件事：

1. `__free_hook` 是**写入终点**，不是 UAF 自动提供的能力；
2. `system` 接收的是 `free(p)` 原本的第一个参数 `p`，所以最后被释放的 name 必须指向有效命令字符串。

验证时不靠猜：

```gdb
info sharedlibrary
p/x &__free_hook
x/gx &__free_hook             # 写前与写后都记一次
disassemble __libc_free        # 先确认实际还有 hook 分支
break __libc_free
continue
bt
p/x $rdi
x/s $rdi
```

更多解释见 `__free_hook劫持`。若当前 libc 没有这条分支，正确结论是“这条旧终点失效”；不是继续替换某个网上偏移。

## 5. 题目专用的调试路线

### Step A：先证明 dangling pointer，不把它误叫成直接 show UAF

1. build 一个 `name = b"MARK-A"`；
2. destroy 它；
3. 在第二次 `destroy` 的 `free` 入口停下，确认 `$rdi` 仍等于第一次的 name_user；
4. 比较第一次 free 前后 `x/32bx name_user`，记录 allocator 改写过的区域；
5. 单独确认 `visit` 的 `flag` 检查：它是否允许直接访问已 destroy 的对象？

### Step B：只证明第八次的去向

1. 申请大小相同的 9 个 name；
2. 每次 destroy 后记录 `$rdi`、chunk header 和 `bins`；
3. 不依赖输出文本，先由 GDB 判断第八次是否真的到 unsorted；
4. `blow_up` 后重建对象，逐个记录新 name 是否复用 A；
5. 仅在“复用 + 写入范围 + visit 输出”三者对上时，才把输出当作 leak。

### Step C：只证明重复节点，不直接写 hook

1. 对一个小 name 执行两次真实可达的 destroy；
2. 在第二次 free 前后查看该 chunk 的用户区和 tcache；
3. 连续 build 同尺寸 marker，记录每次返回地址；
4. 只有“同一地址按预期复用”已成立，才讨论下一个目标。

## 6. 学习脚本骨架：故意留下需验证的事实

```python
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

elf = ELF('./gundam', checksec=False)
libc = ELF('./libc.so.6', checksec=False)  # 只能是附件核验过的库
io = process('./gundam')

def build(name: bytes, kind=0):
    # TODO：用附件真实菜单提示同步；确认 read 是否吃换行 / NUL
    pass

def visit():
    # TODO：返回原始 bytes；不要先 decode
    pass

def destroy(index: int):
    # TODO：确认同一个 index 第二次是否仍会调用 free(name)
    pass

def blow_up():
    # TODO：确认释放/清理的是哪一层对象
    pass

# Stage 1：9 个同尺寸 name；逐次验证 free 的 bin 去向；重建后确认哪个新 name 复用 A，再解析残留 leak。
# leak = ...
# libc.address = leak - VERIFIED_UNSORTED_FIELD_OFFSET
# assert libc.address & 0xfff == 0

# Stage 2：只在“同一 S_user 二次 free 未被拦截 + bins 确认”之后，验证重复分配。
# 不写死 target；先让下一次 build 返回一个自己可验证的 heap marker。

# Stage 3：仅附件证明旧 hook 分支仍在时，才填写 hook 与 system，并在 GDB 对照写前后内容。
```

## 7. 我的理解：这题是“两个层面的释放”

一开始我会把它理解成“`destroy` 后名字还能被 visit 读出来”。但公开反编译里的 `flag` 检查提醒我：这说法太快了。更准确的说法是：

```text
业务层：这个 Gundam 已经不再使用（flag=0）
内存层：name 指向的 chunk 已交回 allocator
指针层：结构体里仍保留旧 name 地址
```

漏洞恰好发生在三层不同步：业务层把它当旧对象，allocator 把它当空闲链节点，而 `destroy` 又继续相信旧地址。

这里还有一个很容易漏掉的中间层：**leak 不一定是直接读 freed name；也可能是新 name 复用 freed chunk 后，只覆盖了一小段输入，剩下的 allocator 字段被打印出来。** 因而 “UAF” 负责留下可重复释放的旧地址，“短写 + 重用”负责让残留数据可见。两件事都要在附件里各自证明。

这也解释了为什么此题分成“先大后小”更自然：

```text
大 name：让 allocator 留下可定位 libc 的痕迹，解决“地址在哪里”
小 name：让 allocator 的复用链可被观察，解决“写入怎样到目标”
最终 free：提供已有间接调用点的触发时机
```

它们不是三段互不相关的套路，而是对同一个悬空指针在不同 allocator 状态下的三次利用。

## 8. 练习、反思与资料

### Example A：脱稿解释

请画出 `factory[i] → gundam → name` 的三层关系，并解释 `flag=0` 为什么不能代替 `name=NULL`。

### Test B：附件到手后的 48 小时迁移题

不看公开 EXP，只完成：

1. 用 GDB 证明第二次 `destroy` 是否仍将第一次的 name_user 传给 free；
2. 写出第八次 free 是否进入 unsorted 的证据；
3. 证明新 name 是否复用 A，以及输出为什么保留了 A 的哪个字段；
4. 若 double free 被 abort，记录具体报错、目标 libc 和第二次 `$rdi`，而不是继续换次数。

### 公开资料（用于对照，不替代本地证据）

- [wudiiv11：BUUCTF gundam](https://www.cnblogs.com/wudiiv11/p/buuctf-gundam.html)：对象逻辑、旧环境复盘、8 次填 tcache / 1 次观察 unsorted 的公开路线。
- [CoLin：gundam 复盘](https://hornos3.github.io/2021/03/19/gundam/)：可用来交叉阅读菜单生命周期；具体地址仍须以附件为准。
- `UAF详解` · `Tcache_Attack` · `Unsorted_Bin_Attack` · `__free_hook劫持`：把题目现象拆回通用原理。

## 最后一行

> 这题不是“连续 free 两次就赢”。先证明旧 `name` 指针还在，再证明对应 chunk 去了哪里，最后才谈这条链能否被改写。

## 相关代码与实战模板

- 本页模板入口：`malloc/free 生命周期实验` · `glibc LIFO 地址复用观察（需 GDB 确认 tcache）` · `pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。
