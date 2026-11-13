# 格式化字符串索引

`printf(buf)` 一类漏洞单独成类，内部按**版本 → 架构 → 题目**分目录；运行库仍用 [`libc/<版本>/<架构>/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/ORIGINAL_NOTES.md)，题目自带 `env/` 的优先用自己的。

| 题目 | 版本 / 架构 | 备注 | 状态 |
| --- | --- | --- | --- |
| [wdb_2018_2nd_easyfmt](../../../PWN/Format-String/019.wdb_2018_2nd_easyfmt/ORIGINAL_NOTES.md) | 2.23 / i386 | 死循环 `printf(buf)`；GOT 可写 | 本地兼容候选；仅静态确认 |
| [axb_2019_fmt32](../../../PWN/Format-String/016.axb_2019_fmt32/ORIGINAL_NOTES.md) | 2.23 / i386 | 每轮 `alarm(3)`；`sprintf` 前缀 `Repeater:` | 本地兼容候选；仅静态确认 |
| [hitcontraining_playfmt](../../../PWN/Format-String/017.hitcontraining_playfmt/ORIGINAL_NOTES.md) | 2.23 / i386 | Debian GCC 6.4 编译，版本待核（可能 2.24） | 本地兼容候选；仅静态确认 |
| [suctf_2019_playfmt](../../../PWN/Format-String/018.suctf_2019_playfmt/ORIGINAL_NOTES.md) | 2.23 / i386 | Ubuntu 16.04 GCC 5.4 编译 | 本地兼容候选；仅静态确认 |
| [wustctf2020_babyfmt](../../../PWN/Format-String/015.wustctf2020_babyfmt/ORIGINAL_NOTES.md) | 2.23 / amd64 | PIE；Ubuntu 16.04 GCC 5.4 编译 | 本地兼容候选；仅静态确认 |
| [bctf2018_hardcore_fmt](../../../PWN/Format-String/020.bctf2018_hardcore_fmt/ORIGINAL_NOTES.md) | 2.27 / amd64 | PIE；Ubuntu 18.04 GCC 7.3 编译 | 本地兼容候选；仅静态确认 |
| [bbctf_2020_fmt_me](../../../PWN/Format-String/021.bbctf_2020_fmt_me/ORIGINAL_NOTES.md) | 2.31 / amd64 | Arch GCC 9.3 编译 | 本地兼容候选；仅静态确认 |
| [格式化字符串漏洞 / fmt_test](2.35/amd64/格式化字符串漏洞/) | 2.35 / amd64 | 自己编译的 `fmt_test.c` 小实验，不是比赛原题 | 仅本地实验 |

- 版本标签只说明架构和符号需求允许该版本运行，不证明远程环境就是这一版；`hitcontraining_playfmt` 的 Debian GCC 6.4 更可能对应 2.24，但库内没有 2.24 运行库，暂借 2.23 i386。
- 这些题都没有在 VM 里跑过，状态是“文件已归档、VM 待验收”。共享目录约束和启动方式见 [`libc/README.md`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/ORIGINAL_NOTES.md)。
