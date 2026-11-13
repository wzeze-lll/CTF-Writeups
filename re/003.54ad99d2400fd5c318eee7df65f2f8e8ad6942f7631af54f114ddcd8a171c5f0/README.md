# 知识点

逆向

# 题目分析

分类：re。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [Description.txt](Description.txt)
- [login.html](login.html)

## 已有分析

- [FLARE_ON_2017_Challenge1_login_html_WP.md](notes/FLARE_ON_2017_Challenge1_login_html_WP.md)


### FLARE-On 2017 Challenge 1：login.html

> [!abstract] 题目结论
> 页面把输入内容做 ROT13，再和写在 JavaScript 里的字符串比较。把比较串再做一次 ROT13，就得到输入：`ClientSideLoginsAreEasy@flare-on.com`。如果平台要求 `flag{...}` 外壳，提交格式为 `flag{ClientSideLoginsAreEasy@flare-on.com}`。

#### 题目画像与证据范围

- **类型：** 网页文件 / JavaScript 逻辑逆向。
- **核心知识：** 查看 HTML 源码、追踪输入到比较点、ROT13、区分程序校验文本与平台 flag 格式。
- **输入：** 页面中 `id="flag"` 的输入框。
- **校验：** 按钮事件处理函数将输入转成 ROT13，再与常量比较。
- **证据状态：** 根据用户提供的完整 HTML 源码整理，并与下方两篇公开题解交叉核对；没有在本机浏览器运行原题附件，因此不记作动态复现。

这是一道本地页面校验题。当前证据只说明页面在浏览器里比较字符串，不能据此推断存在服务器端认证或 Web 漏洞。

#### 先读懂页面在做什么

源码中的关键逻辑是：

```javascript
document.getElementById("prompt").onclick = function () {
    var flag = document.getElementById("flag").value;
    var rotFlag = flag.replace(/[a-zA-Z]/g, function (c) {
        return String.fromCharCode(
            (c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13)
                ? c
                : c - 26
        );
    });

    if ("PyvragFvqrYbtvafNerRnfl@syner-ba.pbz" == rotFlag) {
        alert("Correct flag!");
    } else {
        alert("Incorrect flag, rot again");
    }
};
```

翻成人话：

1. 从输入框取出用户输入。
2. 找出其中每个英文字母，把它向后移动 13 位；超过 `Z` 或 `z` 就绕回字母表开头。
3. 数字、`@`、点号等非字母保持不变。
4. 把变换结果和固定字符串比较，相同就显示成功提示。

因此比较串是**输入经过变换后的结果**，不是应该直接输入的内容。

#### 手算一个字符

以大写 `T` 为例：

```text
'T' 的 ASCII 值是 84
84 + 13 = 97，也就是小写区间以外的数
因为大写字母上限是 'Z' = 90，所以减 26
97 - 26 = 71，也就是 'G'
```

实现里按当前字符的大小写选择上限：大写用 `90`，小写用 `122`。由于处理范围已经限制为英文字母，回绕后大小写不会改变。非字母没有进入替换回调，因此原样保留。

ROT13 可以自己解密自己：对同一字母再移动 13 位，总共移动 26 位，刚好回到原字符。

#### 还原输入

题目给出的比较串：

```text
PyvragFvqrYbtvafNerRnfl@syner-ba.pbz
```

对它再做 ROT13：

```text
ClientSideLoginsAreEasy@flare-on.com
```

这就是页面要接收的原始输入。`flag{...}` 是题目平台常用的提交包装；页面本身比较的是邮箱样式的正文，不包括大括号。

#### 简短可运行脚本

只用 Python 标准库，不需要安装第三方包：

```python
import codecs

cipher = "PyvragFvqrYbtvafNerRnfl@syner-ba.pbz"
answer = codecs.decode(cipher, "rot_13")

### ROT13 做两次应回到原字符串，用断言检查方向和数据是否抄对。
assert codecs.decode(answer, "rot_13") == cipher

print(answer)
print(f"flag{{{answer}}}")
```

预期输出：

```text
ClientSideLoginsAreEasy@flare-on.com
flag{ClientSideLoginsAreEasy@flare-on.com}
```

`codecs.decode(..., "rot_13")` 处理英文字母并保留非字母。若想练习手写变换，可看 `ROT13 知识点`。

#### 用浏览器验证页面逻辑

拿到原始 HTML 文件时，可以先用文本编辑器查看源码，搜索 `onclick`、`.value`、`replace` 和比较用的常量。也可以在浏览器开发者工具的 Console 中验证：

```javascript
const cipher = "PyvragFvqrYbtvafNerRnfl@syner-ba.pbz";
const answer = cipher.replace(/[a-zA-Z]/g, c =>
    String.fromCharCode(
        (c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26
    )
);
console.log(answer);
```

应该显示：

```text
ClientSideLoginsAreEasy@flare-on.com
```

这验证的是页面变换逻辑。若要验证原题交互，还需要打开原始 HTML，在输入框中输入正文并点击按钮；本次没有执行这一步。

#### 做同类题的观察顺序

1. 先确认文件类型。`.html` 通常先用浏览器或文本编辑器看，不要因为 IDA 能打开就把它当作机器码分析。
2. 找页面事件入口，例如 `onclick` 或事件监听器。
3. 追踪输入来源，例如 `.value`。
4. 找输入经过的变换，再找最终 `if` 比较的常量。
5. 根据赋值方向还原：这里是 `ROT13(输入) == 常量`，所以对常量再做 ROT13 得到输入。
6. 用短脚本断言检查变换可逆，再回到页面验证。

#### 常见误区

| 误区 | 正确理解 |
|---|---|
| 直接把 `Pyvrag...` 当作输入 | 它是输入经过 ROT13 后的比较结果；要再做一次 ROT13 |
| 把 ROT13 当作安全加密 | 它是可逆的字母替换，没有密钥，也不适合保护真实密码 |
| 以为标点也会变化 | 正则只匹配 `[a-zA-Z]`，`@` 和 `.` 会保留 |
| 认为这是服务器登录漏洞 | 现有证据只显示浏览器端字符串比较；没有服务器端行为证据 |
| 看到成功提示就称为远程验证 | 页面弹窗只验证本地 JavaScript 分支，不代表连接了服务器 |

#### 自测

若输入中有一个小写 `z`，ROT13 后是什么？为什么 `@` 不变？请分别用手算和 Python 验证。

#### 参考资料

- [Lynn's Blog：2017 Flare-On 1 Login](https://0x00.tw/2018/05/10/2017-Flare-On-1-Login.html)：看页面校验代码、ROT13 与目标字符串。
- [0xec：Flare-On Challenge 2017 Writeup](https://0xec.blogspot.com/2017/10/flare-on-challenge-2017-writeup.html)：交叉核对题目答案和验证逻辑。
- `基础运算与XOR逆算`：看 ROT13 的通用解释与简短脚本。
- `RE题目与WP索引`：查看本知识库其他 RE 题目和 WP。

#### 相关笔记

`基础运算与XOR逆算` · `RE知识体系与题型地图` · `RE题目与WP索引`


# EXP

当前归档中没有已识别的 EXP / 求解脚本。
