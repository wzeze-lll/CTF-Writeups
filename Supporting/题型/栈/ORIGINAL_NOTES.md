# 栈题索引

栈题不按 glibc 版本分目录，统一放在 `栈/`；下面按 ret2 体系分组：`ret2text/`、`ret2libc/`、`ret2syscall/`、`ret2shellcode/`，另外保留 `CANARY/` 和 `SROP/` 两个专题。题干没有自带 libc 的，glibc 标签是“本地兼容候选”，不代表远程环境版本；自带 `env/` 的题优先用题目自己的运行库。

## ret2text

栈溢出后直接跳到程序里已有的后门函数（通常自带 `system("/bin/sh")` 或读 flag 的代码）。

| 题目 | 架构 / 环境 | 学习重点 | 状态 |
| --- | --- | --- | --- |
| [guarded_echo](../../../PWN/Stack/022.guarded_echo/guarded_echo) | amd64 / 2.35 兼容候选（Ubuntu 24.04 GCC 13.3 编译） | 程序自带 `win`（`0x12d0`）读 `/flag`；PIE，echo 阶段 `printf(用户输入)` 可泄露地址，随后按可控长度向 0x48 缓冲区栈溢出跳 `win`（所谓 guard 检查恒通过，不是 canary） | ELF 需要 GLIBC_2.34 起始符号 |

## ret2libc

程序没有现成后门，需要泄露出 libc 基址后跳 `system` 或 one-gadget。

| 题目 | 架构 / 环境 | 学习重点 | 状态 |
| --- | --- | --- | --- |
| [stack1](../../../PWN/Stack/027.stack1/stack1) | i386 / glibc 2.23 兼容候选 | 基础栈溢出；无 win 函数，`fgets` 溢出后泄露 libc 再 `system("/bin/sh")` | 本地兼容候选 |
| [rpg](../../../PWN/Stack/026.rpg/rpg) | amd64 / glibc 2.27 兼容候选 | 伪造 rbp 做栈迁移，再 ret2libc | 本地兼容候选 |

## ret2syscall

不用 libc 的 `system`，直接构造寄存器执行 `execve` 或 ORW 一类裸 syscall。

| 题目 | 架构 / 环境 | 学习重点 | 状态 |
| --- | --- | --- | --- |
| [seccomp_orw](../../../PWN/Stack/014.seccomp_orw/ORIGINAL_NOTES.md) | amd64 / 自带 libc 2.35-0ubuntu3.15 | `read` 0x30 进 0x20 栈缓冲；seccomp 只禁 `execve`/`execveat`，必须 ORW | 附件自带 `env/`；仅静态确认 |

## ret2shellcode

程序提供可写可执行内存（如 `mmap` 出 RWX 段），直接把 shellcode 送进去执行。

| 题目 | 架构 / 环境 | 学习重点 | 状态 |
| --- | --- | --- | --- |
| [shellcode](../../../PWN/Stack/013.shellcode/ORIGINAL_NOTES.md) | amd64 / 自带 libc 2.31-0ubuntu9.17 + `libseccomp.so.2` | `mmap` 出 RWX 内存后直接执行输入；seccomp 只放 open/write/mmap，要用裸 syscall，并靠 `mmap(fd)` 读文件 | 附件自带 `env/`；仅静态确认 |

## CANARY

| 题目 | 架构 / 环境 | 学习重点 | 状态 |
| --- | --- | --- | --- |
| [pwn118](../../../PWN/Format-String/024.pwn118/pwn118) | i386 / glibc 2.23 兼容候选 | Canary 与 GOT | 本地兼容候选 |
| [pwn119](../../../PWN/Stack/025.pwn119/pwn119) | i386 / glibc 2.23 兼容候选 | fork 场景下的 Canary / 信息泄露 | 本地兼容候选 |
| [babypie](../../../PWN/Stack/023.babypie/babypie) | amd64 / glibc 2.27 兼容候选 | Canary、PIE 与部分覆盖 | 本地兼容候选 |

## SROP

| 题目 | 架构 / 环境 | 学习重点 | 状态 |
| --- | --- | --- | --- |
| [ciscn_2019_es_7](../../../PWN/Stack/029.ciscn_2019_es_7/ciscn_2019_es_7) | amd64 / glibc 2.27 兼容候选 | 泄露栈地址、构造 SigreturnFrame | 文件已归档；EXP 未在 VM 跑通 |
| [Caged_Signal](../../../PWN/Stack/028.Caged_Signal/chall) | amd64 / glibc 2.35 兼容候选 | SROP、seccomp；进阶题 | 文件已归档；EXP 未在 VM 跑通 |
| [rootersctf_2019_srop](../../../PWN/Stack/030.rootersctf_2019_srop/rootersctf_2019_srop) | amd64 / 静态 ELF | SROP、栈迁移、分阶段输入 | 静态链接，无需动态 libc |

`glibc 2.27/2.35 兼容候选` 只依据架构与最低符号需求，不能证明题目远程环境版本。`seccomp_orw` 的补丁版和共享的 `libc/2.35/amd64/` 不是同一份文件，跑它时用题目自己的 `env/`；`shellcode` 同理，用的是自带的 2.31 + `libseccomp.so.2`，不借 `libc/2.31/amd64/`。

分组口径：有现成后门可跳归 `ret2text`；要泄露 libc 地址再打 `system` 归 `ret2libc`；绕过 NX 用寄存器 + 裸 syscall 归 `ret2syscall`；把 shellcode 写进可执行内存归 `ret2shellcode`。Canary 绕过和 SROP 是独立技术专题，不按 ret2 目标分。
