# WDB 2018 第二阶段 · easyfmt（格式化字符串）

## 来源

| 项 | 值 |
| --- | --- |
| 出处 | 2018 WDB 第二阶段（`2018WDB/第二场/Pwn/easyFMT.zip`） |
| 参考仓库 | <https://github.com/hacker-mao/ctf_repo/tree/master/2018WDB/第二场/Pwn> |
| 二进制 | `easyfmt`，**未 strip**，i386，Build ID `f86851c3576d0aabf0b0b2310d835d0f6e660eb8` |
| sha256 | `2b1d4c17094269d4f0e60a3e2aadd32c625b324861826de22a06bad614697147` |
| 编译环境 | `GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10)`，interpreter `/lib/ld-linux.so.2` |
| libc | 附件未附带；使用版本目录 [`libc/2.23/i386/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/2.23/i386) 的 2.23 运行库（i386/ubuntu:16.04，2.23-0ubuntu11.3） |

题目只有 7596 字节，仓库里的 `easyFMT.zip` 也只有约 2.9 KB，包里不带 libc/loader。二进制按 Ubuntu 16.04 编译、只要求 `GLIBC_2.0`/`GLIBC_2.2.5` 老符号，所以归档到 2.23 i386；这是**本地兼容**，不证明远程就是 2.23-0ubuntu11.3 这个补丁版。

## 保护

| 保护 | 结论 | 依据 |
| --- | --- | --- |
| PIE | 关 | `e_type = ET_EXEC`，地址固定在 `0x8048xxx` |
| Canary | 开 | `main` 序言读写 `%gs:0x14`，存在 `__stack_chk_fail` |
| NX | 开 | `GNU_STACK` 为 `rw-` |
| RELRO | Partial | 有 `GNU_RELRO`，没有 `BIND_NOW` → **GOT 可写** |

## main 逻辑（反汇编要点）

```c
char buf[0x64];                 // ebp-0x70
setbuf(stdin/ stdout/ stderr, NULL);
puts("Do you know repeater?");
while (1) {
    read(0, buf, 0x64);         // 0x80485b0
    printf(buf);                // 0x80485ca  ← 直接把输入当格式串
    putchar('\n');
}
```

栈上布局（`ebp-0x70` 起）：

```text
低地址
ebp-0x70  buf[0x64]        ← read 写入 0x64 字节
ebp-0x0c  canary           ← read 正好停在它前面，不越界
ebp-0x08  saved ebx
ebp-0x04  saved ebp
ebp+0x00  saved eip
高地址
```

`read` 长度 0x64 与 buf 大小相等，没有栈溢出；漏洞是 **`printf(buf)` 的格式化字符串**，而且放在死循环里，可以反复给 payload（"repeater"）。

## 利用要点（静态推断）

- GOT 可写 + 非 PIE，最直接的是把 `printf@got` 改成 `system`，再发 `/bin/sh`：

| 符号 | 地址 |
| --- | --- |
| `printf@plt` | `0x8048400` |
| `printf@got` | `0x804a014` |
| `read@got` | `0x804a010` |
| `puts@plt` | `0x8048410` |

- 本机 2.23 i386 运行库的符号偏移（`lib/libc.so.6`，**换补丁版必须重查**）：

| 符号 | 偏移 |
| --- | --- |
| `system` | `0x3adb0` |
| `printf` | `0x49680` |
| `puts` | `0x5fcb0` |
| `__libc_start_main` | `0x18550` |
| `__free_hook` | `0x1b48b0` |
| `__malloc_hook` | `0x1b3768` |

- 读栈上哪几个位置是格式串参数，要在 VM 里用 `%p` 试；静态只能确定参数区从 `printf` 的返回地址之上开始。canary 在 `ebp-0xc`，用 `%n` 写 GOT 时注意不要把 payload 写成长到越过 buf。

## 启动（Linux VM）

32 位 ELF 需要内核支持 IA32（x86-64 VM 通常可用）：

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/i386/ld-linux.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/i386/lib" \
  "$PWN_ROOT/格式化字符串/2.23/i386/wdb_2018_2nd_easyfmt/easyfmt"
```

或用统一入口：

```bash
bash tools/pwn-env.sh run 2.23 i386 格式化字符串/2.23/i386/wdb_2018_2nd_easyfmt/easyfmt
bash tools/pwn-env.sh gdb 2.23 i386 格式化字符串/2.23/i386/wdb_2018_2nd_easyfmt/easyfmt
```

## 状态

- 已验证（静态）：架构、Build ID、保护属性、`main` 反汇编、GOT 偏移、运行库符号偏移。
- 未验证：VM 内启动、GDB 调试、格式串参数位置、EXP。macOS 不能执行 Linux ELF。
