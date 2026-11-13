"""Decode the same bytes as draft_incorrect.c: XOR with 0x20, then subtract 64."""

key = (
    180, 136, 137, 147, 191, 137, 147, 191, 148, 136,
    133, 191, 134, 140, 129, 135, 191, 65,
)

decoded = bytes((value ^ 0x20) - 64 for value in key)
print(decoded.decode("ascii"))
