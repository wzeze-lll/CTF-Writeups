#!/usr/bin/env python3
"""Confirm the marker in the packed PE and print the documented flag."""
from pathlib import Path

sample = Path(__file__).with_name("新年快乐.exe").read_bytes()
assert b"HappyNewYear!" in sample and b"please input the true flag:" in sample
print("flag{HappyNewYear!}")
