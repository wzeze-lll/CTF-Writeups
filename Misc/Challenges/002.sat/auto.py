#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""高频守候：实例一开口立刻落盘。轮转探测 + 静默 banner 线程。"""
import os, re, socket, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from satlib import *

HOST = os.environ.get("SAT_HOST", "127.0.0.1")
PORT = int(os.environ.get("SAT_PORT", "24619"))
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "auto.log")
FLAG_RE = re.compile(rb"[A-Za-z0-9_]{2,}\{[^}]{3,}\}")


def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def dump(tag, data):
    p = os.path.join(HERE, "hit_%s.bin" % tag)
    with open(p, "ab") as f:
        f.write(b"\n=== %s ===\n" % time.strftime("%H:%M:%S").encode() + data)
    m = FLAG_RE.search(data)
    log("*** DATA[%s] %r%s" % (tag, data[:300], ("  FLAG=" + m.group().decode()) if m else ""))


def probe(payload, wait=3.0):
    try:
        s = socket.create_connection((HOST, PORT), timeout=5)
    except Exception:
        return b"", "connfail"
    out, why = b"", None
    t0 = time.time()
    try:
        if payload:
            s.sendall(payload)
        s.settimeout(wait)
        while time.time() - t0 < wait:
            try:
                d = s.recv(65536)
            except socket.timeout:
                break
            except OSError:
                why = "rst"; break
            if not d:
                why = "fin"; break
            out += d
    finally:
        try: s.close()
        except Exception: pass
    return out, why


def silent_thread():
    """永不发数据，只等 banner"""
    while True:
        try:
            s = socket.create_connection((HOST, PORT), timeout=5)
            s.settimeout(30)
            out = b""
            while len(out) < 65536:
                d = s.recv(4096)
                if not d:
                    break
                out += d
            if out:
                dump("banner", out)
        except Exception:
            pass
        time.sleep(2)


def main():
    log("=== auto watch v2 start -> %s:%d ===" % (HOST, PORT))
    threading.Thread(target=silent_thread, daemon=True).start()
    probes = []
    for mode in MODES:
        for kind in (b"T", b"C", b"F"):
            probes.append(("%s_%s" % (mode, kind.decode()), frame(kind, b"", mode)))
    probes.append(("empty", b""))
    i = 0
    while True:
        tag, p = probes[i % len(probes)]
        i += 1
        out, why = probe(p, 3.0)
        if out:
            dump(tag, out)
        elif i % 16 == 0:
            log("round %d done (last %s/%s, no data)" % (i // 16, tag, why))
        time.sleep(0.4)


if __name__ == "__main__":
    main()
