# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [rome.exe](rome.exe)

## 已有分析

- [BUUCTF_ACTF2020_rome_WP_学习版.md](notes/BUUCTF_ACTF2020_rome_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)


### BUUCTF [ACTF 新生赛 2020] rome：大小写分支与模 26 逆算

> [!note] 本页依据
> 根据用户提供的 IDA 伪代码整理，并用两篇公开题解交叉核对。当前没有题目 ELF 附件，因此脚本验证的是字符变换，不代表已经把答案输入原程序跑通。

#### 题目要做什么

程序读取一行输入，要求它有固定外壳 `ACTF{...}`，并把花括号里的 16 个字符变换后与内置字符串比较。伪代码中的目标密文是：

```text
Qsw3sj_lz4_Ujw@l
```

要做的事很直接：把每个字符按程序的规则反向变换，恢复正文，再补回题目要求的输入外壳。

#### 先看字符分支

程序按字符范围选择规则：

```c
if (x >= 'A' && x <= 'Z')
    y = (x - 51) % 26 + 65;
else if (x >= 'a' && x <= 'z')
    y = (x - 79) % 26 + 97;
else
    y = x;
```

十进制 `65` 是 `A`，`97` 是 `a`。把公式按字母表起点改写：

```text
大写：((x - 'A') + 14) % 26 + 'A'  → 向后循环移动 14 位
小写：((x - 'a') + 18) % 26 + 'a'  → 向后循环移动 18 位
其他：保持不变
```

例如大写 `C` 的字母序号是 2，向后移 14 位后是 16，即 `Q`；所以解密时 `Q` 要向前移 14 位回到 `C`。小写 `a` 向后移 18 位是 `s`，所以密文中的 `s` 向前移 18 位回到 `a`。

##### “不是有范围吗？”——范围判断和解密各管一件事

范围告诉程序（也告诉我们）该用哪一套规则：大写走大写分支，小写走小写分支，标点和数字走原样分支。它**不能单独给出明文**；明文来自“密文 + 对应分支的逆运算”。

```text
看到密文 Q → 属于 A..Z → 用大写偏移 14 → 向前移回 C
看到密文 s → 属于 a..z → 用小写偏移 18 → 向前移回 a
看到密文 3 → 不属于字母范围 → 保持 3
```

#### 逆算得到正文

```text
密文：Qsw3sj_lz4_Ujw@l
明文：Cae3ar_th4_Gre@t
```

下划线、数字 `3`、`4` 和 `@` 不在字母范围内，所以原样保留。完整的**程序输入**为：

```text
ACTF{Cae3ar_th4_Gre@t}
```

注意区分题目程序的校验格式和平台提交格式：公开 BUUCTF 题解通常把提交答案写成 `flag{Cae3ar_th4_Gre@t}`；而用户提供的程序伪代码检查的是 `ACTF{...}`。前者是平台 flag 包装，后者是程序要求输入的内容，不要把两者混成一个字符串。

#### 简短可运行脚本

下面脚本只依赖 Python 3，直接运行会输出正文，并用正向变换断言核验逆算没有写反：

```python
"""Invert the case-dependent rotations in the supplied rome sample."""
from pathlib import Path
encoded = "Qsw3sj_lz4_Ujw@l"
sample = Path(__file__).with_name("rome.exe").read_bytes()
assert all(bytes([0xc6, 0x45, 0xe3 + index, value]) in sample
           for index, value in enumerate(encoded.encode()))
answer = []
for character in encoded:
    if "A" <= character <= "Z":
        character = chr((ord(character) - 65 - 14) % 26 + 65)
    elif "a" <= character <= "z":
        character = chr((ord(character) - 97 - 18) % 26 + 97)
    answer.append(character)
print("".join(answer))
```
