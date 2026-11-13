#!/usr/bin/env python3
# 等实例起来：每轮用多种封装戳一下，一旦有非空回应立刻落盘
import socket, time, sys, json
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from satlib import *
HOST, PORT = "127.0.0.1", 24619
LOG = "/home/ctf/Desktop/work/buuctf/sat/hits.log"
probes = [frame("T", b"", m) for m in MODES] + [frame("C", ccsds_tc(0x064, 0), m) for m in MODES]
round_ = 0
while True:
    round_ += 1
    for i, p in enumerate(probes):
        try:
            s = socket.create_connection((HOST, PORT), timeout=6); s.settimeout(2.0)
            s.sendall(p)
            try:
                d = s.recv(65536)
            except Exception:
                d = b""
            s.close()
        except Exception as e:
            d = b""
        if d:
            line = "%s probe%d sent=%s got=%r\n" % (time.strftime("%H:%M:%S"), i, p.hex(), d[:200])
            print(line, flush=True)
            open(LOG, "a").write(line)
    print("[%s] round %d: all silent" % (time.strftime("%H:%M:%S"), round_), flush=True)
    time.sleep(20)
