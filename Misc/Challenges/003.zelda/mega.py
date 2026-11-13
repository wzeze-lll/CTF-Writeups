import os, sys, time, socket
os.environ["ZH"] = os.environ.get("ZH", "127.0.0.1")
os.environ["ZP"] = os.environ.get("ZP", "36943")
os.environ["ZLOG"] = os.environ.get("ZLOG", "mega.log")
import win
delay = float(sys.argv[1]) if len(sys.argv)>1 else 0
if delay: time.sleep(delay)
s=socket.socket(); s.settimeout(5)
try:
    s.connect((win.HOST,win.PORT))
except Exception as e:
    print("connect err", e); sys.exit(1)
s.settimeout(1.5)
b=b""
try:
    while True:
        d=s.recv(8192)
        if not d: break
        b+=d
        if b"Plateau" in b: break
except Exception: pass
print("BANNER", repr(b[:50]), flush=True)
if b"Plateau" in b:
    sess=win.Sess(s,b)
    for c in [l.strip() for l in open("mega.txt") if l.strip()]:
        sess.cmd(c, quiet=0.35)
        if sess.dead: break
    try: s.close()
    except Exception: pass
else:
    s.close()
