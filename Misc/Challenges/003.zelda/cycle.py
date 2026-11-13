#!/usr/bin/env python3
"""One connection per interval; run a command script; log; quit."""
import os, sys, time, socket
os.environ.setdefault("ZH","127.0.0.1"); os.environ.setdefault("ZP","36943")
os.environ.setdefault("ZLOG","cycle.log")
import win

def one_try():
    s = socket.socket(); s.settimeout(4)
    try:
        s.connect((win.HOST, win.PORT))
    except Exception:
        s.close(); return None
    s.settimeout(0.8)
    buf=b""; t0=time.time()
    while time.time()-t0 < 2.0:
        try:
            d=s.recv(8192)
        except socket.timeout:
            continue
        except Exception:
            break
        if not d: break
        buf += d
        if b"Plateau" in buf: return s, buf
    s.close(); return None

def main():
    script = sys.argv[1]
    interval = float(sys.argv[2]) if len(sys.argv)>2 else 60
    rounds = int(sys.argv[3]) if len(sys.argv)>3 else 100
    cmds = [l.strip() for l in open(script) if l.strip() and not l.startswith("#")]
    win.log("cycle start script=%s interval=%s" % (script, interval))
    for r in range(rounds):
        t = one_try()
        if not t:
            win.log("round %d: no session" % r)
            time.sleep(interval)
            continue
        s,b = t
        sess = win.Sess(s,b)
        for c in cmds:
            sess.cmd(c, quiet=0.4)
            if sess.dead: break
        try: s.close()
        except Exception: pass
        win.log("round %d done" % r)
        time.sleep(interval)

if __name__ == "__main__":
    main()
