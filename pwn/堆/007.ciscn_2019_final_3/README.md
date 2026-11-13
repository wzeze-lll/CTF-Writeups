# 知识点

堆

# 题目分析

分类：pwn / 堆。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ciscn_final_3](ciscn_final_3)

## 已有分析

- [ciscn_2019_final_3_WP_学习版.md](notes/ciscn_2019_final_3_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)


### ciscn_2019_final_3 — 先改变“free 会走哪条路”，再谈泄露（学习版）

> [!important] 本页的边界
> 公开资料常把本题归为 glibc 2.27 的 tcache 题，并给出“重复释放 → 改 tcache 状态 → 让一个 chunk 去 unsorted → 泄露 libc”的路线。但不同发行版微版本的 tcache 检查可能不同。没有原始 ELF、配套 libc/ld 和一次 GDB 记录前，不应把公开脚本中的 heap 偏移、字段偏移或 request size 直接搬到本地。

横向辨别三题的漏洞与 allocator 分支差异：`旧版tcache三题对照`。

#### 0. 这题练什么：不是“会 double free”，而是会改 allocator 的选择

本题最值得学的地方，不是最终写到哪个 hook，而是这一句：

> **同一次 `free(A)` 不一定永远进 tcache；分配器会按当前 size class 的状态、版本检查和相邻 chunk 状态选择路径。**

