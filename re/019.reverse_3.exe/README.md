# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [reverse_3.exe](reverse_3.exe)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

原 exp.py 的常量与本地 reverse_3.exe 完全匹配，已合并进该题。solve.py 另加 Base64 严格解码和正向回验。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/hopein/p/16938005.html)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [exp.py](exp.py)
- [solve.py](solve.py)

```python
"""Undo the index addition before standard Base64 decoding."""
from pathlib import Path
import base64

encoded = "e3nifIH9b_C@n@dH"
assert encoded.encode() in Path(__file__).with_name("reverse_3.exe").read_bytes()
intermediate = bytes(ord(character) - index for index, character in enumerate(encoded))
plain = base64.b64decode(intermediate, validate=True)
assert bytes(value + index for index, value in enumerate(base64.b64encode(plain))) == encoded.encode()
print(plain.decode("ascii"))
```
