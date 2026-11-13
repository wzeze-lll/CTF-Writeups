# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [luck_guy](luck_guy)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

3.c 和 1111.c 内容相同，对应 luck_guy 的分支重排；保留原文件名，solve.py 给出一致的 Python 解法。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/yushiting/p/17211804.html)

本地反汇编中，常量逐字节通过 movb 写入栈，见 [关键函数](key_function.asm)。

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [1111.c](1111.c)
- [3.c](3.c)
- [solve.py](solve.py)

```python
"""Reproduce the local luck_guy case 4 -> case 5 -> case 1 data path."""
from pathlib import Path

sample = Path(__file__).with_name("luck_guy").read_bytes()
assert b"GXY{do_not_" in sample
encoded = bytes.fromhex("69637567606f667f")
assert all(bytes([0xc6, 0x45, 0xd0 + index, value]) in sample
           for index, value in enumerate(encoded))
plain = bytes(value - (2 if index % 2 else 1) for index, value in enumerate(encoded))
print("GXY{do_not_" + plain.decode("ascii"))
```
