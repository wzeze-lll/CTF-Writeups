---
tags: [逆向, Android, JADX, WP, 凯撒移位, BUUCTF]
created: 2026-11-12
updated: 2026-11-12
evidence: STATIC_ONLY
level: L1
---

# BUUCTF findit：Android 字符处理与凯撒移位

> [!abstract] 题目结论
> 这道 APK 里有两段不同的字符处理：第一段把固定提示串变成输入答案，第二段在输入正确后解出 flag。输入答案是 `LzakAkLzwXdsyZgew`；flag 是 `flag{c164675262033b4c49bdf7f9cda28a75}`。**答案输入和最终 flag 不是同一个字符串。**

## 题目画像与证据范围

- **类型：** Android APK / Java 逻辑逆向。
- **主要工具：** JADX 查看 Java 伪代码；必要时用 Apktool 查看 Smali。
- **知识点：** Activity 与按钮回调、字符数组、条件判断、返回/分支、ASCII 字符移位、`% 26`、Python 还原。
- **分析依据：** 用户提供的 Java/Smali 讲解内容，以及两篇已打开核对的公开题解中的 `MainActivity` 代码和密文。
- **证据状态：** 静态分析与脚本逻辑整理；没有在本机安装并运行原 APK，不记作设备动态复现。

## 先看按钮点击后的流程

题目在 `onCreate()` 中找到输入框、结果文本和按钮，并为按钮设置点击回调。点击后大致执行：

```text
读取输入框
    ↓
按数组 a 的规则生成正确答案 x
    ↓
x 与用户输入相同吗？
    ├─ 否：显示错误提示
    └─ 是：按数组 b 的规则生成 y，显示 flag
```

因此，分析时要分别跟踪“输入校验路径”和“flag 输出路径”。只看 `b` 能解出 flag，但还解释不了程序要求输入什么；只解出输入答案，也不等于拿到了 flag。

## 第一段：从数组 `a` 推出输入答案

固定字符数组是：

```java
char[] a = {
    'T', 'h', 'i', 's', 'I', 's', 'T', 'h', 'e',
    'F', 'l', 'a', 'g', 'H', 'o', 'm', 'e'
};
```

循环逻辑可以概括为：

```java
if ((c >= 'A' && c < 'I') || (c >= 'a' && c < 'i')) {
    out = (char) (c + 18);
} else if (!isEnglishLetter(c)) {
    out = c;
} else {
    out = (char) (c - 8);
}
```

人话解释：`A` 到 `H`、`a` 到 `h` 加 18；其余英文字母减 8；非英文字母原样保留。手算几个字符：

| 原字符 | 规则 | 结果 |
|---|---|---|
| `T` | `T` 不在 `A..H`，所以减 8 | `L` |
| `h` | `h` 在 `a..h`，所以加 18 | `z` |
| `i` | 不在 `a..h`，所以减 8 | `a` |
| `I` | 不在 `A..H`，所以减 8 | `A` |

把整个数组跑一遍得到：

```text
LzakAkLzwXdsyZgew
```

`String.valueOf(x).equals(edit.getText().toString())` 是在比较生成的字符串与输入框文字是否相同。`equals()` 返回 `true/false`，随后决定走成功还是失败分支；这个返回值本身不会打印文字。相关基础见 `boolean 与返回值`。

## 第二段：从数组 `b` 解出 flag

题目中的字符数组为：

```text
pvkq{m164675262033l4m49lnp7p9mnk28k75}
```

程序只对英文字母加 16；如果结果越过字母范围，就减 26 绕回。数字、`{`、`}` 不变。字母的下标按 `a=0, b=1, ..., z=25` 计算：

```text
p：下标 15，(15 + 16) % 26 = 5  → f
v：下标 21，(21 + 16) % 26 = 11 → l
k：下标 10，(10 + 16) % 26 = 0  → a
q：下标 16，(16 + 16) % 26 = 6  → g
```

所以开头 `pvkq{` 变为 `flag{`，完整结果是：

```text
flag{c164675262033b4c49bdf7f9cda28a75}
```

### 原代码里的边界细节

公开代码在移位后使用 `y[i] >= 'z'` 判断回绕。标准的小写字母移位一般应在**大于 `'z'`** 时回绕，因为等于 `'z'` 仍是合法字母。原判断会让某个输入字母恰好移到 `'z'` 时多减 26。

本题给出的 `b` 中没有触发这个边界的字符，因此不会改变本题输出。复现原程序时，下面脚本会按题目实际判断写；分析一般 Caesar 移位时，则应优先使用模 26 公式。

## 一份可运行的 Python 复现脚本

