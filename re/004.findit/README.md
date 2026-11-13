# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [6a428ff2-25d7-403c-b28e-3f980a10a5a2.apk](6a428ff2-25d7-403c-b28e-3f980a10a5a2.apk)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

JADX 对本地 APK 的 MainActivity 反编译得到两个字符变换循环；solve.py 复现注册码与显示文本。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://www.cnblogs.com/Dav-ove3/p/17244088.html)
- [个人已有笔记](notes/BUUCTF_findit_Android_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [MainActivity.decompiled.java](MainActivity.decompiled.java)
- [solve.py](solve.py)

```python
"""Reproduce the two loops from the local findit MainActivity decompilation."""
from pathlib import Path
from zipfile import ZipFile

sample = next(Path(__file__).parent.glob("*.apk"))
with ZipFile(sample) as archive:
    assert b"Lcom/example/findit/MainActivity;" in archive.read("classes.dex")

def transform_password(text):
    output = []
    for character in text:
        value = ord(character)
        if "A" <= character < "I" or "a" <= character < "i":
            value += 18
        elif "A" <= character <= "Z" or "a" <= character <= "z":
            value -= 8
        output.append(chr(value))
    return "".join(output)

def transform_message(text):
    output = []
    for character in text:
        value = ord(character)
        if "A" <= character <= "Z" or "a" <= character <= "z":
            value += 16
            if ord("Z") < value < ord("a") or value >= ord("z"):
                value -= 26
        output.append(chr(value))
    return "".join(output)

print("password:", transform_password("ThisIsTheFlagHome"))
print(transform_message("pvkq{m164675262033l4m49lnp7p9mnk28k75}"))
```
