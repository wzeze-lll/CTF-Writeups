# PWN 题型与运行环境

题目先按**题型**分开：堆题和运行库一起放在 `libc/<版本>/<架构>/`（堆题内部再按 glibc 版本 → 架构 → 题目），栈题在 `栈/`（不按 glibc 分，按 ret2 体系和专题分组），格式化字符串题在 `格式化字符串/`（按版本 → 架构分），VM/JIT 等无法归类的题在 `other/`。运行库只当环境使用。这个目录通过共享文件夹供 Linux 虚拟机使用；macOS 本机不能直接执行这些 Linux ELF。进入虚拟机后从共享目录打开本项目，具体启动方式见 [运行环境索引](../../Environment/%E9%A2%98%E5%9E%8B/libc/ORIGINAL_NOTES.md)。`tools/` 保存本地小实验。

```text
题型/
├── 栈/                            # 栈题，不分 glibc 版本
│   ├── ret2text/                  # guarded_echo
│   ├── ret2libc/                  # stack1、rpg
│   ├── ret2syscall/               # seccomp_orw（自带 env/）
│   ├── ret2shellcode/             # shellcode（RWX mmap；自带 env/）
│   ├── CANARY/                    # pwn118、pwn119、babypie
│   ├── SROP/                      # ciscn_2019_es_7、Caged_Signal、rootersctf_2019_srop
│   └── README.md
├── 格式化字符串/                   # 格式化字符串题：版本 → 架构 → 题目
│   ├── 2.23/i386/{wdb_2018_2nd_easyfmt,axb_2019_fmt32,hitcontraining_playfmt,suctf_2019_playfmt}/
│   ├── 2.23/amd64/wustctf2020_babyfmt/
│   ├── 2.27/amd64/bctf2018_hardcore_fmt/
│   ├── 2.31/amd64/bbctf_2020_fmt_me/
│   ├── 2.35/amd64/格式化字符串漏洞/
│   └── README.md
├── other/                         # VM/JIT 等无法归类的题
│   ├── 2.27/amd64/are_you_root/
│   ├── 2.35/amd64/下溢/
│   ├── 2.35/amd64/baby_randomized_vm_001
│   └── README.md
├── libc/                          # 运行库 + 堆题（版本 → 架构 → 题目）
│   ├── 2.23/i386/UAF/             # hacknote
│   ├── 2.23/amd64/wdb_2018_1st_babyheap/
│   ├── 2.27/amd64/{ciscn_2019_es_1,ciscn_2019_final_3,hitb2018_gundam}/
│   ├── 2.31/amd64/
│   ├── 2.35/amd64/VIPhouse/
│   ├── static/                    # 静态链接题说明
│   ├── 堆题索引.md
│   └── README.md
└── tools/                         # C 小实验、脚本和临时练习
```

## 入口

- [glibc 版本与环境说明](../../Environment/%E9%A2%98%E5%9E%8B/libc/ORIGINAL_NOTES.md)
- [堆题索引](../../Environment/%E9%A2%98%E5%9E%8B/libc/%E5%A0%86%E9%A2%98%E7%B4%A2%E5%BC%95.md)
- [栈题索引](%E6%A0%88/ORIGINAL_NOTES.md)
- [格式化字符串索引](%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2/ORIGINAL_NOTES.md)
- [其他题型索引](other/ORIGINAL_NOTES.md)
- [本地实验工具](../../Labs/C-Memory/001.%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0/ORIGINAL_NOTES.md)

Linux VM 的统一本地启动 / GDB 入口见 [配套环境使用说明](../../Labs/C-Memory/001.%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0/ORIGINAL_NOTES.md)。`.vscode/` 是工作站侧的编辑配置：其中编译器和 LLDB 是 macOS 主机工具，不能用来运行本题库的 Linux ELF；`launch.json` 已清空旧项目的绝对路径配置，避免误启动其他目录里的程序。请在 x86-64 Linux VM 中通过 `pwn-env.sh gdb ...` 使用 GDB。此目录目前只记录已归档的 libc 与候选题目，不把静态兼容性写成远程版本证明。

## 版本标签怎么读

- **附件匹配**：题目目录确实带有对应 libc/loader，且本地 loader 启动验证过。
- **附件自带运行库**：题目目录下的 `env/` 里放着自己的 libc/loader（包内还需 `libseccomp.so.2` 等依赖时也放这里）。这种题优先用 `env/`，不要套共享版本库——同一 glibc 版本的不同补丁版偏移可能不同。
- **本地兼容候选**：题目 ELF 的架构与最低 GLIBC 符号需求允许该版本运行；这不证明比赛远程环境就是该版本。
- **静态**：ELF 静态链接，不需要从 `libc/<版本>/` 选择动态 libc。
- **待验证**：只完成静态归档或文件检查，尚未在目标 Linux 环境启动/调试。

`libc.so.6` 是常见文件名，不是版本号。每次复现都要检查目标架构、ELF interpreter、加载器、依赖库和实际加载路径。版本目录内保存的库是运行环境材料；题目自身目录中的原始附件和脚本也都保留。

本库只用于合法 CTF、课程、靶场和本地实验。含有远程连接参数的脚本没有在整理过程中运行。

## 目录调整记录

- 2026-11-05（再补）：按用户要求把堆题**合并回 `libc/`**，直接放在 `libc/<版本>/<架构>/<题目>/`，与运行库同目录；删除顶层 `堆/`，原 `堆/README.md` 改为 [`libc/堆题索引.md`](../../Environment/%E9%A2%98%E5%9E%8B/libc/%E5%A0%86%E9%A2%98%E7%B4%A2%E5%BC%95.md)。同时把栈题按 ret2 体系分成 `栈/ret2text/`、`栈/ret2libc/`、`栈/ret2syscall/`、`栈/ret2shellcode/`，保留 `CANARY/`、`SROP/`。所有 README、脚本和 `pwn-env.sh` 示例路径同步更新。
- 2026-11-05（补）：把格式化字符串题从 `other/` 拆出来，单独建 `格式化字符串/<版本>/<架构>/<题目>/`；`other/` 只留 VM/JIT 和分类存疑题（are_you_root、下溢、baby_randomized_vm_001）。
- 2026-11-05：按用户要求把**栈题和堆题分成两类**：`stack/` 改名 `栈/`；新建 `堆/<版本>/<架构>/<题目>/`，把原 `libc/<版本>/<架构>/` 下的堆题（UAF、wdb_2018_1st_babyheap、ciscn_2019_es_1、ciscn_2019_final_3、hitb2018_gundam）挪过去；新建 `other/` 放格式化字符串、VM/JIT 等非堆非栈题（wdb_2018_2nd_easyfmt、下溢、格式化字符串漏洞、baby_randomized_vm_001、are_you_root）。`libc/` 从此只保留运行库。所有 README、脚本和 `pwn-env.sh` 的路径同步更新。
- 2026-10-27：取消 `libc/<版本>/<架构>/challenges/<题型>/` 这一层，题目直接放在版本目录下；栈题统一移到 `stack/`，按 CANARY / SROP 分组；同时修正了脚本里的根目录层级、软链接和文档路径。
- 2026-10-27（补）：发现 Mac 侧创建的软链接在虚拟机里不可用（9p 共享限制，报 ELOOP），已把全部运行库别名改成真实文件副本；`libc/2.23/i386` 的库文件（此前误留在废纸篓）已恢复。详见 [tools/README.md](../../Labs/C-Memory/001.%E6%9C%AC%E5%9C%B0%E7%BB%83%E4%B9%A0/ORIGINAL_NOTES.md)。
