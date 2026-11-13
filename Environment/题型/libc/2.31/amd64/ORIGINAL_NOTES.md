# glibc 2.31 · amd64

## 环境来源与核验

运行库从 Ubuntu 20.04 amd64 环境提取。libc 报告 GNU libc **2.31-0ubuntu9.17**。文件为 `lib/libc-2.31.so` 与 `lib/ld-2.31.so`，均为 ELF 64-bit x86-64。Build ID：libc `0323ab4806bee6f846d9ad4bccfc29afdca49a58`，loader `cb904567e1b2a460b6fc20817776ad590d265686`。

顶层 `libc.so.6`、`ld-linux-x86-64.so.2` 与 `lib/` 里的文件都是**真实文件副本**（本库不允许软链接）。借用本目录运行库的题目：[bbctf_2020_fmt_me](../../../../../PWN/Format-String/021.bbctf_2020_fmt_me/ORIGINAL_NOTES.md)（Arch GCC 9.3 编译，2.31 兼容候选）。[`栈/ret2shellcode/shellcode`](../../../../../PWN/Stack/013.shellcode/ORIGINAL_NOTES.md) 自带 `env/`，不用这里的库。

## 在 Linux 虚拟机使用

在 VM 中进入共享目录里的题型库根目录。将来有匹配 2.31 的题目时，把 `<target>` 换成题目路径：

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.31/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.31/amd64/lib" \
  <target>
```

目录内库文件可以这样核验版本：

```bash
"$PWN_ROOT/libc/2.31/amd64/libc.so.6"
file "$PWN_ROOT/libc/2.31/amd64/ld-linux-x86-64.so.2"
```

已在 Linux/amd64 环境用指定 loader 加载 `/bin/true`，并确认解析到本目录的 `libc.so.6`；当前没有题目在本目录中完成运行验证。来源版本与文件 Build ID 不是题目远程环境的证明。GDB 调试方式见 [`libc 运行环境索引`](../../ORIGINAL_NOTES.md)。
