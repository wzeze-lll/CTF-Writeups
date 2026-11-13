# glibc 2.23 · amd64

## 环境来源与核验

运行库取自 Ubuntu 16.04 官方 `libc6_2.23-0ubuntu10_amd64.deb`（`/lib/x86_64-linux-gnu/`）：

| 文件 | 来源 | ELF | Build ID | sha256 |
| --- | --- | --- | --- | --- |
| `libc-2.23.so` / `libc.so.6` | `libc6` 2.23-0ubuntu10 | 64-bit x86-64 | `b5381a457906d279073822a5ceb24c4bfef94ddb` | `05b841eae6f475817ebb3b99562cd6535cc61b099350a25019cd5d3b3136881d` |
| `ld-2.23.so` / `ld-linux-x86-64.so.2` | 同上 | 64-bit x86-64 | `5d7b6259552275a3c17bd4c3fd05f5a6bf40caa5` | `6d0bfd685a7ad6dfccae1fae70c1f06018a0f756c53de0aabb609456a10f3747` |

版本字符串：`GNU C Library (Ubuntu GLIBC 2.23-0ubuntu10) stable release version 2.23`。

文件都是真实副本（`ld-linux-x86-64.so.2` 是 `ld-2.23.so` 的副本，不是软链接）：本库通过 9p 共享给虚拟机，宿主机侧软链接在 VM 里报 ELOOP，详见 [`tools/README.md`](../../../../../Labs/C-Memory/001.%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0/ORIGINAL_NOTES.md)。

## 借用本目录运行库的题目

| 题目 | 题型 | 归档依据 | 匹配状态 |
| --- | --- | --- | --- |
| [wdb_2018_1st_babyheap](../../../../../PWN/Heap/031.wdb_2018_1st_babyheap/ORIGINAL_NOTES.md) | 堆 / double free、UAF | 二进制由 Ubuntu 16.04 GCC 8.1 编译；附件自带 libc 与本目录 libc 字节相同 | 附件匹配（libc 同包）；VM 未验收 |
| [wustctf2020_babyfmt](../../../../../PWN/Format-String/015.wustctf2020_babyfmt/ORIGINAL_NOTES.md) | 格式化字符串 | 64 位 PIE；Ubuntu 16.04 GCC 5.4 编译；附件不带 libc | 2.23 本地兼容候选；VM 未验收 |

题目目录里的 `env/` 是这份 libc + loader 的自洽副本，`pwn-env.sh` 会自动优先使用它。

## 在 Linux 虚拟机启动

在 VM 中进入共享目录里的题型库根目录，然后运行：

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/amd64" \
  "$PWN_ROOT/libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap"
```

或用统一入口：

```bash
bash tools/pwn-env.sh run 2.23 amd64 libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap
bash tools/pwn-env.sh gdb 2.23 amd64 libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap
```

## 当前验证范围

- 已验证：deb 包来源、libc/loader 的 ELF 架构、Build ID、sha256；附件 libc 与官方包字节一致。
- 未验证：VM 内用该 loader 启动题目、GDB 调试、EXP。macOS 不能执行 Linux ELF。
- 版本标签只说明"附件匹配"，不证明比赛远程镜像就是这一补丁版；复现时优先用题目自带的 `env/`。
