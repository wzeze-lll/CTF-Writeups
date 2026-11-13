# bbctf_2020_fmt_me

64 位格式化字符串题（BBCTF 2020 fmt_me），未 strip，无附带 libc/loader。

| 项 | 值 |
| --- | --- |
| 架构 | x86-64（非 PIE），interpreter `/lib64/ld-linux-x86-64.so.2` |
| Build ID | `77e8f8b2ff4d908cc1ae73cea3bef74a6d89db1c` |
| sha256 | `bb30b49c8a4b192d439ad5fd799c897a84c2e61a3f628ddd4ebe5ea4bf499e4d` |
| 编译环境 | `GCC: (Arch Linux 9.3.0-1) 9.3.0` |
| 运行库 | [`libc/2.31/amd64/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/2.31/amd64/ORIGINAL_NOTES.md)（2.31-0ubuntu9.17，本地兼容候选） |

这是格式化字符串题，单独归在 `格式化字符串/`。Arch Linux 2020 年的 GCC 9.3 对应 glibc 2.31 左右，按 2.31 amd64 归档；二进制未在 VM 运行，只做了静态归档。

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.31/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.31/amd64/lib" \
  "$PWN_ROOT/格式化字符串/2.31/amd64/bbctf_2020_fmt_me/bbctf_2020_fmt_me"

# 或用统一入口
bash tools/pwn-env.sh run 2.31 amd64 格式化字符串/2.31/amd64/bbctf_2020_fmt_me/bbctf_2020_fmt_me
```
