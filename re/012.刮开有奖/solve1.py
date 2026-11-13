"""Solve the sorting, arithmetic and Base64 constraints from the local notes."""
from pathlib import Path
from base64 import b64decode, b64encode

sample = next(Path(__file__).parent.glob("*.exe"))
assert b"ak1w" in sample.read_bytes() and b"V1Ax" in sample.read_bytes()
ordered = sorted([90, 74, 83, 69, 67, 97, 78, 72, 51, 110, 103])
plain = bytes([ordered[0] + 34, ordered[4]]) + b64decode("V1Ax") + b64decode("ak1w")
assert len(plain) == 8
assert 4 * plain[2] - 141 == 3 * ordered[2]
assert plain[3] // 4 == 2 * (ordered[7] // 9)
assert b64encode(plain[2:5]) == b"V1Ax"
assert b64encode(plain[5:8]) == b"ak1w"
print(plain.decode("ascii"))
