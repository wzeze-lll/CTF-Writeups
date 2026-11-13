# 知识点

Algorithms

# 题目分析

分类：Reverse / Algorithms。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [2.py](2.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [2.py](2.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
text = 'killshadow'
key = 'adsfkndcls'
flag = ''
v5 = len(key)
for i in range(10):   #输入十次字符，所以循环十次
    for j in range(ord('A'), ord('z')+1):  #将所有字母进行尝试，寻找可以使if判断成功的字符
        str2 = (j -39 - ord(key[i % v5]) +97) % 26 + 97 #将原本的加密直接照搬过来，这里需要ord(key[i % v5])是因为python不能直接将字符串转成ascii码
        if chr(str2) == text[i]:  #将算出来的ascii码chr()转成ascii码与text内容比较
            flag += chr(j)    
            break   #这里的break作用是如果if判断成功了一次就结束这个内层循环，开始第二个外层循环，如果没有break会输出很多满足条件的别的字符
print(flag)
```