公开复盘描述的目标链是：通过 UAF / 旧 tcache 重复释放，影响一条小块链和它相关的状态；使特定大小的后续 free 不再优先留在 tcache，从而有一个 chunk 能进入 unsorted bin 并产生 libc 线索。[公开复盘](https://www.cnblogs.com/Dav-ove3/p/17244070.html)

```text
程序保存了可再次操作的 chunk 指针
        ↓
同一 chunk 被释放或重用后，程序仍可写 / 再 free
        ↓
先获得“影响 tcache 状态”的候选能力
        ↓
让某个大于/不同于当前缓存状态的 free 走到 unsorted 路径
        ↓
从 freed 用户区 / 程序给出的地址信息定位 libc
        ↓
在题给旧 libc 中，再选择可验证的间接控制终点
```

因此它比 `gundam` 多了一层思考：`gundam` 主要靠“第八次相同 size 的 free”把 tcache 填满；`final_3` 的公开路线则强调**先改变或伪造 allocator 看到的状态**。这不是背一条更长的 payload，而是理解 allocator 的分支条件。

#### 1. 先把题目接口画成“地址账本”

公开代码片段显示：`Allocate` 接收 index 和 size，写入用户数据后会打印一个 `gift` 地址；`Free(index)` 按 index 释放。也就是说，它可能同时给了：

```text
分配能力：指定请求大小 + 写入 bytes
释放能力：按 index free
地址线索：程序输出某个 heap / chunk 相关地址
```

拿到附件后，不要先写 exploit，先建一张表：

| 操作序号 | index | 请求 size | 返回 / gift | user 指针 | free 后状态 | 备注 |
|---|---:|---:|---|---|---|---|
| 0 |  |  |  |  |  |  |
| 1 |  |  |  |  |  |  |

你要从反编译与运行中确认四个问题：

1. `gift` 是 user pointer、chunk header、结构体地址，还是另一个全局数组地址？
2. `Free` 后 index 是否清零？第二次 `Free(index)` 实际传给 `free` 的值是否相同？
3. 写入长度由 `size`、固定长度还是 `read` 的返回值控制？
4. 是否存在一次“只输出地址而不直接 show”的机会限制？

如果其中任何一项与公开复盘不同，后面的链要跟着改，而不是硬调常数。

#### 2. 漏洞的最小模型：UAF / double free 候选，不是结论

抽象后的危险代码像这样：

```c
void remove(size_t i) {
    free(ptrs[i]);
    // 缺少：ptrs[i] = NULL;
}

void add(size_t i, size_t n) {
    ptrs[i] = malloc(n);
    read(0, ptrs[i], n);
    printf("gift: %p\n", ptrs[i]);
}
```

如果 `remove(i)` 后 `ptrs[i]` 仍保留，至少有两个待验证方向：

```text
再次 remove(i) → 可能把同一 user pointer 送入 free 两次
新的 malloc 复用旧地址 → 程序仍可用旧 index 操作新/空闲对象
```

但“可能”必须由 GDB 变成事实：

```gdb
break __libc_free
continue
p/x $rdi                 # 第一次 free 的 user pointer
continue
p/x $rdi                 # 第二次是否仍是同一个值
bt                       # 哪个菜单路径触发
```

若第二次已经 abort，得到的不是失败，而是很有价值的结论：**当前题给库的重复释放检查生效，公开旧路线不能原样用。**

#### 3. 关键难点：tcache count 不是“一个神秘数字”

把 tcache 的某条 size class 想成一个小抽屉：

```text
tcache[size_class]
head  ──> 空闲 chunk 链
count ──> 抽屉里当前有几个节点
```

在很多旧环境中，如果该抽屉未满，`free(A)` 会优先把 A 放入 tcache；如果它已满，分配器才可能走下一条路径。公开资料中的思路，是设法让分配器认为某个 size class 已满，再释放一个相应大小的 A，以便观察 unsorted-bin 路径。

```text
正常状态：count = 少量
free(A)  → tcache[size] 接收 A

待验证的被影响状态：count = 达到上限
free(A)  → tcache 不能接收
           ↓
        继续走 allocator 后续分支
           ↓
        在特定大小/邻居条件下，可能成为 unsorted-bin 节点
```

这也是为什么本题要区分两种控制：

| 你影响的东西 | 它解决什么问题 |
|---|---|
| tcache 链的 next | 影响下一次同尺寸 malloc 从哪里取节点 |
| tcache 的“是否已满”状态 | 影响下一次 free 是否还会被 tcache 截走 |

第二行通常更难：你必须先有一个能写到相关 allocator 状态的路径，且写入格式、偏移与版本完全正确。它不是“往任意地址写 8 字节”的同义词。

> [!warning] 不把公开字段偏移写成模板
> 一份公开 EXP 会用程序打印的 heap 地址减常数去定位某个 tcache 结构，再构造 bytes 改计数。那是它观察到的布局。你自己的附件必须重新证明：gift 是什么、减的常数指向什么、写入确实到达 count、以及下一次 free 的 bin 去向真的改变。

#### 4. 为什么要让 chunk 去 unsorted：目标是 libc 坐标，不是“换一个 bin”

tcache 的单链字段在很多环境中是 heap 内信息或编码值；它未必直接给 libc base。若某个 chunk 真进入 unsorted bin，链表字段会指向 arena/bins 附近，才可能形成 libc 相关泄露。

```text
先：A 在 tcache
    A_user 的开头更像 tcache next / key

后：A 在 unsorted
    A_user 的开头可能关联 main_arena / bins
                         │
                         └─ 从 libc mapping 内地址反推 base
```

严谨的计算式仍是：

```text
libc_base = leak - offset_of_the_exact_leaked_field_in_given_libc
```

而不是：

```text
libc_base = leak - 某篇 WP 的固定数
```

##### 必做的交叉验证

1. `bins` 证明 A 在 unsorted；
2. `x/4gx A_user` 确认你拿的是 A 的新 allocator 字段；
3. `info proc mappings` 显示该值落入 libc mapping；
4. 计算出的 `libc_base` 页对齐；
5. 再用另一个 libc 符号或 mapping 起点验证一次。

任何一步不对，就停在这一阶段排错，不要进入“写 hook”。

#### 5. 后半段：从受控分配到旧 hook，只是一个历史终点

公开路线在得到 libc base 后，又回到小块重复释放与 tcache 链控制：让后续分配返回 `__free_hook` 附近的可写位置，再写入 `system`；最后释放一个内容为 `"/bin/sh\0"` 的 chunk。

```text
已知 libc base
  ↓
可计算 hook_addr 与 system_addr
  ↓
已证明的小块链控制
  ↓
某次 malloc 返回的 user 指针真实落在目标槽
  ↓
edit / add 写入 system_addr
  ↓
后续 free(p) 的 p 指向 "/bin/sh\0"
```

只在以下都成立时，这才近似为 `system("/bin/sh")`：

- 题给 libc 的 `__libc_free` 仍有 hook 读取 / 间接调用分支；
- 你写到的是准确 hook 槽，而不是“附近地址”；
- `system` 是本次运行的真实地址；
- 最后 `free` 的 `$rdi` 确实指向带 NUL 结尾的命令。

请用 `__free_hook劫持` 的观察链确认；不要把 `glibc 2.34+` 的兼容符号误当可触发的旧 hook。

#### 6. 分阶段 GDB 计划

##### A. 地址账本与 UAF

```gdb
break __libc_free
run
### 每次 Free(index) 都记录：index、$rdi、该地址的 header、调用栈
p/x $rdi
x/4gx $rdi-0x10
bt
continue
```

##### B. tcache 的实际状态

```gdb
bins
vis_heap_chunks
x/4gx <A_user>
```

每次操作后只写一句日志，例如：

```text
free(0): A_user=...；0x60 size class 的 tcache count 从 ? 到 ?；A 的 user 区前 16 字节为 ...
```

##### C. 进入 unsorted 的那一次

```gdb
### 释放前后都观察，别只在“预计成功”后看
bins
x/4gx <large_A_user>
info proc mappings
```

##### D. 最终触发（旧环境才做）

```gdb
p/x &__free_hook
x/gx &__free_hook
disassemble __libc_free
break __libc_free
continue
p/x $rdi
x/s $rdi
```

#### 7. 学习脚本骨架：记录事实，不硬编码公开布局

```python
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

elf = ELF('./ciscn_2019_final_3', checksec=False)
libc = ELF('./libc.so.6', checksec=False)  # 附件收据确认后才使用
io = process('./ciscn_2019_final_3')

book = []

def allocate(index: int, size: int, data: bytes = b''):
    # TODO：按真实协议同步；保留 gift 原始文本与解析出的地址
    # book.append({'index': index, 'request': size, 'gift': gift, 'data': data})
    pass

def free_index(index: int):
    # TODO：记录本次之前 ptrs[index] 的含义；GDB 中核对 $rdi
    pass

### Phase 1：只用 marker 验证 gift / user pointer / index 生命周期。
### Phase 2：验证重复 free 在目标 libc 下的真实反应。
### Phase 3：若确有受控 tcache 状态，逐步证明哪一次 free 改走 unsorted。
### Phase 4：从实际 A_user 字段解析 leak，再计算并交叉验证 libc base。
### Phase 5：只有旧 hook 分支已被反汇编证明时，才选择其作为终点。
```

#### 8. 我的理解：这题在训练“看分支”，不是“背链条”

`final_3` 最容易让人只记住一串词：

```text
double free → 改 count → unsorted leak → hook → shell
```

但这串词太快，省略了真正重要的问题：**每一条 allocator 分支为什么会被选中？**

我现在会把它翻译为：

```text
我先能否影响空闲 chunk / allocator 的某个状态？
        ↓
这个状态被哪一条 free 分支读取？
        ↓
它会让 A 去 tcache、fastbin、unsorted，还是直接 abort？
        ↓
如果 A 真在 unsorted，A_user 里哪个字段给我 libc 坐标？
        ↓
拿到基址后，我的“写在哪里”与“怎样触发”是否都是实际存在的？
```

所以 `count` 的意义不是一个要背的数字。它是“分配器下一次作出路线选择时看的状态”。控制它的难点，也不在数学，而在于**你有没有先证明自己的写能到那里、且当前 libc 用的正是那个布局**。

#### 9. 验收与公开资料

##### Example A：可完整复述

请用自己的图说明：

```text
tcache 的 next 控制“下一次 malloc 取谁”
tcache 是否满控制“这一次 free 先放哪”
```

并解释为什么“让 A 去 unsorted”本质上是为了拿 libc 坐标。

##### Test B：附件到手后的迁移验证

不看任何公开 EXP：

1. 填好地址账本；
2. 证实或否定同 index 两次 free 的可达性；
3. 用 `bins` 写出让 A 进 unsorted 的真实前置条件；
4. 将一个 observed leak 映射到 libc mapping，并写出 offset 的来源；
5. 若任一步失败，记录“现象 → 分支条件 → 新假设”，而不是继续尝试固定偏移。

##### 公开资料（作路线对照）

- [Dav-ove3：ciscn_2019_final_3](https://www.cnblogs.com/Dav-ove3/p/17244070.html)：公开链条中“旧 tcache 状态 → unsorted leak → hook”的思路来源。
- [Hornos3：BUUCTF 堆题复盘](https://hornos3.github.io/2023/03/04/buuctf-pwn-write-ups-11/)：用于理解环境微版本会改变 tcache 行为这一风险；以附件为准。
- `Tcache_Attack` · `Unsorted_Bin_Attack` · `glibc版本差异` · `__free_hook劫持`：将题目路线拆成版本化的、可观察的原理。

#### 最后一行

> 本题最可迁移的收获不是“能把 count 改成某个数字”，而是：**每次 free 前先问，allocator 接下来要读哪个状态、因此它会走哪一条路。**

#### 相关代码与实战模板

- 本页模板入口：`malloc/free 生命周期实验` · `glibc LIFO 地址复用观察（需 GDB 确认 tcache）` · `pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。


# EXP

当前归档中没有已识别的 EXP / 求解脚本。
