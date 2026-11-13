#!/usr/bin/env python3
import os, sys, time
os.environ.setdefault("ZH","127.0.0.1"); os.environ.setdefault("ZP","36943")
os.environ.setdefault("ZLOG","run.log")
import win

def get_session(tries=40):
    for i in range(tries):
        r = win.grab()
        if r: return r
        time.sleep(1.5)
    return None

def main():
    cmds = sys.argv[1:]
    r = get_session()
    if not r:
        print("no session"); return 1
    s,b = r
    sess = win.Sess(s,b)
    for c in cmds:
        out = sess.cmd(c)
        if sess.dead:
            break
    try: s.close()
    except Exception: pass
    return 0

if __name__ == "__main__":
    sys.exit(main())
