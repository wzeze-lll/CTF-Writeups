#!/usr/bin/env python3
"""Start local bad_puppet, feed commands, print output."""
import subprocess, socket, time, os, sys, signal

BIN = os.path.expanduser("~/bp/bad_puppet/bad_puppet/bad_puppet")
CWD = os.path.dirname(BIN)

def start():
    try:
        subprocess.run(["pkill", "-f", "bad_puppet"], check=False)
    except Exception:
        pass
    time.sleep(0.3)
    p = subprocess.Popen([BIN], cwd=CWD, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        s = socket.socket(); s.settimeout(0.3)
        try:
            s.connect(("127.0.0.1", 31337)); s.close(); break
        except Exception:
            time.sleep(0.1)
        finally:
            try: s.close()
            except Exception: pass
    return p

def main():
    cmds = [l.rstrip("\n") for l in sys.stdin if l.strip()]
    p = start()
    s = socket.socket(); s.settimeout(3); s.connect(("127.0.0.1", 31337))
    s.settimeout(0.35)
    def rd():
        b=b""
        while True:
            try: d=s.recv(65536)
            except Exception: break
            if not d: break
            b+=d
        return b.decode("utf-8","replace")
    time.sleep(0.2); print(rd(), flush=True)
    for c in cmds:
        try:
            s.sendall(c.encode()+b"\n")
        except Exception as e:
            print("[send err]", e); break
        time.sleep(0.1)
        out = rd()
        print(">>> " + c); print(out, flush=True)
        if not out and "quit" not in c:
            pass
    s.close()
    time.sleep(0.2)
    p.terminate()
    try: p.wait(timeout=2)
    except Exception: p.kill()

if __name__ == "__main__":
    main()
