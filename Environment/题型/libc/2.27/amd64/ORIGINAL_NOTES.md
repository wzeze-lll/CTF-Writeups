# glibc 2.27 · amd64

本目录保留原有 Ubuntu glibc 2.27 运行树、`glibc227-fixed/`、独立 libc/loader 别名和 Debian 包。独立 libc 的版本字符串标识为 Ubuntu GLIBC 2.27，架构为 x86-64。顶层标准入口和题目脚本相对链接现在指向 `glibc227-fixed/`，因为这份目录中的 `.so` 别名是有效的符号链接；另一个原始复制树里有些链接被保存成了短文本文件，保留作原始材料但不作为运行路径。

## 借用本目录运行库的题目

题目本体就在本目录下，运行库也在这里。

| 题目 | 题型 | 归档状态 |
| --- | --- | --- |
| [ciscn_2019_es_1](../../../../../PWN/Heap/033.ciscn_2019_es_1/ciscn_2019_es_1) | UAF、unsorted bin、tcache | 题目目录自带同版 libc/ld，脚本指向题目目录；本地启动已显示题目菜单并正常退出，EXP/远程未运行 |
| [hitb2018_gundam](../../../../../PWN/Heap/035.hitb2018_gundam/gundam) | 堆 / tcache | 2.27 教学兼容候选；目标环境版本未由 ELF 符号需求单独证明 |
| [ciscn_2019_final_3](../../../../../PWN/Heap/034.ciscn_2019_final_3/ciscn_final_3) | 堆 / tcache | 2.27 教学兼容候选；目标环境版本需附件或比赛容器证实 |
| [bctf2018_hardcore_fmt](../../../../../PWN/Format-String/020.bctf2018_hardcore_fmt/ORIGINAL_NOTES.md) | 格式化字符串 | Ubuntu 18.04 GCC 7.3 编译；附件不带 libc | 2.27 本地兼容候选；VM 未验收 |

栈题 `babypie`、`rpg`、`ciscn_2019_es_7` 在 [`栈/`](../../../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%88/ORIGINAL_NOTES.md)，因为栈题不按 glibc 分目录；这里保留的 2.27 运行库仍是它们的启动环境。

所有题目附件均按原样保留；目录名称表示本地练习环境，不自动等于远程题目镜像版本。

## ciscn_2019_es_1 的运行库

`es_1` 并入 `libc/2.27/amd64/` 时把自己的 `libc.so.6`、`ld-2.27.so` 一起带过来了，脚本用 `Path(__file__).resolve().parent` 定位这些文件，不依赖本目录的相对链接。它引用远程靶场的脚本没有在整理时运行。

在 Linux/amd64 虚拟机中，从共享目录的题型库根目录运行：

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.27/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu" \
  "$PWN_ROOT/libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1"
```

本次已在 Linux/amd64 环境验证 loader 实际加载本地 2.27 libc，并启动题目显示菜单后正常退出；这不等同于 EXP/远程服务验证。进入 GDB 调试前请复制二进制并只 patch 副本，避免改坏原题附件。
