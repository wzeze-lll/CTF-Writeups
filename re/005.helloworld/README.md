# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

题型或原始题名尚待确认，保留附件原名。

## 文件

- [7ea2fc42d5bf465ce996d7dc5a6260a03038089a06fe7ce56695539fabc926f2.apk](7ea2fc42d5bf465ce996d7dc5a6260a03038089a06fe7ce56695539fabc926f2.apk)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

## 代码配对与核对

本地 DEX 的 com.example.helloword.MainActivity 和唯一 flag 字符串对应 helloworld；脚本直接从附件读取。

参考资料用于核对题名与思路；下面脚本根据本地代码和附件整理。静态求解或代数回验不等于原程序动态通关。

- [公开题解](https://archive.next.arttnba3.cn/2020/10/09/【CTF题解-0x06】BUUCTF-Reverse-write-up-by-arttnb3/)

# EXP

推荐 Python 3 求解：

```bash
python3 solve.py
```

- [solve.py](solve.py)

```python
"""Read the challenge string directly from the supplied APK's DEX."""
from pathlib import Path
from zipfile import ZipFile
import re

with ZipFile(next(Path(__file__).parent.glob("*.apk"))) as archive:
    dex = archive.read("classes.dex")
    assert b"Lcom/example/helloword/MainActivity;" in dex
    matches = sorted(set(re.findall(rb"flag\{[0-9a-f]{32}\}", dex)))
    assert len(matches) == 1, "Inspect DEX strings if the APK differs."
    print(matches[0].decode("ascii"))
```
