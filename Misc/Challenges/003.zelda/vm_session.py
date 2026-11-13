#!/usr/bin/env python3
"""Run from the UTM VM: connect, then execute a command script, echoing everything."""
import socket, time, sys, json

HOST, PORT = "127.0.0.1", 26732

def connect(timeout=10):
    s = socket.socket(); s.settimeout(timeout)
    s.connect((HOST, PORT))
    s.settimeout(1.0)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < 4:
        try:
            d = s.recv(8192)
        except socket.timeout:
            continue
        except Exception:
            break
        if not d:
            break
        buf += d
        if b"Plateau" in buf:
            break
    if b"Plateau" not in buf:
        s.close(); return None
    return s, buf

def drain(s, quiet=0.5, total=6.0):
    s.settimeout(quiet)
    buf = b""; end = time.time() + total
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        except Exception:
            break
        if not d:
            buf += b"<<EOF>>"; break
        buf += d
    return buf.decode("utf-8", "replace")

def main():
    cmds = sys.argv[1:]
    r = connect()
    if not r:
        print("[!] no banner; service refused", flush=True)
        return 1
    s, buf = r
    print("[banner]", buf.decode("utf-8", "replace"), flush=True)
    for c in cmds:
        print(">>> " + c, flush=True)
        s.sendall(c.encode() + b"\n")
        time.sleep(0.1)
        out = drain(s)
        print(out, flush=True)
        if "<<EOF>>" in out:
            print("[!] server closed", flush=True)
            break
    s.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
