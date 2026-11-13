# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

题型或原始题名尚待确认，保留附件原名。

## 文件

- [e290a2112fa5e3068dcc990b842bc6fcabb8dac5949986a60f2cd56239d94c58.exe](e290a2112fa5e3068dcc990b842bc6fcabb8dac5949986a60f2cd56239d94c58.exe)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

本地 PE 同时包含 ak1w、V1Ax 两个比较常量。123.c 对应排序阶段，solve.py 补齐字符与 Base64 约束。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/Mayfly-nymph/p/11488817.html)
- [个人已有笔记](notes/BUUCTF_%E5%88%AE%E5%BC%80%E6%9C%89%E5%A5%96_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [123.c](123.c)
- [solve.py](solve.py)

```python
"""Solve the sorting, arithmetic and Base64 constraints from the local notes."""
from pathlib import Path
from base64 import b64decode, b64encode

sample = next(Path(__file__).parent.glob("*.exe"))
assert b"ak1w" in sample.read_bytes() and b"V1Ax" in sample.read_bytes()
ordered = sorted([90, 74, 83, 69, 67, 97, 78, 72, 51, 110, 103])
plain = bytes([ordered[0] + 34, ordered[4]]) + b64decode("V1Ax") + b64decode("ak1w")
assert len(plain) == 8
assert 4 * plain[2] - 141 == 3 * ordered[2]
assert plain[3] // 4 == 2 * (ordered[7] // 9)
assert b64encode(plain[2:5]) == b"V1Ax"
assert b64encode(plain[5:8]) == b"ak1w"
print(plain.decode("ascii"))
```
