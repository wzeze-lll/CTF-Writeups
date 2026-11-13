# 知识点

C-Memory

# 题目分析

分类：Labs / C-Memory。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [1.c](1.c)
- [1111.c](1111.c)
- [123.c](123.c)
- [2.c](2.c)
- [21.c](21.c)
- [3.c](3.c)
- [3.py](3.py)
- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [check-env.sh](check-env.sh)
- [pwn-env.sh](pwn-env.sh)
- [scratch/111.py](scratch/111.py)

## 已有分析

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)

### tools

这里放通用小实验和不属于某一道题的辅助材料。

#### labs

- `labs/memory_layout/`：`test.c` 及原有编译产物 `test`，用于观察基础内存布局。
- `labs/pointer_demo/`：`zhizhen.c` 及原有编译产物 `zhizhen`，用于练习指针。

#### scratch

- `scratch/111.py`：原目录中的 1 字节空白脚本，先保留，未推测用途。

#### 共享目录里不要放软链接

本库通过 UTM 的 virtio-9p 共享给 Linux 虚拟机。2026-10-27 实测：**宿主机（Mac）侧创建的软链接，在虚拟机里一律不可用**——`readlink` 返回空，`cat`/`ls` 报 `Too many levels of symbolic links`。对照组：同一个目录里由虚拟机自己 `ln -s` 的链接正常。

因此约定：`libc.so.6`、`ld-linux-x86-64.so.2` 这类别名**全部用真实文件副本**（`cp`），不要用 `ln -s`。多占几 MB，但 Mac 和虚拟机两边都能用。

改动运行库材料后可跑检查：

```bash
bash tools/check-env.sh
```

脚本会列出所有软链接和非 ELF 的占位文件；在虚拟机里运行时还会额外验证每个条目能否解析。

#### 使用配套 glibc 启动或调试题目

在 Linux x86-64 虚拟机中，从本目录所在的题型库执行：

```bash
bash tools/pwn-env.sh run 2.27 amd64 libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1
bash tools/pwn-env.sh gdb 2.27 amd64 libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1
```

将 `2.27 amd64` 换成题目对应的版本和架构；32 位题用 `2.23 i386`，静态题用 `static amd64`。如果题目目录自带 `env/`（里面有 `libc.so.6` 和 `ld-*`），脚本会自动改用这份运行库并打印 `Using challenge-local runtime:`——同一个 glibc 版本的不同补丁版不能混用。命令里的版本参数这时只作为默认值。`gdb` 模式只修改 `/tmp` 中的临时副本，不修改原题文件；进入 GDB 后用 `start`，再用 `info sharedlibrary` 核对实际加载路径。

如果 VM 共享目录带 `noexec`，脚本会把目标 ELF、loader 和对应库临时复制到 `/tmp` 再运行；只复制 loader/libc 不够，因为目标 ELF 的可执行段也需要从允许执行映射的文件系统加载。临时副本在命令结束后清理，原附件不改。若自动检测失败，可显式执行：

```bash
PWN_FORCE_RUNTIME_COPY=1 bash tools/pwn-env.sh run 2.27 amd64 libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1
```

GDB 模式需要 VM 中有 `gdb` 与 `patchelf`。Ubuntu 可用 `sudo apt install gdb patchelf` 安装；若 VM 没有网络或不能安装软件，需在 VM 内补齐后才能完成调试验证。

运行前可先确认工具和虚拟机架构：

```bash
uname -m
gdb --version | head -n 1
patchelf --version
python3 -c 'from pwn import *; print("pwntools:", pwnlib.__version__)'
```

本题库中的本地 EXP 启动方式已改为显式调用对应版本 loader；静态 ELF 仍直接启动。远程连接分支只保留在脚本中，没有在整理过程中运行。GDB 中的 `info sharedlibrary` 是运行时确认 libc 路径的依据；`ldd --version` 只显示 VM 系统自带 glibc，不能代替这一步。

已有二进制与源码一并保留；实验二进制应由对应源码重新编译后再比较，不把旧二进制视为源码的必然产物。


# EXP

- [labs/memory_layout/test.c](labs/memory_layout/test.c)
- [labs/pointer_demo/zhizhen.c](labs/pointer_demo/zhizhen.c)
- [scratch/111.py](scratch/111.py)
- [1.c](1.c)
- [2.c](2.c)
- [3.c](3.c)
- [1111.c](1111.c)
- [21.c](21.c)
- [123.c](123.c)
- [3.py](3.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```c
#include <stdio.h>
 
int main()
{
    char key[18]={
        180, 136, 137, 147, 191, 137, 147, 191, 148, 136,
        133, 191, 134, 140, 129, 135, 191, 65 };
        for(int i=0;i<18;i++)
        {
            key[i]=key[i]^0x20-64; 
            printf("%c",key[i]);
        }
    return 0;
}
```
