---
tags: [re, reverse, 字节序, 字符串变换, ascii, BUUCTF, 学习版]
created: 2026-11-06
updated: 2026-11-06
learning_level: L1；静态路线与脚本自检已完成，原始附件未在本地动态验证
---

# BUUCTF SimpleRev：字节序、字符串比较与逐字符逆算

> [!warning] 证据边界
> 本页依据用户提供的伪代码和公开题解整理。材料中一处写“Linux 64 位”，另一处用 PE 查壳工具，二者互相矛盾；因此**不把平台或保护结论当作已证实事实**。拿到附件后先执行 `file ./SimpleRev`，再按实际格式选择工具。

## 一句话

SimpleRev 的核心不是“看到加密就爆破”，而是从最后的 `strcmp(text, str2)` 倒推：

```text
输入字符 v1
    ↓ 逐字符变换（使用循环 key）
str2
    ↓ strcmp
text = "killshadow"
```

只要还原 `text` 与 `key`，再把变换反过来，就能构造会生成 `killshadow` 的输入。

> [!abstract] 推荐阅读顺序
> 1. 先看最终 `strcmp`，确定真正目标是谁。
> 2. 再看 `join / strcpy / strcat`，还原 `text` 和 `key`。
> 3. 最后处理每个输入字节的变换，并用脚本重新加密验证。
>
> 这题的“大小端”只出现在**把整数常量读回字符**时；逐字符公式本身是 ASCII 与模 26 运算。

## 1. 从最终比较开始

伪代码的关键是：

```c
if (!strcmp(text, str2))
    puts("Congratulation!");
else
    puts("Try again!");
```

`strcmp(a, b) == 0` 的意思是两个以 `\0` 结尾的字符串相同。因此本题的目标不是直接猜 flag，而是让程序计算出的 `str2` 与 `text` 完全相同。

> [!tip] 逆向第一反应
> 在 IDA 中先找 `strcmp`、`memcmp`、`strncmp` 这类最终比较；再从它们的两个参数向上追踪。这样通常比从 `main` 第一行顺读更快。

## 2. 还原目标字符串 `text`

用户提供的逻辑为：

```c
text = join(key3, &v9);
```

已知静态记录中：

```text
key3 → "kills"
v9   → 内存字节顺序对应 "hadow"
join(key3, v9) → "killshadow"
```

所以最终比较目标是：

```python
text = 'killshadow'
```

### 不是“IDA 显示大端”，而是如何看字节

例如一个 64 位整数在反编译器里显示为一个十六进制数字，但 x86-64 内存按小端序存储：低字节在低地址。想把常量当字符串看，优先做下面任一个：

```text
IDA：选中常量后用 R 转字符；或跳到内存查看字节
GDB：x/8bx 地址          # 一字节一字节看
GDB：x/s 地址            # 当作 NUL 结尾字符串看
Python：value.to_bytes(8, 'little')
```

不要机械地“看见整数就反转字符”。先看内存中的实际字节，再决定字符串方向。

## 3. 还原循环 key

伪代码的构造关系：

```c
strcpy(key, key1);
strcat(key, src);

for (i = 0; i < strlen(key); ++i)
    if ('A' <= key[i] && key[i] <= 'Z')
        key[i] += 32;
```

静态记录给出的字符为：

```text
key1 = "ADSFK"
src  = "NDCLS"
拼接 = "ADSFKNDCLS"
转小写 = "adsfkndcls"
```

因此：

```python
key = 'adsfkndcls'
```

> [!note] `v3` 为什么从 10 开始也没关系
> 原逻辑先用 `v3` 遍历 10 个 key 字符，后面的输入变换继续使用 `key[v3++ % v5]`。因为 `10 % 10 == 0`，第一个输入字符仍使用 `key[0]`。脚本里直接从 `i = 0` 开始取 `key[i % len(key)]`，效果等价。

## 4. 输入字符怎样变成 `str2`

对非空格输入，关键公式可写成：

```c
str2[pos] = (input - 39 - key[key_pos % key_len] + 97) % 26 + 97;
```

人话：程序取一个输入字母和当前 key 字符做运算，结果总是落在小写字母 `a`～`z`；然后和 `killshadow` 的对应位置比较。

### 输入分支要注意

| 输入 | 程序行为（按用户提供伪代码） | 对做题的影响 |
|---|---|---|
| `A`～`Z` | 执行变换，key 下标前进 | 可作为本题的规范输入范围 |
| `a`～`z` | 也执行相同变换 | 可能有等价小写输入；公开脚本通常固定选大写 |
| 空格 | 只移动输出位置，不前进 key | 会让 `str2` 出现空洞，通常不适合此题 |
| 其他字符 | 伪代码显示可能不写 `str2` 但仍移动位置 | 先不要拿它们做爆破范围 |

