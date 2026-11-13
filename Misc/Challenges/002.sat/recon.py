#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""黑盒协议探测：先让服务器开口，再谈利用。"""
import socket, struct, time, sys, itertools
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from satlib import *

HOST, PORT = "127.0.0.1", 24619


def probe(data, wait=3.0, tag=""):
    try:
        s = socket.create_connection((HOST, PORT), timeout=6)
    except Exception as e:
        return ("CONNFAIL", str(e))
    out = b""
    try:
        if data:
            s.sendall(data)
        t0 = time.time()
        s.settimeout(wait)
        while time.time() - t0 < wait:
            try:
                d = s.recv(65536)
            except socket.timeout:
                break
            except OSError as e:
                out += b"<RST>"; break
            if not d:
                out += b"<EOF@%.1fs>" % (time.time() - t0); break
            out += d
            if len(out) > 8192:
                break
    finally:
        s.close()
    return (tag, out)


def stage0():
    print("[0] 连通性/是否有 banner")
    try:
        s = socket.create_connection((HOST, PORT), timeout=6)
    except Exception as e:
        print("    连接失败:", e); return False
    t0 = time.time(); s.settimeout(10); got = b""
    try:
        while time.time() - t0 < 10:
            d = s.recv(4096)
            if not d:
                print("    %.1fs 后 EOF，期间数据 %r" % (time.time() - t0, got)); break
            got += d
            print("    banner:", d)
    except socket.timeout:
        print("    10s 静默，无 banner（可能等客户端先发帧）")
    s.close()
    return True


def stage1():
    print("\n[1] 外层封装判定：同一逻辑内容按 5 种封装发送")
    for mode in MODES:
        for kind in (b"T", b"C", b"F"):
            payload = frame(kind, b"", mode)
            tag, out = probe(payload, 2.5, "%s/%s" % (mode, kind.decode()))
            print("    %-16s -> %r" % (tag, out[:120]))


def stage2():
    print("\n[2] 首字节全量 fuzz（0x00-0xFF，len2be 空体）")
    hits = []
    for b in range(256):
        payload = bytes([b]) + b"\x00\x00"
        tag, out = probe(payload, 1.5)
        if out and out != b"<EOF>":
            hits.append((b, out))
            print("    hit 0x%02x -> %r" % (b, out[:120]))
    print("    hits:", len(hits))


def stage3(apid_guess=0x064):
    print("\n[3] CCSDS 命令包功能码枚举（APID=0x%03x）" % apid_guess)
    for fcode in range(0, 0x40):
        body = ccsds_tc(apid_guess, fcode)
        for mode in ("len2be", "raw"):
            tag, out = probe(frame("C", body, mode), 1.5)
            if out and b"<EOF>" not in out:
                print("    fcode=0x%02x %s -> %r" % (fcode, mode, out[:200]))
                break
        else:
            continue


if __name__ == "__main__":
    if not stage0():
        sys.exit(1)
    stage1()
    stage2()
    stage3()
