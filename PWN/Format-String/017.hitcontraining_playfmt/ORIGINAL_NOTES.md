# hitcontraining_playfmt

32 位格式化字符串题（HITCON Training 的 playfmt），未 strip，无附带 libc/loader。

| 项 | 值 |
| --- | --- |
| 架构 | i386，interpreter `/lib/ld-linux.so.2` |
| Build ID | `38c67cd31046e505ee0b71aeb170232225f3e11b` |
| sha256 | `e3546c7a45479b44a15ecbd4fe98dfa4d63bacf49b267bf484331f78b75fc285` |
| 编译环境 | `GCC: (Debian 6.4.0-2) 6.4.0 20170724` |
| 运行库 | [`libc/2.23/i386/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/2.23/i386/ORIGINAL_NOTES.md)（本地兼容候选） |

这是格式化字符串题，单独归在 `格式化字符串/`。

版本待核：Debian GCC 6.4.0 对应 Debian 9，glibc 可能是 2.24 而不是 2.23；二进制只要求 `GLIBC_2.0` 老符号，先用 2.23 i386 运行库做兼容候选，找到原始环境后再定版本。二进制未在 VM 运行，只做了静态归档。

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/i386/ld-linux.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/i386/lib" \
  "$PWN_ROOT/格式化字符串/2.23/i386/hitcontraining_playfmt/hitcontraining_playfmt"

# 或用统一入口
bash tools/pwn-env.sh run 2.23 i386 格式化字符串/2.23/i386/hitcontraining_playfmt/hitcontraining_playfmt
```
