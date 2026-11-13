# 知识点

Heap

# 题目分析

分类：PWN / Heap。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [VIPhouse](VIPhouse)

## 已有分析

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)

### VIPhouse

64 位堆题（菜单含 login / note / uaf），未 strip 的动态符号里有 `login`、`logout`，无附带 libc/loader。

| 项 | 值 |
| --- | --- |
| 架构 | x86-64，stripped，interpreter `/lib64/ld-linux-x86-64.so.2` |
| Build ID | `25fa66e392d7d25ff2f07210b334aa4be60e77dd` |
| sha256 | `ae7e0a365e1d94b31efb3578c8b5f8bad642f28a55c1e9a38c733846e2bb3763` |
| 编译环境 | `GCC: (Ubuntu 11.3.0-1ubuntu1~22.04.1)` |
| GLIBC 需求 | 需要 `GLIBC_2.34`，对应 Ubuntu 22.04 / glibc 2.35 |
| 运行库 | `libc/2.35/amd64/`（见上方完整分析记录）（2.35-0ubuntu3.1，本地兼容候选） |

菜单是 `1. login in / 2. fmt / 3. uaf / 4. canary / 5. login out`，堆操作和格式化字符串混在一题里；按主要机制归到 `libc/2.35/amd64/` 下的堆题。二进制未在 VM 运行，只做了静态归档。

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.35/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.35/amd64" \
  "$PWN_ROOT/libc/2.35/amd64/VIPhouse/VIPhouse"

### 或用统一入口
bash tools/pwn-env.sh run 2.35 amd64 libc/2.35/amd64/VIPhouse/VIPhouse
```


# EXP

当前归档中没有已识别的 EXP / 求解脚本。
