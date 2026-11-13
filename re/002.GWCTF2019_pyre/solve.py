"""Invert the add-index and adjacent-XOR stages from the local pyre bytecode notes."""
code = bytes([31, 18, 29, 40, 48, 52, 1, 6, 20, 52, 44, 27, 85, 63, 111, 54, 42, 58, 1, 68, 59, 37, 19])
values = list(code)
for index in range(len(values) - 2, -1, -1):
    values[index] ^= values[index + 1]
plain = bytes((value - index) % 128 for index, value in enumerate(values))
forward = [(value + index) % 128 for index, value in enumerate(plain)]
for index in range(len(forward) - 1):
    forward[index] ^= forward[index + 1]
assert bytes(forward) == code
print(plain.decode("ascii"))
