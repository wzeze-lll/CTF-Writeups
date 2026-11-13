"""Reproduce the local luck_guy case 4 -> case 5 -> case 1 data path."""
from pathlib import Path

sample = Path(__file__).with_name("luck_guy").read_bytes()
assert b"GXY{do_not_" in sample
encoded = bytes.fromhex("69637567606f667f")
assert all(bytes([0xc6, 0x45, 0xd0 + index, value]) in sample
           for index, value in enumerate(encoded))
plain = bytes(value - (2 if index % 2 else 1) for index, value in enumerate(encoded))
print("GXY{do_not_" + plain.decode("ascii"))
