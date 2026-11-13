#!/usr/bin/env python3
"""Recover the flag prefix from the local PE string."""
from pathlib import Path
import re

sample = Path(__file__).with_name("c809d6f2590b8f72c2191c7fd222c7529af451a813bbf067c0fc2c1ed675e879.exe").read_bytes()
matches = re.findall(rb"DBAPP\{[0-9a-f]{32}\}", sample)
assert len(matches) == 1
print(matches[0].replace(b"DBAPP", b"flag").decode("ascii"))
