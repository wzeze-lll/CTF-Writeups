# axb_2019_fmt32

32 位格式化字符串题（文件名表明是 2019 安洵杯），未 strip，无附带 libc/loader。

| 项 | 值 |
| --- | --- |
| 架构 | i386，interpreter `/lib/ld-linux.so.2` |
| Build ID | `fac8f324df591d1193df64140ddb88fb9dab7984` |
| sha256 | `3499cb7948d425961b14eb94b6f4f611559152ed6db36e90ebdec0f213ee76d1` |
| 编译环境 | `GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.11)` |
| 运行库 | [`libc/2.23/i386/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/2.23/i386/ORIGINAL_NOTES.md)（2.23-0ubuntu11.3，本地兼容候选） |

这是格式化字符串题，单独归在 `格式化字符串/`。二进制未在 VM 运行，只做了静态归档。

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/i386/ld-linux.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/i386/lib" \
  "$PWN_ROOT/格式化字符串/2.23/i386/axb_2019_fmt32/axb_2019_fmt32"

# 或用统一入口
bash tools/pwn-env.sh run 2.23 i386 格式化字符串/2.23/i386/axb_2019_fmt32/axb_2019_fmt32
```
