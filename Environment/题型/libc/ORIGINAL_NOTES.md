# glibc 运行环境索引

`libc/` 放运行库，同时按版本/架构收纳堆题（`libc/<版本>/<架构>/<题目>/`）；其他题型分在 [`栈/`](../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%88/ORIGINAL_NOTES.md)、[`格式化字符串/`](../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2/ORIGINAL_NOTES.md)、[`other/`](../../../Supporting/%E9%A2%98%E5%9E%8B/other/ORIGINAL_NOTES.md)。堆题另外有索引：[`堆题索引.md`](堆题索引.md)。你主要在 Linux 虚拟机里使用共享目录；不需要为了做题专门搭 Docker。进入 VM 后先 `cd` 到共享目录里的 `题型/`，之后所有命令都从这个目录运行。

| 环境 | 架构 | 运行库状态 | 借用它的题目 |
| --- | --- | --- | --- |
| [glibc 2.23](2.23/i386/ORIGINAL_NOTES.md) | i386 | Ubuntu 16.04 来源的 2.23 libc/loader 已放好 | 堆题 [UAF / hacknote](../../../PWN/Heap/032.hacknote/ORIGINAL_NOTES.md)；格式化字符串题见 [格式化字符串/2.23/i386/](../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2/ORIGINAL_NOTES.md) |
| [glibc 2.23](2.23/amd64/ORIGINAL_NOTES.md) | amd64 | Ubuntu 16.04 官方 `libc6` 2.23-0ubuntu10 的 libc/loader 已放好 | 堆题 [wdb_2018_1st_babyheap](../../../PWN/Heap/031.wdb_2018_1st_babyheap/ORIGINAL_NOTES.md)（自带 `env/`，内容相同）；[格式化字符串/2.23/amd64/wustctf2020_babyfmt](../../../PWN/Format-String/015.wustctf2020_babyfmt/ORIGINAL_NOTES.md) |
| [glibc 2.27](2.27/amd64/ORIGINAL_NOTES.md) | amd64 | 原运行树与 fixed 运行树均保留；标准入口指向可用的 fixed 树 | 堆题 [ciscn_2019_es_1](../../../PWN/Heap/033.ciscn_2019_es_1/ciscn_2019_es_1)、[final_3](../../../PWN/Heap/034.ciscn_2019_final_3/ciscn_final_3)、[hitb2018_gundam](../../../PWN/Heap/035.hitb2018_gundam/gundam)；[bctf2018_hardcore_fmt](../../../PWN/Format-String/020.bctf2018_hardcore_fmt/ORIGINAL_NOTES.md)；栈题脚本借用本目录 `glibc227/` |
| [glibc 2.31](2.31/amd64/ORIGINAL_NOTES.md) | amd64 | Ubuntu 20.04 来源的 2.31 libc/loader 已放好 | [bbctf_2020_fmt_me](../../../PWN/Format-String/021.bbctf_2020_fmt_me/ORIGINAL_NOTES.md)；（[栈/ret2shellcode/shellcode](../../../PWN/Stack/013.shellcode/ORIGINAL_NOTES.md) 自带 `env/`） |
| [glibc 2.35](2.35/amd64/ORIGINAL_NOTES.md) | amd64 | 2.35-0ubuntu3.1 libc/loader 的真实副本 | 堆题 [VIPhouse](../../../PWN/Heap/036.VIPhouse/ORIGINAL_NOTES.md)；[other/2.35/amd64/下溢](../../../PWN/VM/038.%E4%B8%8B%E6%BA%A2) 自带同版 `env`；栈题 `guarded_echo`、`Caged_Signal` 借用本目录；[格式化字符串漏洞](../../../Supporting/%E9%A2%98%E5%9E%8B/%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2/2.35/amd64/%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%BC%8F%E6%B4%9E) 为本地实验 |
| [静态 ELF](static/ORIGINAL_NOTES.md) | amd64 | 不需要动态 libc | [栈/SROP/rootersctf_2019_srop](../../../PWN/Stack/030.rootersctf_2019_srop) |

## 当前 UTM 虚拟机的验收边界

版本页记录的 loader 启动烟测证明这些文件曾在 Linux/amd64 环境中运行，不自动证明当前 UTM 共享目录挂载也可执行。本轮在 macOS 完成了启动脚本语法、VS Code JSON、Markdown 本地链接、符号链接及强制临时复制流程检查；GDB 分支使用模拟的 `gdb`/`patchelf` 验证了 noexec 下复用临时目标副本及退出清理，不等于真实调试器或 ELF 已运行。

2026-10-22 的 UTM 复验只确认 Ubuntu 22.04.5 已登录。尝试通过 UTM 控制台输入只读检查命令时，按键映射把命令字符转换错乱，输出不可信；已停止输入并释放键鼠捕获，没有把这次尝试记作验收。共享目录的 Linux 路径、挂载是否带 `noexec`、GDB/pwndbg/patchelf 是否可用，以及启动脚本能否在当前 VM 完成运行与调试，仍待可靠的 VM 内终端输入后验证。macOS 上的静态或模拟检查不能替代这项验收。

进入 VM 后，在题型库根目录运行以下只读检查，再用实际题目验证启动与 GDB：

```bash
pwd
uname -m
findmnt -T "$(pwd)" -o TARGET,FSTYPE,OPTIONS
command -v gdb patchelf
bash tools/pwn-env.sh run 2.27 amd64 libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1
bash tools/pwn-env.sh gdb 2.27 amd64 libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1
```

