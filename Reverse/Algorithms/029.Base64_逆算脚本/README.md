# 知识点

Algorithms

# 题目分析

分类：Reverse / Algorithms。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [exp.py](exp.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [exp.py](exp.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
import base64
sum = "e3nifIH9b_C@n@dH"
flag = ""
l=len(sum)
for i in range(0,l):
    flag +=chr(ord(sum[i]) - i)
print(base64.b64decode(flag))
```
