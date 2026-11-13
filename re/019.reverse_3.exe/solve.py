"""Undo the index addition before standard Base64 decoding."""
from pathlib import Path
import base64

encoded = "e3nifIH9b_C@n@dH"
assert encoded.encode() in Path(__file__).with_name("reverse_3.exe").read_bytes()
intermediate = bytes(ord(character) - index for index, character in enumerate(encoded))
plain = base64.b64decode(intermediate, validate=True)
assert bytes(value + index for index, value in enumerate(base64.b64encode(plain))) == encoded.encode()
print(plain.decode("ascii"))
