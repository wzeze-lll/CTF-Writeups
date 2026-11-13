#!/usr/bin/env python3
"""usage:
    python3 check.py "i0,i1,...;j0,j1,...;k0,k1,..."
    python3 check.py answer.txt
"""
import hashlib
import sys
from pathlib import Path

V = "cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    try:
        text = src.read_text() if src.exists() else sys.argv[1]
    except OSError:          # inline answer string too long for a filename
        text = sys.argv[1]
    try:
        canon = ";".join(",".join(str(int(v)) for v in s.split(","))
                         for s in text.strip().split(";"))
    except Exception:
        sys.exit("[-] wrong")
    body = hashlib.sha256(canon.encode()).hexdigest()[:32]
    if hashlib.sha256(("ns::" + body).encode()).hexdigest() == V:
        print(f"[+] correct! flag = flag{{{body}}}")
    else:
        sys.exit("[-] wrong")


if __name__ == "__main__":
    main()
