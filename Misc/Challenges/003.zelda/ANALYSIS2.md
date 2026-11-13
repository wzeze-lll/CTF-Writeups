# bad_puppet（Zelda/Hero/至尊魔戒）逆向与利用笔记

## 1. 程序形态
- `bad_puppet`：C++ 多线程 socket 服务，默认监听 `0.0.0.0:31337`，`--stdio` 走标准输入输出，`argv[1]` 为端口。
- 线程：`command_loop`（解析命令）→ 6 个 BlockingQueue（Battle/Inventory/MainWorld/Map/Shop/Transaction）→ 对应 worker 线程。
- 保护：PIE、Canary、NX、Full RELRO。
- 导入表里没有 `open/read`（文件）、`system/execve`、`getenv`，**二进制本身不读 /flag、也没有任何 flag 字符串** ⇒ 远端 flag 只能靠 RCE 读 `/flag`。

## 2. 关键结构（实测 + 反汇编）
```
Item（weapon/material，malloc 0xe8/0xf0）：
 +0x00 id        +0x08 type(1=weapon,3=material)
 +0x10 price     +0x18 damage/aux
 +0x20 name[0x40] +0x60 desc[0x80]  +0xe0 count

Ring（malloc 0x160，Item* 指向 base+0x90）：
 base+0x00 desc[0x80]   base+0x80 flags(bit0 = final-boss reward)
 base+0x88 refcnt 0x101  base+0x90 id/type/price/name...
 item_description(p): type==2 ? p-0x90 : p+0x60
 destroy_item(p):      type==2 ? free(p-0x90) : free(p)
```
`mw whisper` 的写入目标就是 `item_description(item)`，长度上限 0x7f（`min(len,0x7f)`，随后补 NUL），对真戒指是**安全**的；它是给“类型混淆出的假戒指”用的写原语。

## 3. 三个真实缺陷
1) **puppet 与 main world 双持有**：`inv equip` 后物品同时被背包和主世界引用；`inv drop` / `shop sell` 只释放一次，主世界 equip 槽变成悬垂指针（`mw show` 打出 `type=Unknown` 的垃圾）。
2) **`shop sell` + `mw throw` 双释放**：卖掉的物品仍被主世界持有，`mw throw` 会再次 `destroy_item` → `free(): double free detected in tcache 2`（本地已复现，见 `/tmp/err.log`）。
3) **克隆/丢弃的 stale slot**：`mw throw` 会 `clone_item` 出一个新 drop；克隆分配到的正是刚释放的 chunk，随后原指针再被 free，于是 drop 里的指针悬垂，`mw pickup` 把悬垂指针塞回背包 → 可对已释放 chunk 做类型混淆。

## 4. 经济漏洞（已本地打通，无需 RCE）
`shop buy` → `inv equip` → `shop sell`（+price，主世界仍持有）→ `mw throw`（克隆出 drop）→ `mw pickup`（克隆回背包）→ `shop sell`（再 +price）
每轮净赚一个售价（阔剑 260）。5 轮后 2300 卢比。

```
5 轮阔剑：1000 -> 2300
shop buy 3 35   (2240)
map teleport castle
battle
use item -> 1 -> 35     # 35*250 = 8750 >= 8000
=> Battle won: Demon King Ganondorf defeated
=> The Ring dropped in the main world
mw pickup 0 -> inv list -> inv equip 1 -> mw whisper 0 4142...
```
本地已完整跑通（`winremote.py`），**胜利只掉戒指，不打印 flag**。

## 5. 为什么本地拿不到 flag
二进制没有任何文件读取路径；`The Ring` 只是 0x160 的“记事本”，whisper 上限 0x7f。要拿 flag 必须：
- 把“假戒指 + ptr-0x90 写”升级成任意写（heap grooming 把假戒指放到目标对象前 0x90），
- 再劫持控制流做 ORW（PIE/Full RELRO，需要 heap→PIE/stack 的二次泄露）。
这是完整的堆利用链，不是游戏内逻辑能完成的。

## 6. 远端状态
- `127.0.0.1:26732`、`127.0.0.1:36943`、`127.0.0.1:34878` 三个地址都出现“TCP 能连、无 banner 立刻 EOF / 连接超时 / 直接 refused”。
- 平台容器是单会话 + 频繁重启：只在极少数时刻能拿到完整 banner，一次会话结束后要等数分钟才恢复，期间所有连接被立即关闭。
- 因此远端 flag 需要：稳定容器 + 完整 RCE 链。

## 7. 复现脚本
- `winremote.py`：连上后自动跑“5 轮经济漏洞 → 35 炸弹秒 Ganon → 捡戒指 → whisper”，环境变量 `EH/EP` 指定地址。
- `zelda/localrun.py` / `c.py`：本地起 `./bad_puppet` 并喂命令。
- `exploit.py`：带 tx 同步的循环版本（用于调试双释放）。

## 8. 远端实测（2026-11-01 01:0x，127.0.0.1:20483）
完整链路已在远端跑通：
```
5 轮阔剑经济漏洞 -> 2300 卢比
shop buy 3 34 -> battle -> use item 1 34 -> 8000 伤害
[+] Battle won: Demon King Ganondorf defeated
[+] The Ring dropped in the main world
mw pickup 0 -> inv equip 1 -> mw whisper 0 4142...
[+] whispered to ring: #13 The Ring
quit -> [*] bye
```
**远端胜利不打印 flag**（输出与本地完全一致），确认 flag 必须靠 RCE 读 /flag。

## 9. 已确认的 tcache 投毒原语（本地复现）
```
win -> 拿到 Ring -> inv equip 1
inv drop 1        # puppet 释放 ring（base），主世界仍持有 base+0x90
mw show           # description_head 变成堆指针（tcache fd 已被写入 base+0）
mw whisper 0 <16 hex>   # 直接改写已释放 ring 的 tcache fd/key（base+0 / base+8）
quit
=> glibc: tcache_thread_shutdown(): unaligned tcache chunk detected  (tcache 元数据被改写)
```
- `description_addr` 泄露 ring base（堆地址），safe-linking 编码 `stored = target ^ (base >> 12)` 可算。
- whisper 对已释放 ring 的类型/flag 检查仍然通过（type 在 base+0x98、flag 在 base+0x80，释放后内容未变）。
- 下一次 `malloc(0x160)`（`clone_item(Ring)`，即 `mw throw`/`inv drop` 的克隆）会返回任意 target。
- 克隆时 `clone_item` 把 0x150 字节从 base 复制到 target：前 0x7f 字节由 whisper 控制 ⇒ 受限任意写；同时克隆的 desc 在 target-0x90 未被写 ⇒ 可做 0x80 字节任意读。
下一步：用上述任意读泄露 std::thread::_State 的 libstdc++ vtable → libstdc++/libc base → environ → 栈 → ROP(ORW /flag)。
