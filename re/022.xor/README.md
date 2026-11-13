# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [1.py](1.py)
- [xor](xor)

## 已有分析

- [BUUCTF_xor_WP.md](notes/BUUCTF_xor_WP.md)
- [GWCTF2019_xxor_WP.md](notes/GWCTF2019_xxor_WP.md)


### BUUCTF xor WP

> [!info] 题目信息
> - 平台：[BUUCTF](https://buuoj.cn/challenges#xor)（需登录，按题名搜索）
> - 类型：RE / 基础 XOR
> - 难度：入门
> - 证据状态：`STATIC_ONLY + SCRIPT_VERIFIED`。依据公开题解结构与题面描述整理；解密脚本用公开密文在本地跑通并得到 flag，未持有原附件，未在 IDA 中复核偏移。

#### 一句话

程序对缓冲区做**就地**逐字节 XOR：`buf[i] ^= buf[i-1]`。因为写到同一块内存，后一项用的是**已经变成密文的前一项**，所以逆算是 `p[i] = c[i] ^ c[i-1]`，不是 `c[i] ^ p[i-1]`。

#### 已知数据

```text
密文（hex）:
66 0a 6b 0c 77 26 4f 2e 40 11 78 0d 5a 3b 55 11
70 19 46 1f 76 22 4d 23 44 0e 67 06 68 0f 47 32 4f
```

长度 33 字节。首字节 `0x66 = 'f'` 没有被前项 XOR，保持不变——这本身就是 flag 开头 `f` 的提示。

#### 程序逻辑（还原）

```c
char buf[33] = {...};          // 输入或内置密文
for (int i = 1; i < 33; i++) {
    buf[i] ^= buf[i - 1];      // 就地修改
}
```

关键点：

```text
c[0] = p[0]
c[1] = p[1] ^ c[0]      ← 不是 p[0]！
c[2] = p[2] ^ c[1]
...
```

所以：

```text
p[0] = c[0]
p[i] = c[i] ^ c[i - 1]
```

> [!warning] 最容易错的地方
> 如果按 `p[i] = c[i] ^ p[i-1]` 逆算，第一字节之后就会开始错，输出类似 `fl\x07\x0b...` 的乱码。看到“第一字节对、后面全错”，先检查是不是就地链式 XOR。

#### 解密脚本

```python
"""Decode 33 ciphertext bytes; the trailing NUL in original 1.py is a terminator."""
from pathlib import Path
encoded = bytes.fromhex("660a6b0c77264f2e4011780d5a3b55117019461f76224d23440e6706680f47324f")
assert encoded in Path(__file__).with_name("xor").read_bytes()
plain = bytes([encoded[0]]) + bytes(encoded[index] ^ encoded[index - 1] for index in range(1, len(encoded)))
forward = bytearray(plain)
for index in range(1, len(forward)):
    forward[index] ^= forward[index - 1]
assert bytes(forward) == encoded
print(plain.decode("ascii"))
```
