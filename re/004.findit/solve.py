"""Reproduce the two loops from the local findit MainActivity decompilation."""
from pathlib import Path
from zipfile import ZipFile

sample = next(Path(__file__).parent.glob("*.apk"))
with ZipFile(sample) as archive:
    assert b"Lcom/example/findit/MainActivity;" in archive.read("classes.dex")

def transform_password(text):
    output = []
    for character in text:
        value = ord(character)
        if "A" <= character < "I" or "a" <= character < "i":
            value += 18
        elif "A" <= character <= "Z" or "a" <= character <= "z":
            value -= 8
        output.append(chr(value))
    return "".join(output)

def transform_message(text):
    output = []
    for character in text:
        value = ord(character)
        if "A" <= character <= "Z" or "a" <= character <= "z":
            value += 16
            if ord("Z") < value < ord("a") or value >= ord("z"):
                value -= 26
        output.append(chr(value))
    return "".join(output)

print("password:", transform_password("ThisIsTheFlagHome"))
print(transform_message("pvkq{m164675262033l4m49lnp7p9mnk28k75}"))
