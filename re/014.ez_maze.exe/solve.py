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
