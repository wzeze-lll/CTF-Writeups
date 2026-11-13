# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

题型或原始题名尚待确认，保留附件原名。

## 文件

- [0d1ac4a5958003726e95e51f9821e3dfd14a27a85d8476bf6637889946b6e94b.exe](0d1ac4a5958003726e95e51f9821e3dfd14a27a85d8476bf6637889946b6e94b.exe)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

本地 PE 含 BJD 格式字符串，与 JustRE 对话框题解一致；补充脚本计算固定格式结果。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://bbs.huaweicloud.com/blogs/397532)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [solve.py](solve.py)

```python
"""Recover the local JustRE dialog format; the program itself is not executed."""
from pathlib import Path

sample = next(Path(__file__).parent.glob("*.exe"))
assert b"BJD{%d%d2069a45792d233ac}" in sample.read_bytes()
print("BJD{%d%d2069a45792d233ac}" % (19999, 0))
```
