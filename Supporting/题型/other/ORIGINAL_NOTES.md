# 其他题型索引

不属于堆、栈、格式化字符串的题放这里：VM/JIT、逆向类，以及分类还没定的题。仍然按**版本 → 架构 → 题目**分目录，运行库用 [`libc/<版本>/<架构>/`](../../../Environment/%E9%A2%98%E5%9E%8B/libc/ORIGINAL_NOTES.md) 或题目自带的 `env/`。

| 题目 | 题型 | 版本 / 架构 | 状态 |
| --- | --- | --- | --- |
| [PicoCTF_2018_are_you_root](../../../PWN/Heap/037.are_you_root) | 堆 UAF / 越权（分类存疑） | 2.27 / amd64 | 原目录标 `2.27/i386`，二进制实为 x86-64；版本待核 |
| [下溢 / postfix_jit](../../../PWN/VM/038.%E4%B8%8B%E6%BA%A2) | VM/JIT、表达式栈下溢 | 2.35 / amd64 | 附件自带 libc/loader；启动验证过 |
| [baby_randomized_vm_001](../../../PWN/VM/039.baby_randomized_vm_001/baby_randomized_vm_001) | VM / 逆向 | 2.35 / amd64 | 兼容候选；单文件 |

- `are_you_root` 的利用是 `login` malloc 出 `user` 结构、`reset` 后不置空、再次 `login` 复用同一 chunk 拿到残留 `auth`，机制上属于堆 UAF；但旧归档目录 `libc/2.27/i386/` 与二进制架构（x86-64）对不上，运行库也没核过，所以先放 `other/`，确认后再决定是否挪进 `libc/2.27/amd64/`。
- `下溢` 的真题面写的是“堆/逻辑栈下溢、JIT”，实际是 postfix 表达式虚拟机自己的栈溢出/下溢，不是 glibc 堆，也没有栈溢出题那种保存 RIP，暂按 VM 题归档。
- 格式化字符串题已单独放到 [`格式化字符串/`](../%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AD%97%E7%AC%A6%E4%B8%B2/ORIGINAL_NOTES.md)，不再混在这里。
- 这几道题的原始附件、IDA 数据库、core 都跟着目录一起搬过来了。
