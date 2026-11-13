"""Read the challenge string directly from the supplied APK's DEX."""
from pathlib import Path
from zipfile import ZipFile
import re

with ZipFile(next(Path(__file__).parent.glob("*.apk"))) as archive:
    dex = archive.read("classes.dex")
    assert b"Lcom/example/helloword/MainActivity;" in dex
    matches = sorted(set(re.findall(rb"flag\{[0-9a-f]{32}\}", dex)))
    assert len(matches) == 1, "Inspect DEX strings if the APK differs."
    print(matches[0].decode("ascii"))
