# 静态链接题目

静态 ELF 的 libc 代码已经链接进二进制，不需要选择 `libc/2.xx/` 的动态运行库。

静态题不按 glibc 版本归档，题目实体统一放在栈题目录里：

- [rootersctf_2019_srop](../../../../PWN/Stack/030.rootersctf_2019_srop/rootersctf_2019_srop)：amd64、静态链接。保留原 exploit、debug 脚本、IDA 数据库和历史文件。

检查方式：

```bash
file ./栈/SROP/rootersctf_2019_srop/rootersctf_2019_srop
```

预期能看到 `statically linked`。仍需在 x86-64 Linux 虚拟机运行；静态链接只表示无需动态 libc，不代表跨 CPU 架构。
