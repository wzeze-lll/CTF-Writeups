# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

题型或原始题名尚待确认，保留附件原名。

## 文件

- [333.py](333.py)
- [398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5.pyc](398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5.pyc)
- [398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py](398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py)
- [recovered.py](recovered.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [333.py](333.py)
- [recovered.py](recovered.py)
- [398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py](398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5_decompiled.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python

code = [
    '\x1f', '\x12', '\x1d', '(', '0', '4',
    '\x01', '\x06', '\x14', '4', ',', '\x1b',
    'U', '?', 'o', '6', '*', ':',
    '\x01', 'D', ';', '%', '\x13'
]

l = len(code)

# 第一步：逆向 XOR
for i in range(l - 2, -1, -1):
    a = ord(code[i])
    b = ord(code[i + 1])

    value = a ^ b
    code[i] = chr(value)

# 第二步：撤销加下标
flag = ""

for i in range(l):
    a = ord(code[i])
    value = (a - i) % 128
    flag += chr(value)

print(flag)
```
