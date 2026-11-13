# bctf2018_hardcore_fmt

64 位格式化字符串题（BCTF 2018 hardcore_fmt），未 strip，无附带 libc/loader。

| 项 | 值 |
| --- | --- |
| 架构 | x86-64，PIE，interpreter `/lib64/ld-linux-x86-64.so.2` |
| Build ID | `4211d00aacd7ec376353515ea3535062567d8d87` |
| sha256 | `e4820fb440036efae4d0bba8351be284a27085dd899200c3ef10209475c3d400` |
| 编译环境 | `GCC: (Ubuntu 7.3.0-27ubuntu1~18.04)` |
| 运行库 | [`libc/2.27/amd64/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/2.27/amd64/ORIGINAL_NOTES.md)（2.27 运行树，本地兼容候选） |

这是格式化字符串题，单独归在 `格式化字符串/`。Ubuntu 18.04 GCC 7.3 编译，按 2.27 amd64 归档；二进制未在 VM 运行，只做了静态归档。

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.27/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu" \
  "$PWN_ROOT/格式化字符串/2.27/amd64/bctf2018_hardcore_fmt/bctf2018_hardcore_fmt"

# 或用统一入口
bash tools/pwn-env.sh run 2.27 amd64 格式化字符串/2.27/amd64/bctf2018_hardcore_fmt/bctf2018_hardcore_fmt
```
