---
tags: [逆向, RE, WP, 排序, Base64, 字符约束]
created: 2026-11-12
updated: 2026-11-12
evidence: STATIC_ONLY
掌握等级: L1（材料覆盖；未在原附件动态验证）
---

# BUUCTF「刮开有奖」：排序、Base64 与字符约束

> [!note] 依据与状态
> 本页依据用户提供的 IDA 伪代码，并对照公开题解整理。原题是 32 位 Windows 对话框程序；原笔记编写时缺少本地附件；现已在本仓库中配对 PE 附件，因此 Python 脚本只验证静态推导出的字符串关系，不代表已经在原程序中点击验证。

## 先看程序让我们输入什么

对话框从输入框取字符串，先检查长度为 8。程序没有要求输入 `flag{}` 外壳；需要填入的 8 个字符是：

```text
UJWP1jMp
```

提交平台时写成：

```text
flag{UJWP1jMp}
```

最容易迷路的原因是 IDA 把一串相邻的栈变量拆成 `v7`、`v8`……等名字；正确做法是沿着数据流看初始化值、排序后的数据、输入字符的使用位置和最后的比较条件。

## 第一层：11 个数字其实是 ASCII 字符

程序初始化了 11 个数：

```text
90, 74, 83, 69, 67, 97, 78, 72, 51, 110, 103
```

按 ASCII 表解释就是：

```text
90 74 83 69 67 97 78 72 51 110 103
 Z  J  S  E  C  a  N  H  3   n   g
```

`sub_4010F0(array, 0, 10)` 对下标 `0..10` 的内容做递归分区和交换。它的整体效果是按字符编码从小到大排序，不是把字符加密成另一种字符：

```text
排序前：ZJSECaNH3ng
排序后：3CEHJNSZagn
下标：  01234567890
```

快速排序可以用一个生活例子理解：选一个数当基准，把较小的放左边、较大的放右边，再分别处理左右两堆。函数内部的左右下标和交换看起来复杂，但先认出“分区 + 递归”后，可以用小脚本把固定输入跑一遍，检查排序结果。

### IDA 里的 `+ 4*i` 是什么

32 位伪代码可能出现：

```c
*(_DWORD *)(base + 4 * i)
```

`_DWORD` 是 4 字节，数组第 `i` 个 DWORD 的地址是：

```text
元素地址 = 数组首地址 + i × 4
```

所以 `4*i` 是元素宽度造成的步长。若把数据按 `char *` 处理，每个元素 1 字节，等价写法是 `((char *)base)[i]`，这时不再乘 4。**只有确认元素宽度后才能改写寻址表达式**；若数组确实是 `int[]`，不能随手删掉 `4*i`。

本题的 ASCII 值都小于 128。作为 32 位整数排序，和按其低字节对应的字符做排序，比较顺序相同；但在复现代码中仍要明确自己用的是 `int[]` 还是 `char[]`，不要让类型转换掩盖内存步长。

## 第二层：前两位由排序结果直接算出

题目条件可读成下面几条。这里把排序后的数组记为 `a`：

```text
a = "3CEHJNSZagn"

input[0] = a[0] + 34
input[1] = a[4]
4 * input[2] - 141 = 3 * a[2]
input[3] / 4 = 2 * (a[7] / 9)
```

代入：

1. `a[0]` 是 `'3'`，ASCII 值 51，所以 `input[0] = 51 + 34 = 85`，即 `'U'`。
2. `a[4]` 是 `'J'`，所以 `input[1] = 'J'`。
3. `a[2]` 是 `'E'`，ASCII 值 69，所以 `input[2] = (3×69+141)/4 = 87`，即 `'W'`。
4. `a[7]` 是 `'Z'`，ASCII 值 90，右侧为 `2×(90/9)=20`。C 的整数除法会向零截断，因此这一条单独只能推出 `input[3]` 在 80 到 83 之间，即 `P/Q/R/S`，**不能单独断定它就是 `P`**。下一层 Base64 条件会把它确定为 `P`。

## 第三层：两段 Base64 确定剩下六位

程序把输入切成两组、每组三个字符，再做 Base64 编码：

```text
input[2:5] → 编码后必须是 "V1Ax"
input[5:8] → 编码后必须是 "ak1w"
```

Base64 是编码，不是加密。对这两个已知编码直接解码：

```text
"V1Ax" → "WP1"
"ak1w" → "jMp"
```

