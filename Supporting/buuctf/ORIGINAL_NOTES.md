# buuctf 工作区索引

按 `~/Desktop/work/题型/` 的体系分类：栈题按 ret2 系列分组，堆题进 `libc/<glibc>/<架构>/`，VM/内核/非 glibc 平台进 `other/`，非 PWN 单列 `misc/`、`web/`。

> 本目录**不是 git 仓库**，移动/改名不可回滚。脚本里的相对路径按题目目录内自洽设计；babel 的 `/mnt/work/buuctf/...` 绝对路径已同步改成新位置。

## 目录

```text
buuctf/
├── 栈/
│   ├── ret2text/                      # 目前为平铺文件
│   │   ├── rip、rip.py                 RIP（BUUCTF，栈溢出跳后门）
│   │   ├── jarvisoj_level0            level0（callsystem 后门）
│   │   ├── get_started_3dsctf_2016    32 位静态，get_flag(a,b)
│   │   ├── ciscn_2019_n_8             全局数组变量覆盖（非 ret2）
│   │   └── mrctf2020_easyrop          菜单 read 溢出 + system@plt
│   ├── ret2libc/ciscn_2019_c_1/       ciscn_2019_c_1（BUUCTF，泄露 puts → system）
│   ├── ret2csu/blind_pwn/             blind pwn（seccomp 只留 read，ret2csu + 退出码外带）
│   └── CANARY/easytl/                 easytl（TLS SNI 溢出，canary + ROP ORW）
├── libc/2.39/amd64/bad_puppet/        bad_puppet（C++ 堆题，double free / 类型混淆）
├── other/
│   ├── 2.39/amd64/babel/              babel（BUUCTF，OCaml 字节码 VM + GC 悬垂引用）
│   ├── uClibc-1.0.32/mips64/oldsvr/   oldsvr（MIPS64 MQTT broker 堆溢出）
│   └── windows-x64/ironclad/          Ironclad（Windows 内核驱动分析）
├── misc/
│   ├── neuron_shuffle/                NeuronShuffle（模型打乱顺序还原，未解）
│   ├── zelda/                         剑士 Hero 文本游戏（黑盒逻辑 + 结构体覆盖）
│   └── sat/                           模拟卫星测控站（CCSDS/CFDP 协议，附件型远端）
└── web/
    └── vaultlink/                     VaultLink（HTTP 代理 SSRF + WebSocket）
```

## 题目索引

| 题目 | 分类 | 来源 | 状态 | 关键文件 |
|---|---|---|---|---|
| rip | 栈 / ret2text | BUUCTF | 脚本可跑 | `rip`、`rip.py` |
| jarvisoj_level0 | 栈 / ret2text | BUUCTF | 有 `callsystem` 后门 | `jarvisoj_level0` |
| get_started_3dsctf_2016 | 栈 / ret2text | BUUCTF | 32 位静态，调 `get_flag(0x308cd64f, 0x195719d1)` | `get_started_3dsctf_2016` |
| ciscn_2019_n_8 | 栈 / ret2text（实为变量覆盖） | BUUCTF | 无 ret2；`scanf("%d")` 写全局数组，使 `[13]=0`、`[14]=17` | `ciscn_2019_n_8` |
| mrctf2020_easyrop | 栈 / ret2text | BUUCTF | 菜单三项不同长度 `read` 溢出，`system@plt` 可用 | `mrctf2020_easyrop` |
| ciscn_2019_c_1 | 栈 / ret2libc | BUUCTF | 两阶段 exp 完整 | `ciscn_2019_c_1`、`final_exp.py`、`Dockerfile`（ubuntu:16.04） |
| blind_pwn | 栈 / ret2csu | — | 本地已出 flag；远端 1 bit 信道 | `blind_pwn.md`、`blind_pwn_remote.md`、`att/`、`exp_blind*.py` |
| easytl | 栈 / CANARY | — | 工作区（TLS 握手构造 + ROP） | `exploit.py`、`pwn.py`、`easytl`、`libs/`（空） |
| bad_puppet | 堆 / glibc 2.39 amd64 | — | 本地链已通，远端待定 | `bad_puppet/`（含 `libs/`）、`exp/`、`chall.zip`；分析见 `misc/zelda/ANALYSIS2.md` |
| babel | other / VM-JIT / glibc 2.39 | BUUCTF | 本地 flag 已拿 | `babel_wp.md`、`lab/`、`exploit*.py` |
| oldsvr | other / MIPS64 uClibc | — | 本地 qemu 全通，远端缺 libc 基址 | `WRITEUP.md`、`server`、`rootfs/`、`tools/` |
| ironclad | other / Windows 内核 | — | 仅静态分析 | `analysis.md`、`exploit.c` |
| neuron_shuffle | misc | — | 未解（结论：缺随机种子/规范化规则） | `ns_solve/SUMMARY_1PAGE.md`、`neuron_shuffle.zip` |
| zelda | misc（逻辑） | — | 游戏内通关，未出 flag | `ANALYSIS.md`、`win*.py`、`bad_puppet/`（该题附带副本） |
| sat | misc / 协议 | — | 实例未起，仅协议侦察 | `README.md`、`satlib.py`、`recon.py` |
| vaultlink | web | — | 探测脚本集 | `ws.py`、`scan*.py`、`auth*.py` |

## 说明

- `libc/2.39/amd64/bad_puppet/bad_puppet/libs/` 来自原附件 `chall.zip`（glibc 2.39 / GCC 13，Ubuntu 24.04）；`misc/zelda/` 里另有一份同题附件副本，保留给该工作区的 `localchain*.py` 使用。
- `栈/ret2csu/` 是新建的 ret2 子类：blind pwn 靠 `__libc_csu_init` 的 pop/call gadget 调 `read`，不属于 ret2libc/ret2syscall。
- 已清掉的内容：两个 core dump、`.DS_Store`、`.gdb_history`、`.vscode`、`__pycache__`、`.til`、`pwn1`（`rip` 重复）、`ciscn_2019_es_1`（`题型/libc/2.27/amd64/ciscn_2019_es_1` 已有同哈希副本）、DASCTF 残留 `exp.py`/`exp_副本.py`、`exp_blind.py.bak`、写坏的 `ciscn_2019_c_1.py`、重复的 `zelda/bad_puppet.zip`。
