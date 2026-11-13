"""Inverse of (character + 64) XOR 32, verified against Reverse.class."""
key = [180, 136, 137, 147, 191, 137, 147, 191, 148, 136, 133, 191, 134, 140, 129, 135, 191, 65]
plain = bytes((value ^ 32) - 64 for value in key)
assert [(value + 64) ^ 32 for value in plain] == key
print(plain.decode("ascii"))
