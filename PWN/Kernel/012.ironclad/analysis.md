# Ironclad — Windows Kernel Driver Analysis

## 0. 结论速览

| 项目 | 结果 |
|------|------|
| 目标 | `ironclad.sys` — x64 Windows 内核驱动 |
| 设备 | `\\.\Ironclad`（SDDL 限制访问） |
| 环境 | Win11 26H2，VBS/HVCI 关闭，test signing 打开，Secure Boot 关闭 |
| 硬缓解 | /GS 栈金丝雀、CFG（Guard CF）、`MmProtectDriverSection`、池块 MAC（每启动随机 key） |
| 主要漏洞 | **0x22240c 处理函数 `0x140004F50` 栈缓冲区溢出**（ring flags bit0=1 时溢出 0x200 字节到 0x100 字节栈缓冲） |
| 信息泄露 | **0x222408 查询位 bit1 泄露内核指针**（`IcRS` 结构地址） |
| 其他 | 0x222408 除零（BSOD DoS）；0x222410 是 SHA-256 门控任意读写后门但被禁用 |

## 1. 文件与保护

`setup-vm.ps1` 的 `-Stage Boot` 说明远程 VM：
- Secure Boot **off**、test signing **on**、VBS/HVCI **off**、hypervisor **off**。

驱动自身 `DllCharacteristics = 0x41e0`：
`HIGH_ENTROPY_VA | DYNAMIC_BASE | FORCE_INTEGRITY | NX_COMPAT | GUARD_CF`。
`DriverEntry` 结束前调用 `MmProtectDriverSection`（`0x140005370 -> IAT[0x6058]`）把驱动节区设为只读。

`DriverEntry`（`0x14001D000`）先 `ExInitializeResourceLite(&g_res, 0x140008288)`，创建设备
（安全描述符字符串 `SeConvertStringSecurityDescriptorToSecurityDescriptor`），注册分发：

| MajorFunction | 地址 | 说明 |
|---|---|---|
| IRP_MJ_CREATE (0) | `0x1400010D0` | 分配 0x10 字节 context（magic `"FILE"`），`[ctx+8]=0` |
| IRP_MJ_CLOSE (2) | `0x140001030` | 释放 ring，释放 context（tag `IcCf`） |
| IRP_MJ_DEVICE_CONTROL (14) | `0x140001160` | IOCTL 分发 |
| IRP_MJ_CLEANUP (18) | `0x140001000` | 直接完成 |
| DriverUnload | `0x140001470` | 删符号链接、删设备、删资源锁 |

## 2. IOCTL 分发

`0x140001160` 从 IO_STACK_LOCATION 读 `ebx = IoControlCode`，与下列值比较：

| IOCTL | 处理函数 | 语义 |
|---|---|---|
| `0x222400` | `0x1400025F8` | **创建 ring**（输入 0x28 字节结构） |
| `0x222404` | `0x1400022D4` | **处理 N 个 ring 槽位**（输入 = dword count） |
| `0x222408` | `0x1400051B0` | **查询 ring 状态**（输入 = 8 字节 flags） |
| `0x22240C` | `0x140004F50` | **dump ring 哈希表** → 栈溢出 |
| `0x222410` | `0x1400050C4` | SHA-256 门控任意读写（**禁用**） |

> METHOD_BUFFERED：`SystemBuffer = IRP->AssociatedIrp.SystemBuffer`（`[IRP+0x18]`）。

## 3. 关键数据结构

### context（每句柄，tag `IcCf`，0x10 字节）
```
+0x00  dword  0x454C4946 "FILE"
+0x08  qword  ring 指针（创建 ring 后非 0）
```

### ring（tag `IcRg`，大小 = 0x80 + 0x18*edi）
```
+0x00  dword  0x474E4952 "RING"
+0x04  dword  id（全局自增）
+0x08  qword  IcRS 结构指针
+0x10  dword  head（ring 槽位读游标，处理一个槽 +1）
+0x14  dword  write 游标（结果写回 user_ptr2 的游标）
+0x18  dword  flags
+0x1C  dword  已写结果计数
+0x48  LIST_ENTRY 全局 ring 链表节点
+0x58  qword  IcTb 哈希表（0x800 字节，tag `IcTb`）
+0x68  qword  成功处理的 opcode 计数（← 除零点）
+0x70  qword  （被除数的另一计数）
+0x80  哈希表项数组：edi 项 × 0x18 字节
```

哈希表项（0x18 字节）：
```
+0x00  qword  DESC 指针（OR 0xFFFF000000000000 编码）
+0x08  dword  （out[4] 的来源，见下）
+0x0C  word   占用标志（1=占用）
+0x0E  word   flags
+0x10  qword  ATCH 链表节点指针
```

### IcRS 结构（tag `IcRS`，0x58 字节，创建 ring 时从输入复制）
```
+0x00  dword  0x43534552 "RSEC"
+0x04  dword  id
+0x08  qword  ring 指针
+0x10  dword  slot_count   （2 的幂，0x10..0x1000）
+0x14  dword  field0c      （2 的幂，0x10..0x1000）
+0x18  dword  slot_count-1 （掩码）
+0x1C  dword  field0c-1    （掩码）
+0x20  dword  edi = ((flags&1)+1)<<4  → 0x10 或 0x20
+0x24  dword  flags
+0x28  qword  user_ptr1（读源，64 字节/槽）
+0x30  qword  user_ptr2（写目标，0x18 字节/结果）
+0x38  qword  queue（可选，0x10000 字节 tag IcCl）
+0x40  qword  count 指针（可选）
```