GDB 中执行 `start` 和 `info sharedlibrary`，确认实际加载的是题库里的 2.27 libc；若共享挂载含 `noexec`，再检查启动器是否提示复制到 `/tmp`，并确认题目菜单能正常出现。未完成这些步骤前，状态保持“文件已归档、VM 待验收”。

## 在虚拟机里直接启动

在 VM 的终端进入共享目录中的 `题型/` 后，设置一个仅供本终端使用的路径变量：

```bash
PWN_ROOT="$(pwd)"
```

这里的路径应是 **Linux 虚拟机实际看到的挂载路径**，不是 macOS 上的 `/home/ctf` 路径。先用 `pwd` 确认当前确实位于共享目录里的 `题型/` 根目录；不同虚拟机软件的挂载点可能不同，所以不要把某个固定挂载点写死。

按题目版本调用对应 loader。示例：

```bash
# glibc 2.23 / i386
"$PWN_ROOT/libc/2.23/i386/ld-linux.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/i386/lib" \
  "$PWN_ROOT/libc/2.23/i386/UAF/hacknote"

# glibc 2.23 / amd64
"$PWN_ROOT/libc/2.23/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.23/amd64" \
  "$PWN_ROOT/libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap"

# glibc 2.27 / amd64
"$PWN_ROOT/libc/2.27/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu" \
  "$PWN_ROOT/libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1"

# glibc 2.35 / amd64
"$PWN_ROOT/libc/2.35/amd64/ld-linux-x86-64.so.2" \
  --library-path "$PWN_ROOT/libc/2.35/amd64" \
  "$PWN_ROOT/other/2.35/amd64/下溢/postfix_jit"
```

glibc 2.31 目录是备用运行环境，目前没有已确认匹配的题目。i386 题需要 VM 内核支持 32 位 ELF；如果报 `Exec format error`，使用 32 位 x86 Linux VM，或确认当前 x86-64 VM 启用了 IA32 兼容支持。ARM Linux VM 不能直接运行这些 x86 ELF。

## 用 GDB 调试

GDB 通常需要把目标解释器和库路径写进 ELF。原始题目文件不要直接改：复制一份到 `/tmp`，再只 patch 副本。先在 VM 安装/确认 `gdb`、`patchelf`，路径使用 VM 里共享目录的实际挂载路径，不要粘贴 macOS 的 `/home/ctf` 路径。

下面是 amd64 2.27 的示例：

```bash
cp "$PWN_ROOT/libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1" /tmp/es1_vm
patchelf --set-interpreter "$PWN_ROOT/libc/2.27/amd64/ld-linux-x86-64.so.2" /tmp/es1_vm
patchelf --set-rpath "$PWN_ROOT/libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu" /tmp/es1_vm
gdb -q /tmp/es1_vm
```

调试时用 `info sharedlibrary` 核对实际加载路径。若只用指定 loader 启动成功，记录为“启动验证”；只有 GDB 确认加载路径且题目交互正常，才记录为“VM 调试验证”。

### 共享目录提示

如果 VM 能看到文件，但执行 loader 或题目时仍报 `Permission denied`，先查看共享目录的挂载选项：

```bash
findmnt -T "$PWN_ROOT" -o TARGET,FSTYPE,OPTIONS
```

若选项含 `noexec`，这表示共享目录禁止直接执行其中的 ELF；反复 `chmod +x` 通常不能解决挂载策略。把所需版本目录复制到 VM 自己的 Linux 文件系统再运行，例如：

```bash
mkdir -p "$HOME/pwn/libc/2.27"
cp -a "$PWN_ROOT/libc/2.27/amd64" "$HOME/pwn/libc/2.27/"
PWN_ROOT="$HOME/pwn"
```

复制后沿用上面的 loader 命令即可。`cp -a` 会保留题目目录中的相对符号链接；若共享目录本身允许执行，则不需要复制。

## 版本判断要点

- `file` 看 ELF 架构和 interpreter；`readelf -d` 看动态依赖；`readelf --version-info` 看二进制要求的 GLIBC 符号版本。
- `strings libc.so.6`、Build ID 或发行版包信息可识别某个 libc 文件；`ldd --version` 只说明当前 VM 的系统 libc。
- ELF 的最低符号要求只能说明“某个版本可能兼容”，不能单独证明题目远程环境的精确版本。
- 运行时应指定 loader，再在 GDB 里看 `info sharedlibrary`；不要仅因为目录里有 `libc.so.6` 就认定程序用了它。

## 资料

- [ld.so(8) 手册](https://man7.org/linux/man-pages/man8/ld.so.8.html)：动态加载器、解释器及库搜索路径。
- [Ubuntu 旧版本 glibc 包归档](https://old-releases.ubuntu.com/ubuntu/pool/main/g/glibc/)：2.23 等旧版包的官方归档。当前 2.23/2.31 文件来源和 Build ID 见各版本页。

要从命令行统一启动或进入 GDB，请使用 [`pwn-env.sh`](../../../Labs/C-Memory/001.%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0/pwn-env.sh)，使用示例见 [`tools/README.md`](../../../Labs/C-Memory/001.%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0/ORIGINAL_NOTES.md)。本地 EXP 的启动方式显式选择归档 loader/libc；若共享挂载为 `noexec`，按上文复制到 VM 文件系统，或使用工具脚本的临时运行时复制功能。无论哪种启动方式，只有 GDB 的 `info sharedlibrary` 能确认该次进程实际加载的库。