## 5. 两种可读脚本

### 写法 A：逐个尝试大写字母

最适合刚开始写 RE 脚本时核对伪代码：

```python
import string

text = 'killshadow'
key = 'adsfkndcls'

def encrypt_one(ch, key_ch):
    return chr((ord(ch) - 39 - ord(key_ch) + 97) % 26 + 97)

flag = ''
for i, want in enumerate(text):
    for ch in string.ascii_uppercase:
        if encrypt_one(ch, key[i % len(key)]) == want:
            flag += ch
            break
    else:
        raise ValueError(f'第 {i} 位没有找到大写输入')

print(flag)  # KLDQCUDFZO
assert ''.join(encrypt_one(ch, key[i % len(key)]) for i, ch in enumerate(flag)) == text
```

为什么这比 `range(ord('A'), ord('z') + 1)` 更好：`string.ascii_uppercase` 只包含 `A`～`Z`，不会把 `Z` 与 `a` 之间的标点误纳入尝试范围。

### 写法 B：直接求逆

对“规范输入是大写字母”的前提，令输入为 `A + r`，可从原式得到：

```text
r = (目标字符 - 'a' - 19 + 当前 key 的 ASCII 值) mod 26
输入 = 'A' + r
```

```python
text = 'killshadow'
key = 'adsfkndcls'

flag = ''.join(
    chr(ord('A') + (ord(want) - ord('a') - 19 + ord(key[i % len(key)]) ) % 26)
    for i, want in enumerate(text)
)

print(flag)  # KLDQCUDFZO
```

> [!important] 脚本验证结果
> 两种脚本均得到 `KLDQCUDFZO`；再把它逐字符送回原变换，会重新得到 `killshadow`。这证明的是**给定伪代码、text 和 key 的数学关系自洽**，不等于原始二进制已经在本地运行验证。

## 6. 在 IDA / GDB 中怎么验证

| 目标 | 推荐操作 | 正确时应看到什么 |
|---|---|---|
| 确认程序格式 | `file ./SimpleRev` | ELF 或 PE 的真实架构，而不是从博客猜 |
| 找成功条件 | Strings → `Congratulation` → Xref；或搜 `strcmp` | 比较点与两个字符串来源 |
| 看整数对应字节 | IDA 内存窗口 / GDB `x/8bx 地址` | 小端内存排列，不凭整数书写顺序猜 |
| 看 `text` | `x/s text地址` | `killshadow` 或当前样本的真实目标 |
| 看 key 转换后结果 | 在循环后断下，`x/s key地址` | `adsfkndcls` 或当前样本实际 key |
| 验证输入变换 | 在 `str2[pos]` 写入后断下，`x/16bx str2地址` | 对应位置逐步变为目标字节 |

## 7. 常见错误

| 容易写错 | 正确理解 |
|---|---|
| “IDA 把字符串显示成大端了” | IDA 展示的是整数；字节序要看内存 |
| 所有整数常量都要反转 | 只有把整数按字符解释时才查看 little-endian 字节顺序 |
| 看到 `% 26` 就直接照抄爆破 | 先明确输入范围、输出字母范围和 key 下标 |
| `v3 = 10` 表示 key 从第 10 位开始 | 有 `% 10`，所以实际从 `key[0]` 开始 |
| `strcmp` 是比较地址 | 它比较两个字符串内容；返回 0 才相同 |

## 8. 关联笔记与参考

- `基础运算与XOR逆算`：`ord()`、`chr()`、字节数组与逐字节验证。
- `常见加密算法识别与还原`：区分编码、简单变换和真正加密。
- `RE导航`：从字符串、Xref 到比较点的通用流程。
- `RE动态调试与GDB速查`：在写入 `str2` 后观察寄存器和内存。
- [原始公开题解（Afanbird）](https://blog.csdn.net/afanzcf/article/details/118788007)：对照其伪代码与常量解释；以手上附件为准。

## 9. 自测与 48 小时变式

不看本页，完成下面两件事：

1. 解释为什么 `v3` 已经是 10，第一轮输入仍使用 `key[0]`。
2. 把 `text` 改成任意 10 个小写字符、key 改成任意 10 个小写字符，使用写法 A 生成一组大写输入，再用 `assert` 重新加密验证。

通过标准：你能从一个新的 `strcmp(target, output)` 伪代码中独立找出 target、key、输入范围和下标推进规则；动态跑通附件后再更新本页等级。