### 创建 ring 输入结构（IOCTL 0x222400，0x28 字节）
```
+0x00  dword  op（必须 == 3）
+0x04  dword  flags（必须 0 或 1；bit0=1 → edi=0x20）
+0x08  dword  slot_count（2 的幂，0x10..0x1000）
+0x0C  dword  field0c  （2 的幂，0x10..0x1000）
+0x10  qword  user_ptr1（非空，8 对齐）
+0x18  qword  user_ptr2（非空，8 对齐）
+0x20  qword  count 指针（可空）
```

## 4. 漏洞 A：栈缓冲区溢出（核心漏洞）

**位置**：`0x140004F50`（IOCTL `0x22240C` 处理函数）。

**触发条件**：创建 ring 时 `flags & 1 == 1`（合法），使 `edi = 0x20`。

**原因**：
```c
// 0x140004F50 prologue: sub rsp, 0x148
// memzero 0x100 字节 @ [rsp+0x30]  —— 只有 0x100 字节
r12d = [IcRS+0x20];   // = edi ∈ {0x10, 0x20}
r14  = rsp + 0x34;
for (i = 0; i < r12d; i++) {          // 当 edi=0x20 → 循环 32 次
    r14[0]  = [ring+0x88 + i*0x18];   // 写 4 字节
    r14[-4] = i;                       // 写 4 字节
    if (occupied) { r14[4] = [DESC+8]; r14[8] = flags; }
    r14 += 0x10;
}
// 结果：edi=0x20 时向 [rsp+0x30] 起写 0x200 字节，
//       越过 [rsp+0x130]（/GS cookie）直至 [rsp+0x230]，
//       覆盖 saved rbx 和返回地址。
```

验证（算术）：
- 缓冲 `[rsp+0x30 .. rsp+0x130)` = 0x100 字节。
- `edi=0x10` → 写 0x100 字节，刚好到 cookie 前，安全。
- `edi=0x20` → 写 0x200 字节，到 `rsp+0x230`，**覆盖 cookie、保存寄存器、返回地址**。

写入内容可控度：
- `[rsp+0x30+i*0x10+0]` = 循环计数 i（不可控，但确定）。
- `[rsp+0x30+i*0x10+4]` = `[ring+0x88+i*0x18]`（哈希表项 +0x08，受 opcode 影响）。
- `[rsp+0x30+i*0x10+8]` = `[DESC+8]`（DESC 对象 +0x08，受创建 DESC 的 opcode 参数影响）。
- `[rsp+0x30+i*0x10+0xC]` = 计算出的 flags（部分可控）。

## 5. 漏洞 B：内核指针泄露

**位置**：`0x1400051B0`（IOCTL `0x222408`，输入 8 字节 flags）。

```c
if (flags & 2)
    out[0x38] = [ring+0x08];   // ← 泄露 IcRS 结构的内核池地址
```

即：`DeviceIoControl(0x222408, &(DWORD)2, 4, out, 0x40)` 后 `*(QWORD*)(out+0x38)`
是内核堆地址（`IcRS` 对象）。用于突破 KASLR / 定位 ring。

## 6. 其他问题

### 6.1 除零（DoS）
`0x1400051B0`（0x222408）在 `flags & 1` 时执行 `rax=[ring+0x70]; rdx=0; div [ring+0x68]`。
若 `[ring+0x68]==0`（未处理过任何 opcode）→ 内核 #DE → BSOD。

### 6.2 被禁用的后门
`0x1400050C4`（0x222410）先 `cmp [0x14001A000],0; je → 0xC0000022`。
`0x14001A000`（.kdp 段首）在文件中为 0 且**从不被写入**，故该 SHA-256 门控的
`memcpy(任意内核地址, 用户, ≤0x100)` / `memcpy(用户, 任意内核地址, ≤0x100)` 后门**永远不可达**，
是误导项（`0x14001A010` 那个 32 字节 SHA-256 摘要无需破解）。

## 7. 完整利用思路

1. `CreateFile("\\\\.\\Ironclad", ...)` 打开设备。
2. `DeviceIoControl(0x222400)` 创建 ring：
   - `op=3, flags=1, slot_count=0x10, field0c=0x10`，
   - `user_ptr1 = VirtualAlloc(0x1000)`（64 字节槽数组），
   - `user_ptr2 = VirtualAlloc(0x1000)`。
3. `DeviceIoControl(0x222408, &2)` 泄露 `IcRS` 内核地址。
4. 通过 opcode（0x222404 处理 64 字节命令槽）构造 DESC 对象，使哈希表项
   `+0x08` 与 `[DESC+8]`、`flags` 落入期望值（用于覆盖返回地址 / 构造数据）。
5. 需要进一步拿到 /GS cookie（`__security_cookie @ driver+0x8240`）才能让 epilogue
   的 `__security_check_cookie` 通过；否则溢出只会触发 BSOD。
   - 利用 opcode 系统寻找读原语，或结合 5 的指针泄露定位驱动基址后读 cookie。
6. 触发 `DeviceIoControl(0x22240C)` 栈溢出 → 覆盖返回地址 → ROP（token steal 或
   任意写 `nt!PsInitialSystemProcess` 相关，再读 `C:\flag.txt`）。

> 实际远程 flag 在 `C:\flag.txt`，ACL 仅 SYSTEM 可读，因此目标是提权到 SYSTEM 或
> 获得内核任意读。

## 8. 已验证的事实 vs 待验证

**已验证（静态反汇编 + 算术）**
- 上述所有地址、结构偏移、IOCTL 分发、溢出与泄露行为。
- SHA-256 门控后门不可达（`0x14001A000` 恒 0）。
- /GS、CFG、`MmProtectDriverSection` 启用。

**待运行时验证**
- /GS cookie 与驱动基址的具体泄露方式（依赖 opcode 语义，需在 VM 中动态调试验证）。
- DESC 对象字段对覆盖数据的精确可控度。
