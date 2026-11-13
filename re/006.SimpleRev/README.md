# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

题型或原始题名尚待确认，保留附件原名。

## 文件

- [7f7222764a31e77bcc09c7f15f80230849e1d9075a1c0c1f5bb421a144652c25](7f7222764a31e77bcc09c7f15f80230849e1d9075a1c0c1f5bb421a144652c25)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

原哈希命名 ELF 的 main 调 Decry，符号包含 key1/key3；与 SimpleRev 的拼接和字符校验结构一致。原 2.py 已与 ELF 放在同一题目录。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/Mayfly-nymph/p/11511292.html)
- [个人已有笔记](notes/BUUCTF_SimpleRev_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [2.py](2.py)
- [solve.py](solve.py)

```python
"""Same inverse as the user's 2.py, with a forward check."""
text = "killshadow"
key = "adsfkndcls"
answer = []
for index, expected in enumerate(text):
    matches = [value for value in range(ord("A"), ord("z") + 1)
               if (value - 39 - ord(key[index % len(key)]) + 97) % 26 + 97 == ord(expected)]
    assert matches
    answer.append(matches[0])
forward = "".join(chr((value - 39 - ord(key[index % len(key)]) + 97) % 26 + 97)
                  for index, value in enumerate(answer))
assert forward == text
print(bytes(answer).decode("ascii"))
```
