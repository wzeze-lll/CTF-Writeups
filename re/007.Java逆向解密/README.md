# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [Reverse.class](Reverse.class)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

本地 Reverse.class 反编译确认前向表达式为 (c + 64) ^ 32。原 1.c 的 key[i]^0x20-64 实际解析成 key[i]^(0x20-64)，且 char 存储存在符号问题。原稿保留，推荐 solve.c 或 solve.py；3.py 也给出了正确逆运算。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/Tsuiyields/p/13864314.html)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [1.c](1.c)
- [3.py](3.py)
- [Reverse.decompiled.java](Reverse.decompiled.java)
- [solve.c](solve.c)
- [solve.py](solve.py)

```python
"""Inverse of (character + 64) XOR 32, verified against Reverse.class."""
key = [180, 136, 137, 147, 191, 137, 147, 191, 148, 136, 133, 191, 134, 140, 129, 135, 191, 65]
plain = bytes((value ^ 32) - 64 for value in key)
assert [(value + 64) ^ 32 for value in plain] == key
print(plain.decode("ascii"))
```
