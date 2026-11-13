#!/usr/bin/env python3
"""Extract the checked flag body from the supplied PE sample."""
from pathlib import Path
import re

sample = Path(__file__).with_name("easyre.exe").read_bytes()
matches = set(re.findall(rb"this_Is_a_EaSyRe", sample))
assert len(matches) == 1
print("flag{" + matches.pop().decode("ascii") + "}")
