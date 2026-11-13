# seccomp_orw（未命名附件 · 栈溢出 + 沙箱 ORW）

原始目录是下载解压后的 `attachment(4)`，没有题名和说明。下面的画像是静态分析得到的，**尚未在 Linux VM 里运行或调试**。

## 环境

| 项 | 值 |
| --- | --- |
| 架构 | x86-64，动态链接，未 strip |
| 题目二进制 Build ID | `7952de45660c8079a097d8b37c6e89df74677e9d` |
| libc | Ubuntu GLIBC **2.35-0ubuntu3.15**，Build ID `6a6cb5a80fd5e5bb5bf3aeaa111add98e88843a5` |
| loader | Build ID `e6d3f5d4f2a24a5464ab59ae321b9474d70410f8` |
| 额外依赖 | `libseccomp.so.2`（题目自己调用 seccomp） |

这份 libc 是 2.35 的**较新补丁版**，和题库共享的 `libc/2.35/amd64/`（2.35-0ubuntu3.1）不是同一个文件，偏移不要混用。运行库因此和题目放在一起，位于 `env/`。

## 静态画像

```text
main:
  sandbox()                          ← 先装 seccomp 过滤器
  write(1, "Give me your name: ", 19)
  vuln()

vuln:
  char buf[0x20];                    ← rbp-0x20
  read(0, buf, 0x30);                ← 多读 0x10 字节
  write(1, "Goodbye!", 8)
  return
```

栈布局（读到 0x30 字节时）：

```text
低地址
+0x00  buf[0x20]                      ← read 的起点
+0x20  saved rbp                      8 字节，可覆盖
+0x28  saved rip                      8 字节，可覆盖
+0x30  （read 到此为止，正好够写完 RIP）
高地址
```

所以回写 offset 是 **0x28（40）**，且 0x30 的长度刚好能写满 8 字节返回地址，不多不少。

保护（静态确认）：

| 保护 | 结论 | 依据 |
| --- | --- | --- |
| Canary | 无 | `vuln` 序言没有读 `fs:0x28` |
| PIE | 无 | 代码与 GOT 地址固定在 `0x401xxx` / `0x403ff0` |
| NX | 开 | `GNU_STACK` 为 `rw-` |
| RELRO | Partial | 有 `GNU_RELRO`，没有 `BIND_NOW` |
| CET/IBT | 有 `endbr64` | `.note.gnu.property` 存在；实际是否强制启用要看运行环境 |

## seccomp 规则

`sandbox()` 的调用序列：

```text
seccomp_init(SCMP_ACT_ALLOW)          // 0x7fff0000：默认放行
seccomp_rule_add(ctx, 0, 59,  0)      // execve   → 0 = SCMP_ACT_KILL_THREAD
seccomp_rule_add(ctx, 0, 322, 0)      // execveat → 同上
seccomp_load(ctx)
```

结论：**只能 ORW**。`open/read/write/sendfile` 等都在，`execve` 与 `execveat` 会被直接杀掉。做题时不要先拼 `system("/bin/sh")` 或 `/bin/sh` shellcode。

## 启动（Linux VM）

```bash
PWN_ROOT="$(pwd)"     # 题型库根目录，在 VM 里
"$PWN_ROOT/栈/ret2syscall/seccomp_orw/env/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/栈/ret2syscall/seccomp_orw/env" \
  "$PWN_ROOT/栈/ret2syscall/seccomp_orw/pwn"
```

或让脚本自动识别题目自带的 `env/`：

```bash
bash tools/pwn-env.sh run 2.35 amd64 栈/ret2syscall/seccomp_orw/pwn
bash tools/pwn-env.sh gdb 2.35 amd64 栈/ret2syscall/seccomp_orw/pwn
```

GDB 里用 `info sharedlibrary` 确认加载的是 `env/libc.so.6`；`seccomp-tools dump` 可复核过滤器，`catch syscall execve` 可验证被拦。

## 状态

- 已验证：ELF 架构、Build ID、符号与反汇编、seccomp 调用参数、`GNU_STACK`/`RELRO` 段。
- 未验证：VM 内启动、GDB 交互、过滤器实际行为、EXP。
- 没有题名和原始题面；如果之后找到出处，把目录和本页标题改成题名即可。
