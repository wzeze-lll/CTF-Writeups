"""Recover the local JustRE dialog format; the program itself is not executed."""
from pathlib import Path

sample = next(Path(__file__).parent.glob("*.exe"))
assert b"BJD{%d%d2069a45792d233ac}" in sample.read_bytes()
print("BJD{%d%d2069a45792d233ac}" % (19999, 0))