脚本分别复现“生成输入答案”和“解出 flag”两段逻辑，并用断言检查结果，避免把输入答案误当成 flag。

```python
def is_english_letter(c):
    return "A" <= c <= "Z" or "a" <= c <= "z"


a = "ThisIsTheFlagHome"
answer = ""

for c in a:
    if "A" <= c < "I" or "a" <= c < "i":
        answer += chr(ord(c) + 18)
    elif not is_english_letter(c):
        answer += c
    else:
        answer += chr(ord(c) - 8)

b = "pvkq{m164675262033l4m49lnp7p9mnk28k75}"
flag = ""

for c in b:
    if not is_english_letter(c):
        flag += c
        continue

    value = ord(c) + 16
    # 按题目实现：落在大写/小写间隙，或大于等于 z 时减 26。
    if (ord("Z") < value < ord("a")) or value >= ord("z"):
        value -= 26
    flag += chr(value)

assert answer == "LzakAkLzwXdsyZgew"
assert flag == "flag{c164675262033b4c49bdf7f9cda28a75}"
print("input:", answer)
print("flag: ", flag)
```

运行后应分别打印：

```text
input: LzakAkLzwXdsyZgew
flag:  flag{c164675262033b4c49bdf7f9cda28a75}
```

`ord()` 把字符转成整数编码，`chr()` 把整数编码转回字符。第二段也可以用通用公式 `(ord(c) - ord('a') + 16) % 26 + ord('a')` 实现标准小写移位；这里保留题目原逻辑，是为了让脚本能逐字节对应它的边界判断。

## JADX 中怎么定位这些逻辑

1. 打开 APK，先看 `AndroidManifest.xml` 和启动 Activity；本题可从 `MainActivity.onCreate()` 开始。
2. 找 `findViewById()`，辨认输入框、结果文本和按钮分别保存在哪些变量。
3. 跟进 `setOnClickListener()` 的 `onClick()`，这是点击按钮后真正执行的代码。
4. 先读 `String.valueOf(x).equals(input)`，明确比较双方；再向上找 `x` 是怎么生成的。
5. 阅读成功分支里对 `b` 的循环，确认其结果被 `setText()` 显示。
6. 若 JADX 伪代码含糊，再到 Smali 核对 `invoke-*`、`move-result*`、`if-*` 和数组读写；不要把 Smali 的虚拟寄存器当成 CPU 的 `eax`/`rax`。

## 常见误区

| 误区 | 正确理解 |
|---|---|
| 把 `LzakAkLzwXdsyZgew` 当成 flag | 它是输入框需要的答案；flag 在通过检查后由数组 `b` 生成 |
| 只凭 `pvkq` 猜 Caesar | 外观只是线索；还要用代码中的 `+16` 和回绕条件证明 |
| 把 `>= 'z'` 当成标准回绕边界 | 标准写法通常是 `> 'z'`；题目原代码的等号是边界差异 |
| 把 Java 的 `char` 简单等同于 C 的 `char` | Java `char` 是 16 位 UTF-16 code unit；本题内容是 ASCII 范围字符，按 ASCII 值推导即可 |
| 以为找到 flag 字符串就算完整分析 | 还应解释输入验证、成功分支、结果显示和平台提交格式 |
| 把静态脚本结果写成 APK 已运行验证 | 脚本只复现算法；设备运行需安装 APK 并实际输入检查 |

## 练习与自测

1. 不运行脚本，手算 `a` 的前三个字符 `T h i` 变成什么，并说明每个字符命中了哪个分支。
2. 若 `b` 中有字符 `j`，按题目原代码会怎样处理？它和标准 Caesar `+16` 有什么差别？
3. 在 Smali 中看到 `String.equals()` 后的 `move-result` 和 `if-eqz`，说明它们怎样决定是否进入失败分支。

## 参考题解

- [布医的小世界：BUUCTF Reverse 篇（含 findit 的 JADX 代码）](https://www.buryia.top/2020/05/18/Learn/CTF/BUU/buu-re/)：看 `MainActivity`、按钮回调、两组数组及原始边界判断。
- [博客园：BUUCTF RE WP 部分合集（含 findit 的 Java 逻辑）](https://www.cnblogs.com/yee-l/p/18233898)：看 `a`、`b` 的代码和输入答案/flag 的区分。
- `Android-JADX与Smali分析`：补 JADX、`onClick()`、Java 返回值与 Smali 条件分支基础。
- `基础运算与XOR逆算`：补字符编码、字母范围变换和 Caesar 类逆算。

## 相关笔记

`Android-JADX与Smali分析` · `Android逆向入门` · `基础运算与XOR逆算` · `RE题目与WP索引`
