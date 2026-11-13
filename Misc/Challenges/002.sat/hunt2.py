#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""地址热更新守候：读 addr.txt -> 目标变了自动切，无需重启。
addr.txt 格式:  host:port
"""
import os, re, socket, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from satlib import *

HERE = os.path.dirname(os.path.abspath(__file__))
ADDR = os.path.join(HERE, "addr.txt")
LOG = os.path.join(HERE, "hunt2.log")
FLAG_RE = re.compile(rb"[A-Za-z0-9_]{2,8}\{[^}]{3,80}\}")
DEFAULT = ("127.0.0.1", 24619)


def log(m):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), m)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def target():
    try:
        raw = open(ADDR).read().strip().splitlines()[0].strip()
        h, p = raw.rsplit(":", 1)
        return h, int(p)
    except Exception:
        return DEFAULT


def rt(host, port, payload, wait=2.5):
    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception:
        return None
    out = b""
    try:
        s.sendall(payload)
        s.settimeout(wait)
        t0 = time.time()
        while time.time() - t0 < wait:
            try:
                d = s.recv(65536)
            except socket.timeout:
                break
            except OSError:
                break
            if not d:
                break
            out += d
    finally:
        try: s.close()
        except Exception: pass
    return out


def save(tag, data):
    if not data:
        return
    with open(os.path.join(HERE, "hit_%s.bin" % tag), "ab") as f:
        f.write(b"\n=== %s ===\n" % time.strftime("%H:%M:%S").encode() + data)
    m = FLAG_RE.search(data)
    log("DATA[%s] %r%s" % (tag, data[:300], ("  *** FLAG=" + m.group().decode()) if m else ""))
    if m:
        open(os.path.join(HERE, "flag.txt"), "ab").write(m.group() + b"\n")


def main():
    log("=== hunt2 start, addr=%s:%d ===" % target())
    probes = [(m, k, frame(k, b"", m)) for m in MODES for k in (b"T", b"C", b"F")]
    n = 0
    cur = target()
    while True:
        t = target()
        if t != cur:
            cur = t
            log(">>> 目标切换为 %s:%d" % cur)
        host, port = cur
        for mode, kind, p in probes:
            out = rt(host, port, p, 2.5)
            if out:
                save("%s_%s" % (mode, kind.decode()), out)
                log("LIVE %s:%d mode=%s kind=%s -> %r" % (host, port, mode, kind, out[:200]))
                # 命中后立刻跑全部路线
                run(host, port, mode)
                out = None
        n += 1
        log("cycle %d @ %s:%d dead" % (n, host, port))
        time.sleep(15)


def run(host, port, mode):
    import subprocess
    env = dict(os.environ, SAT_HOST=host, SAT_PORT=str(port), SAT_MODE=mode)
    log("== 命中，跑全流程 (mode=%s) ==" % mode)
    subprocess.Popen([sys.executable, "-u", os.path.join(HERE, "live_hunt.py")], env=env,
                     stdout=open(os.path.join(HERE, "hunt.out"), "a"), stderr=subprocess.STDOUT)


if __name__ == "__main__":
    main()
