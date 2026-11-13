# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

题型或原始题名尚待确认，保留附件原名。

## 文件

- [333.py](333.py)
- [398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5.pyc](398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5.pyc)
- [398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py](398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py)
- [recovered.py](recovered.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

本地 Python 2.7 字节码中的提示和变换与 GWCTF2019 pyre 一致。333.py 是原求解代码；两个反编译稿存在缺失变量和顶层 return，作为分析记录保留。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/Dav-ove3/p/17244088.html)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [333.py](333.py)
- [398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py](398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py)
- [recovered.py](recovered.py)
- [solve.py](solve.py)

```python
"""Invert the add-index and adjacent-XOR stages from the local pyre bytecode notes."""
code = bytes([31, 18, 29, 40, 48, 52, 1, 6, 20, 52, 44, 27, 85, 63, 111, 54, 42, 58, 1, 68, 59, 37, 19])
values = list(code)
for index in range(len(values) - 2, -1, -1):
    values[index] ^= values[index + 1]
plain = bytes((value - index) % 128 for index, value in enumerate(values))
forward = [(value + index) % 128 for index, value in enumerate(plain)]
for index in range(len(forward) - 1):
    forward[index] ^= forward[index + 1]
assert bytes(forward) == code
print(plain.decode("ascii"))
```
