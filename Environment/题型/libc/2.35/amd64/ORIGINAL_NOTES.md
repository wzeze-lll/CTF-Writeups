# glibc 2.35 · amd64

本环境的 `libc.so.6` 与 `ld-linux-x86-64.so.2` 是从“下溢”题随附文件复制来的**真实副本**（不是软链接，本库禁止 9p 下的软链接）；文件标识为 Ubuntu GLIBC 2.35-0ubuntu3.1、x86-64，与 `other/2.35/amd64/下溢/` 里的 libc 字节相同。题目本体按题型分在 `other/`、`栈/`、`格式化字符串/`；本目录同时保留了堆题 `VIPhouse/`。

## 借用本目录运行库的题目

| 题目 | 题型 | 归档状态 |
| --- | --- | --- |
| [下溢 / postfix_jit](../../../../../PWN/VM/038.%E4%B8%8B%E6%BA%A2/postfix_jit) | VM/JIT、逻辑栈下溢 | 附件自带 glibc 2.35 与 loader，版本来源最直接；附件匹配 |
| [格式化字符串漏洞 / fmt_test](../../../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2/2.35/amd64/%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%BC%8F%E6%B4%9E/fmt_test) | 格式化字符串 | amd64，最低符号需求兼容 2.35；不是远程版本证明 |
| [baby_randomized_vm_001](../../../../../PWN/VM/039.baby_randomized_vm_001/baby_randomized_vm_001) | VM/逆向 | ELF 需要 GLIBC_2.34 起始符号；2.35 本地兼容候选 |
| [VIPhouse](../../../../../PWN/Heap/036.VIPhouse/ORIGINAL_NOTES.md) | 堆 / UAF（混合 fmt） | 需要 GLIBC_2.34，Ubuntu 22.04 GCC 11.3 编译；2.35 本地兼容候选 |

栈题 `guarded_echo`、`Caged Signal`、`seccomp_orw` 在 [`栈/`](../../../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%88/ORIGINAL_NOTES.md)，因为栈题不按 glibc 分目录；本目录的 2.35 运行库仍是 `guarded_echo` 和 `Caged Signal` 的启动环境。

“兼容候选”表示符号版本和架构允许尝试，不表示题目原始远程环境为 glibc 2.35。`postfix_jit` 所在题目目录同时保留原 `vm.tar.gz`、二进制、libc 与 loader。

`seccomp_orw` 是另一套来源：它的 `env/` 里是 **2.35-0ubuntu3.15** 的 libc/loader（本目录共享库是 3.1 版），并额外需要 `libseccomp.so.2`。两者 soname 相同但文件不同，heap 偏移不要互相套用；跑这题请用它自己的 `env/`。

## 在 Linux 虚拟机用本目录 loader 启动

在 VM 中进入共享目录里的题型库根目录，然后运行：

```bash
PWN_ROOT="$(pwd)"
"$PWN_ROOT/libc/2.35/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.35/amd64" \
  "$PWN_ROOT/other/2.35/amd64/下溢/postfix_jit"
```

本次在 Linux/amd64 环境验证 loader 解析到题目目录里的 libc，并实际启动 `postfix_jit`，程序显示启动信息后因 stdin EOF 以状态 1 退出；这仅是启动检查，不是题目 EXP 验证。调试时在 GDB 中用 `info sharedlibrary` 检查实际加载路径。ARM Linux VM 不能直接运行 amd64 ELF，应使用 x86-64 Linux VM。