因此：

```text
input[2:5] = WP1
input[5:8] = jMp
```

这也补上上一节的歧义：`input[3]` 必须是 `P`，因为第三到第五位整体解码结果是 `WP1`。拼起来得到 `UJWP1jMp`。

题目中的 Base64 字符表是标准表 `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=`。若别的题出现自定义字符表，应先提取表，再判断能否直接使用 Python `base64` 模块。

## 可直接运行的 Python 验算脚本

```python
import base64

seed = b"ZJSECaNH3ng"
ordered = bytes(sorted(seed))
assert ordered == b"3CEHJNSZagn"

part_2_4 = base64.b64decode(b"V1Ax", validate=True)
part_5_7 = base64.b64decode(b"ak1w", validate=True)

first = bytes((ordered[0] + 34, ordered[4]))
answer = first + part_2_4 + part_5_7

# 把伪代码里的算式重新检查一遍。
assert 4 * answer[2] - 141 == 3 * ordered[2]
assert answer[3] // 4 == 2 * (ordered[7] // 9)
assert base64.b64encode(answer[2:5]) == b"V1Ax"
assert base64.b64encode(answer[5:8]) == b"ak1w"
assert answer == b"UJWP1jMp"

print(answer.decode("ascii"))
print(f"flag{{{answer.decode('ascii')}}}")
```

运行结果：

```text
UJWP1jMp
flag{UJWP1jMp}
```

这里用 Python 的 `sorted()` 表达“按 ASCII 值升序排列”这个已确认的功能，便于初学时看懂。若要研究题目原始的快速排序实现，再按 IDA 伪代码逐句还原，并和此处结果 `3CEHJNSZagn` 对照。

## 这题的整体路线

```text
识别长度检查：输入是 8 字符
        ↓
提取固定数组：ZJSECaNH3ng
        ↓
读懂递归交换：按 ASCII 升序排序
        ↓
代入等式：先得到 U、J、W，并限制第 4 位
        ↓
解码两段 Base64：得到 WP1 和 jMp
        ↓
拼成 UJWP1jMp，再按平台格式提交
```

## 常见误区

- **把快速排序当成加密**：它只是重排固定字符；先识别算法整体效果，再决定是否需要复刻每个分支。
- **看到 `+4*i` 就照抄或删除**：地址步长取决于元素大小。`int[]` 是 4 字节步长，`char[]` 是 1 字节步长。
- **反推整数除法时直接乘回去**：`x / 4 == 20` 不等于 `x == 80`；对非负整数，解可能是 80、81、82、83。需要别的校验条件排除。
- **把 Base64 当加密**：已知编码字符串可以直接解码；题目是在用编码结果约束输入的两段字符。
- **拼接顺序弄反**：`V1Ax` 对应输入第 3–5 位，`ak1w` 对应第 6–8 位，原输入应为 `UJWP1jMp`。
- **照抄有笔误的 WP**：有转载文章末尾把结果写成 `UJMP1jMP`；与前面已解码的两段不一致。逐项按伪代码和 Base64 结果复核后应为 `UJWP1jMp`。

## 练习与复测

不看脚本回答：

1. 为什么排序输入常量 `ZJSECaNH3ng` 后得到 `3CEHJNSZagn`？
2. `input[3] / 4 == 20` 为什么不能单独推出 `input[3] == 80`？
3. Base64 的 `V1Ax` 和 `ak1w` 分别约束输入的哪三个位置？
4. 伪代码若把基址类型从 `int *` 改成 `char *`，数组下标的字节步长会怎样变化？

## 资料

- [Basstorm：BUUCTF-RE-刮开有奖](https://www.cnblogs.com/basstorm/p/12618478.html)：简短路线，重点看排序结果、两段 Base64 和最终拼接。
- [Hk_Mayfly：BUUCTF--刮开有奖](https://www.cnblogs.com/Mayfly-nymph/p/11488817.html)：较详细伪代码，重点看 DialogFunc、ASCII 数组、比较条件和 Base64 字符表。
- [EPs1l0h：buuctf[刮开有奖]-writeup](https://www.cnblogs.com/EPs1l0h/p/15706944.html)：可对照排序函数和推导；末尾 flag 字符大小写有笔误，使用前按等式复核。
- 相关知识：`常见加密算法识别与还原` · `RE知识体系与题型地图` · `RE题目与WP索引`
