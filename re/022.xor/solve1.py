"""Decode 33 ciphertext bytes; the trailing NUL in the original draft is a terminator."""
from pathlib import Path
encoded = bytes.fromhex("660a6b0c77264f2e4011780d5a3b55117019461f76224d23440e6706680f47324f")
assert encoded in Path(__file__).with_name("xor").read_bytes()
plain = bytes([encoded[0]]) + bytes(encoded[index] ^ encoded[index - 1] for index in range(1, len(encoded)))
forward = bytearray(plain)
for index in range(1, len(forward)):
    forward[index] ^= forward[index - 1]
assert bytes(forward) == encoded
print(plain.decode("ascii"))
