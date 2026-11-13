"""Invert the case-dependent rotations in the supplied rome sample."""
from pathlib import Path
encoded = "Qsw3sj_lz4_Ujw@l"
sample = Path(__file__).with_name("rome.exe").read_bytes()
assert all(bytes([0xc6, 0x45, 0xe3 + index, value]) in sample
           for index, value in enumerate(encoded.encode()))
answer = []
for character in encoded:
    if "A" <= character <= "Z":
        character = chr((ord(character) - 65 - 14) % 26 + 65)
    elif "a" <= character <= "z":
        character = chr((ord(character) - 97 - 18) % 26 + 97)
    answer.append(character)
print("".join(answer))
