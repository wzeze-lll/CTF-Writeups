# 知识点

栈

# 题目分析

分类：pwn / 栈。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [wustctf2020_babyfmt](wustctf2020_babyfmt)

## 已有分析

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)

### wustctf2020_babyfmt

64 位格式化字符串题（WUSTCTF 2020 babyfmt），未 strip，无附带 libc/loader。

| 项 | 值 |
| --- | --- |
| 架构 | x86-64，PIE，interpreter `/lib64/ld-linux-x86-64.so.2` |
| Build ID | `0ca95545650df16c964eead2ca63b18e839a4e2a` |
| sha256 | `175586c4c7cb7eb191ef9b23e2b30d91e600c58be552b0f5ca0cd9ebf2eac18a` |
| 编译环境 | `GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.12)` |
| 运行库 | `libc/2.23/amd64/`（见上方完整分析记录）（2.23-0ubuntu10，本地兼容候选） |

这是格式化字符串题，单独归在 `格式化字符串/`。Ubuntu 16.04 GCC 5.4 编译，按 2.23 amd64 归档；二进制未在 VM 运行，只做了静态归档。

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/amd64" \
  "$PWN_ROOT/格式化字符串/2.23/amd64/wustctf2020_babyfmt/wustctf2020_babyfmt"

### 或用统一入口
bash tools/pwn-env.sh run 2.23 amd64 格式化字符串/2.23/amd64/wustctf2020_babyfmt/wustctf2020_babyfmt
```


# EXP

当前归档中没有已识别的 EXP / 求解脚本。
