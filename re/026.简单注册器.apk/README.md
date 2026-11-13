# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [简单注册器.apk](%E7%AE%80%E5%8D%95%E6%B3%A8%E5%86%8C%E5%99%A8.apk)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

2.c 的常量及四处字符赋值与本地 MainActivity 一致。输出的 flag 与进入该分支所需注册码是不同字符串。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/shell233/p/16554232.html)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [2.c](2.c)
- [MainActivity.decompiled.java](MainActivity.decompiled.java)
- [solve.py](solve.py)

```python
"""Reproduce the output branch in MainActivity; registration input is separate."""
x = list(map(ord, "dd2940c04462b4dd7c450528835cca15"))
x[2] = x[2] + x[3] - 50
x[4] = x[2] + x[5] - 48
x[30] = x[31] + x[9] - 48
x[14] = x[27] + x[28] - 97
for index in range(16):
    x[index], x[31 - index] = x[31 - index], x[index]
print("flag{" + "".join(map(chr, x)) + "}")
```
