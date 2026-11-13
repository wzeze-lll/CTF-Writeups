# glibc 2.23 · i386

## 环境来源与核验

运行库从 Docker Hub 的 `i386/ubuntu:16.04` 镜像提取。镜像内报告 GNU libc **2.23-0ubuntu11.3**；提取文件分别是 `lib/libc-2.23.so` 和 `lib/ld-2.23.so`，均为 ELF 32-bit Intel 80386。Build ID：libc `18f761287ed46e213bec29c2e440e73fd72373be`，loader `2bea6d29e841fecacc546b9b5ab802bd061e8b29`。

目录顶层的 `libc.so.6`、`ld-2.23.so`、`ld-linux.so.2` 以及 `lib/libc.so.6` 都是这两个真实文件的**副本**（不是软链接）。本库通过 9p 共享给虚拟机，宿主机侧创建的软链接在虚拟机里会报 `Too many levels of symbolic links`，所以统一用真实文件，详见 [`tools/README.md`](../../../../../Labs/C-Memory/001.%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0/ORIGINAL_NOTES.md)。文件从 `i386/ubuntu:16.04` 运行库提取，但使用时不要求 Docker；在支持 32 位 ELF 的 x86 Linux 虚拟机内即可通过该 loader 启动。

## 借用本目录运行库的题目

堆题 `hacknote` 直接放在本目录的 `UAF/`；其余题目按题型分在 `栈/`、`格式化字符串/` 等目录。

| 题目 | 题型 | 归档依据 | 匹配状态 |
| --- | --- | --- | --- |
| [hacknote](../../../../../PWN/Heap/032.hacknote/ORIGINAL_NOTES.md) | 堆 / UAF | 32 位 ELF；需 `/lib/ld-linux.so.2`，ELF 只要求老版本符号 | 2.23 本地兼容候选；未证明远程环境精确版本 |
| [wdb_2018_2nd_easyfmt](../../../../../PWN/Format-String/019.wdb_2018_2nd_easyfmt/ORIGINAL_NOTES.md) | 格式化字符串 | 32 位 ELF；Ubuntu 16.04 GCC 5.4 编译；附件不带 libc | 2.23 本地兼容候选；VM 未验收 |
| [axb_2019_fmt32](../../../../../PWN/Format-String/016.axb_2019_fmt32/ORIGINAL_NOTES.md) | 格式化字符串 | 32 位 ELF；Ubuntu 16.04 GCC 5.4 编译；附件不带 libc | 2.23 本地兼容候选；VM 未验收 |
| [hitcontraining_playfmt](../../../../../PWN/Format-String/017.hitcontraining_playfmt/ORIGINAL_NOTES.md) | 格式化字符串 | 32 位 ELF；Debian GCC 6.4 编译，版本待核 | 2.23 本地兼容候选；VM 未验收 |
| [suctf_2019_playfmt](../../../../../PWN/Format-String/018.suctf_2019_playfmt/ORIGINAL_NOTES.md) | 格式化字符串 | 32 位 ELF；Ubuntu 16.04 GCC 5.4 编译；附件不带 libc | 2.23 本地兼容候选；VM 未验收 |

栈题 `stack1`、`pwn118`、`pwn119` 在 [`栈/`](../../../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%88/ORIGINAL_NOTES.md)，因为栈题不按 glibc 分目录；它们在本目录做过启动验证，可作为 2.23 兼容候选。

以上文件均保留了原始题目附件、脚本、core 和调试历史。glibc 文件夹是用于练习的运行环境归档，不是比赛远程版本的证明。

## 在 Linux 虚拟机启动

在 VM 中进入共享目录里的题型库根目录，然后运行：

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/i386/ld-linux.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/i386/lib" \
  "$PWN_ROOT/libc/2.23/i386/UAF/hacknote"
```

更换最后一个路径即可尝试启动其他 ELF。若 VM 是 x86-64，需确认内核启用了 IA32 兼容支持；否则改用 32 位 x86 VM。若报缺少非 glibc 共享库，先看 `readelf -d <binary>` 的 `NEEDED` 项，不要覆盖 VM 的系统库。

## 当前验证范围

- 已验证：来源镜像报告的 libc 版本；提取库和 loader 的 ELF 架构、Build ID；指定 loader 在 Linux 下加载本地 `hacknote`，并进入题目菜单后正常退出。
- 未验证：其余题的完整交互流程、GDB/pwndbg 安装及 EXP 成功。
- 需要复现比赛环境时：优先使用题目原始附件或官方容器；最低符号版本只说明兼容性下界。

来源：[Docker Hub i386/ubuntu 镜像标签](https://hub.docker.com/r/i386/ubuntu/tags)。镜像仅用于提取并识别运行库版本；实际做题建议在专用 Linux 虚拟机中使用。
