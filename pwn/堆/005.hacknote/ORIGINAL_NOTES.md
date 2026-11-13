# HITCON Training · hacknote（UAF）

## 题目附件

本目录保留 `hacknote`、两个原 Python 脚本、IDA 数据库和历史文件。ELF 为 32 位 i386，interpreter 是 `/lib/ld-linux.so.2`。附件没有自带 libc/loader；运行库用 [`libc/2.23/i386/`](ORIGINAL_NOTES.md)，是 2.23 的**本地兼容候选**，不表示它与远程服务精确匹配。

HITCON Training 官方仓库可以确认题目来自训练题集，但不能单独证明这份二进制对应的远程 glibc 版本：[HITCON Training](https://github.com/scwuaptx/hitcon-training)。

## 本地启动

在 Linux 虚拟机中进入共享目录里的题型库根目录，然后运行：

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.23/i386/ld-linux.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/i386/lib" \
  "$PWN_ROOT/libc/2.23/i386/UAF/hacknote"
```

本机 Linux 的运行库不会被替换。启动后可用 `readelf -d` 查看 `NEEDED` 依赖，并在 GDB 中用 `info sharedlibrary` 检查实际加载路径。若 VM 没有 GDB 或 `patchelf`，需在 VM 内安装；本目录只保存题目运行库，不包含调试器。

## 远程脚本提醒

`hacknote.py` 和 `111.py` 原样保留。它们包含远程连接配置；整理过程中没有运行，也没有连接远程服务。先理解本地题目和脚本，再确认题目授权后才考虑远程连接。
