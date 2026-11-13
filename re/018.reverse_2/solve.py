#!/usr/bin/env python3
"""Apply the i/r to 1 replacement used by reverse_2."""
from pathlib import Path

sample = Path(__file__).with_name("reverse_2").read_bytes()
plain = b"{hacking_for_fun}"
assert plain in sample
answer = plain.replace(b"i", b"1").replace(b"r", b"1")
print("flag" + answer.decode("ascii"))
