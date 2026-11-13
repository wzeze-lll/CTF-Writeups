#!/usr/bin/env python3
"""Decode the alternating substitution in the supplied Youngter-drive PE."""
from pathlib import Path

sample = Path(__file__).with_name("Youngter-drive.exe").read_bytes()
cipher = "TOiZiZtOrYaToUwPnToBsOaOapsyS"
key = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
assert b"PnToBsOapsyS" in sample and b"QWERTY" in sample and b"UIOPASDFGHJKLZXCVBNM" in sample
plain = list(cipher)
for index in range(27, 0, -2):
    key_index = key.index(plain[index])
    plain[index] = chr(key_index + 38 if 65 <= key_index + 38 <= 90 else key_index + 96)
body = "".join(plain) + "E"  # challenge's expected final character
assert body == "ThisisthreadofwindowshahaIsESE"
print(f"flag{{{body}}}")
