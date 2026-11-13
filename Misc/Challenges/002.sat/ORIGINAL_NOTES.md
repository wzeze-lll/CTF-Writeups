# 模拟卫星测控站 —— 作战笔记

目标：`/cf/host/flag`（卫星宿主文件系统）
入口：`nc 127.0.0.1 24619`
附件：无

---

## 0. 现场实测（先说结论）

| 时刻 | 动作 | 结果 |
|---|---|---|
| 18:41–18:55 | TCP connect | 成功（三次握手 OK） |
| 同上 | 静默等待 | 3.2~4.6s 后 **FIN，零字节** |
| 同上 | 发 `C`/`T`/`F`/`E` 单字节、`C+len2`、`C+len4`、CCSDS TC、ASCII | 全部零字节后 FIN |
| 同上 | TLS 握手 | EOF（不是 TLS） |

→ 端口在 listen，但后端进程没产出任何东西。这是动态容器型题目 **实例没起来 / 已过期** 的典型症状。
处理：面板点「重新下发」，等满 ~2 分钟初始化，再跑 `watch.py` 直到出现非空回应。

---

## 1. 协议模型（按题面反推）

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

## 2. 为什么一定打得穿：/cf/host/flag 这个路径本身就是答案

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

## 3. 四条路线（按命中概率排序）

### A. CFDP Metadata Put —— 源文件名穿越（最可能）
CFDP 的 `Metadata PDU` 带 **Source Filename / Destination Filename** 两个 LV 字段。
当卫星作为**发送方**执行 Put 时，`Source Filename` 就是它要读的本地路径。
把它设成 `/cf/host/flag`（或穿越变体），卫星就会按 File Data PDU 把 flag 切片推给你。

1. `F` + Metadata(directive 0x07/0x03), dir=toward-sender, mode=class1(不可靠，免 ACK 流程)
2. src=`TRAVERSALS[i]`，dst=`/cf/station/loot`
3. 收 `F` File Data PDU，拼 data field（跳过 4 字节 offset）
4. 补 EOF PDU / Finished PDU 收尾（class2 时）

### B. CCSDS 命令包参数注入
功能码枚举（0x00–0xFF）→ 找出带字符串参数的命令 → 参数里塞
`;cat /cf/host/flag`、`|cat ...`、`$(cat ...)`、反引号、`\n`。
命令包常常只校验"命令号权限"，不校验参数内容。

### C. Proxy Put 反向请求
`Proxy Put Request` 让**卫星主动连回你**（你在公网起 listener）。
- 用途 1：拿到卫星服务端实现的完整 cfg，看它真实路径映射
- 用途 2：把 `/cf/host/flag` 当 payload 塞进代理请求
- 用途 3：顺手做 SSRF，读 `file:///cf/host/flag` / 元数据接口

### D. 遥测/错误文本泄漏
先 `T` 请求遥测：很多模拟器把 "文件列表 / 目录 / 当前权限 / 允许的路径前缀" 直接吐在 TM 数据域里。
E 帧错误文本往往会回显你发的原始路径 —— 顺便验证穿越字符串有没有被规范化。

---

## 4. 拿不到 E/T 回应时的兜底
1. 用 `recon.py` 的 stage2 做首字节全量 fuzz（0x00–0xFF × 5 种封装），确认真正入口字节。
2. 检查是否 **先要登录帧**：`C` 帧里塞 `user/pass`、token、`HELLO`。
3. 观察关闭时机：固定 3~4s 关闭 ⇒ 服务端有 `alarm()` 或初始化超时，说明**它真的在跑**但没读到你的帧 ⇒ 封装猜错。
4. 若连接后立刻 FIN 且从不读数据 ⇒ 实例挂了，重新下发。

---

## 5. 工具
- `satlib.py` —— 帧封装/拆帧、CCSDS TC/TM、CFDP PDU（含 Metadata/FileData/EOF）
- `recon.py`  —— banner、封装判定、首字节 fuzz、功能码枚举
- `exploit.py`—— 四条路线跑批，自动正则抓 flag
- `watch.py`  —— 守候实例上线，一有回应写 `hits.log`

```bash
python3 recon.py           # 先摸协议
python3 exploit.py a       # 只打 CFDP 路线
python3 exploit.py all     # 四条全跑
```
