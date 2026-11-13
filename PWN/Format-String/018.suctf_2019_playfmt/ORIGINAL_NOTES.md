# suctf_2019_playfmt

32 位格式化字符串题（SUCTF 2019 playfmt），未 strip，无附带 libc/loader。

| 项 | 值 |
| --- | --- |
| 架构 | i386，interpreter `/lib/ld-linux.so.2` |
| Build ID | `3ba705f8e341813d856795b1d9129dac61463c1c` |
| sha256 | `d543022adba51c9dae97148280c09192dce6d67d11b3ae43353308e621ec5dda` |
| 编译环境 | `GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10)` |
| 运行库 | [`libc/2.23/i386/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/2.23/i386/ORIGINAL_NOTES.md)（2.23-0ubuntu11.3，本地兼容候选） |

这是格式化字符串题，单独归在 `格式化字符串/`。二进制未在 VM 运行，只做了静态归档。

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/i386/ld-linux.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/i386/lib" \
  "$PWN_ROOT/格式化字符串/2.23/i386/suctf_2019_playfmt/suctf_2019_playfmt"

# 或用统一入口
bash tools/pwn-env.sh run 2.23 i386 格式化字符串/2.23/i386/suctf_2019_playfmt/suctf_2019_playfmt
```
