# 剑士 Hero / 至尊魔戒 / 海拉鲁 —— 黑盒静态推理作战计划

> 无附件、无源码，纯黑盒。所有命令未对目标执行。脚本：`probe.py` / `exp_whisper.py` / `exp_logic.py`

## 0. 状态机基线（从题目给的输出反推）

| 字段 | 值 | 推断 |
|---|---|---|
| `Main World Hero` vs `Inventory Puppet Hero` | 两个标题 | **两个对象视图**：世界对象 + 傀儡/镜像背包。uaf/结构体覆盖的高危信号 |
| `Equipped: empty` 但 `inv list` 里 `equipped=0` | 0/1 布尔 | `inv equip` 必须先做，`mw whisper` 只吃"已装备"物品 |
| `HP=100 Stamina=100 Rupees=1000 Arrows=10 BossHP=0` | 一排标量 | hero 结构体字段布局大概率就是这个顺序 |
| `EXP=0 Battle=inactive Turn=0` | 第 3 行 | 战斗状态机独立；`Turn` 是回合计 |
| `shop list`: 10000/stock=1 Master Sword | 唯一高价品 | 明确目标物 |
| `Bomb Flower price=64 stock=999` | 可堆叠消耗品 | `use item` 的战斗资源 |
| `enemy_hp=400/400` vs `player_hp=100` | 4 倍血差 | 树枝打不动 → 必须搞武器或搞数值 |

## 1. 假设排序

| # | 假设 | 概率 | 一句话 |
|---|---|---|---|
| H1 | `mw whisper` 无长度校验，越界写进 item 结构体 / hero 结构体（Rupees/HP/BossHP 直接可控） | 55% | "whisper=低语"就是给你一个**任意字节写**，最终靠改游戏状态拿 flag，不需要 ROP |
| H2 | `shop buy <idx> <qty>` 数量负数 / `price*qty` int32 溢出 → 卢比暴涨 | 25% | 最符合"中文 misc 文本游戏"的经典题面 |
| H3 | `mw throw` / `mw pickup` / `inv drop` 生命周期错乱：UAF、double free、负索引 OOB | 12% | "Puppet" 这个词就是提示 |
| H4 | `desc` 被 `printf(desc)` 直接当格式串 → `%n` 任意写 | 6% | 依赖 H1 的写原语才能注入 `%n` |
| H5 | 杂项：`map teleport castle` 无门禁、`inv sort` 比较器、stock 负数、flee 刷 EXP | 2% | 顺手验证，成本极低 |

**题型判断**：`misc（逻辑）+ 结构体字段覆盖的盲打 pwn-lite`。不是栈溢出/ROP 题——题面没有任何二进制交互痕迹，所有输出都是 `[*]` 风格的结构化状态，天然是"状态可观测"的盲打环境。

## 2. 验证阶梯（先无损 → 后破坏，破坏性探针一条连接一次）

见 `probe.py`：
- `python3 probe.py recon`：help / mw show / inv list / shop list / map show + 重连看**状态是否跨连接持久**
- `python3 probe.py hierarchy`：`help mw` / `help shop` / `mw` / `battle help` → 挖隐藏子命令（`use item` 是不是顶格命令）
- `python3 probe.py edges`：26 条边界探针，每条独立连接

H1 验证：`python3 exp_whisper.py ramp`（斜坡 payload，byte[i]=i&0xff，被踩的字段打印成十进制后能反推偏移）。
H2 验证：`python3 exp_logic.py money`。
H3 验证：手动序列 `inv equip 0` → `mw throw 0` → `inv list`（puppet 是否还显示树枝 = UAF 铁证）→ `shop buy 3 1` → `inv list`（是否类型混淆成 Bomb Flower）。

## 3. mw 原语盲打（H1/H3）

- Phase A 建模：斜坡 payload 扫长度 → 找字段边界
- Phase B 塑形：`mw throw` + `shop buy` 回收同尺寸 chunk；抛两次看 double free；买两件看是否同 chunk（改 A 看 B）
- Phase C 提权：改 price → 卖；改 type → 当武器；改 Rupees/HP/BossHP → 直接赢
- Phase D 拿 flag：改完状态 → `map teleport castle` → `battle` → 秒杀 → flag

## 4. 纯逻辑速通（H2）

`exp_logic.py`：卢比阶梯 → 买/装备 Master Sword → teleport castle → 自适应回合。
数值预算公式：`need = ceil(enemy_hp / D)`；可行条件 `(need-1)*E < player_hp`；不满足就插 `use item`。

## 5. 连上必抓清单

见正文表格（风险等级 = 会不会毁掉本次会话状态）。
