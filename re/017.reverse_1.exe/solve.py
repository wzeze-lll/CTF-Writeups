#!/usr/bin/env python3
"""Apply the character replacement used by reverse_1."""
from pathlib import Path

sample = Path(__file__).with_name("reverse_1.exe").read_bytes()
plain = b"{hello_world}"
assert plain in sample
answer = plain.replace(b"o", b"0")
print("flag" + answer.decode("ascii"))
