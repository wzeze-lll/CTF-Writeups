from pwn import*
io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
io.interactive()