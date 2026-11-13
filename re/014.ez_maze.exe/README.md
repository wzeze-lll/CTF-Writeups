# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ez_maze.exe](ez_maze.exe)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

本地二进制的迷宫字符串实际为 225 格，即 15×15。网上正文写了 210，但其展示的地图有 15 行。脚本按附件实际长度校验原 111.py 中的路径。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://blog.hxzzz.asia/archives/232/)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [111.py](111.py)
- [solve.py](solve.py)

```python
"""Validate the user's path against the maze embedded in this PE, then hash it."""
from pathlib import Path
import hashlib
import re

sample = Path(__file__).with_name("ez_maze.exe")
maze = max(re.findall(rb"[x$&y]{100,}", sample.read_bytes()), key=len)
width = 15
assert len(maze) % width == 0
path = "sssssssddddwwwddsssssssdddsssddddd"
row, column = divmod(maze.index(b"x"), width)
for step in path:
    delta_row, delta_column = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}[step]
    row += delta_row
    column += delta_column
    assert 0 <= row < len(maze) // width and 0 <= column < width
    assert maze[row * width + column] != ord("$")
assert maze[row * width + column] == ord("y")
print("BaseCTF{" + hashlib.md5(path.encode()).hexdigest() + "}")
```
