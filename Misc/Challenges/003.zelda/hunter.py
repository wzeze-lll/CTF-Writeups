#!/usr/bin/env python3
"""Persistent hunter: grab a live session, run a staged command batch, log everything."""
import socket, time, sys, os, datetime

HOST = os.environ.get("ZH", "127.0.0.1")
PORT = int(os.environ.get("ZP", "26732"))
LOG = os.environ.get("ZLOG", "hunt.log")

STAGES = {
 "recon": ["help", "mw show", "inv list", "shop list", "map show"],
 "money": ["mw show", "shop buy 3 -1", "mw show", "inv list", "shop buy 2 1", "mw show", "inv list"],
 "battle": ["mw show", "map teleport castle", "map show", "battle", "attack", "attack", "attack"],
 "uaf": ["mw show", "inv list", "inv equip 0", "mw show", "mw throw 0", "mw show", "inv list"],
 "whisper": ["mw show", "inv list", "inv equip 0", "mw whisper 0 41424344", "mw show", "inv list"],
 "buy1": ["mw show", "shop buy 0 1", "inv list", "inv equip 1", "mw show"],
}

def log(msg):
    line = datetime.datetime.now().strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def grab():
    s = socket.socket(); s.settimeout(3)
    try:
        s.connect((HOST, PORT))
    except Exception:
        s.close(); return None
    s.settimeout(0.8)
    buf = b""; t0 = time.time()
    while time.time() - t0 < 2.0:
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
            return s, buf
    s.close(); return None

def drain(s, quiet=0.35, total=3.0):
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
            buf += b"<EOF>"; break
        buf += d
    return buf

def run_session(s, banner, stage):
    log("==== SESSION (%s) ====" % stage)
    log(banner.decode("utf-8", "replace"))
    for c in STAGES[stage]:
        log(">>> " + c)
        try:
            s.sendall(c.encode() + b"\n")
        except Exception as e:
            log("[send err] %s" % e); break
        time.sleep(0.05)
        out = drain(s)
        log(out.decode("utf-8", "replace"))
        if b"<EOF>" in out:
            log("[server closed]")
            break
    s.close()

def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "recon"
    tries = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
    log("hunt start stage=%s host=%s:%d" % (stage, HOST, PORT))
    for i in range(tries):
        r = grab()
        if r:
            log("HIT on try %d" % i)
            run_session(r[0], r[1], stage)
            time.sleep(1)
        else:
            if i % 20 == 0:
                log("try %d ..." % i)
        time.sleep(2.5)

if __name__ == "__main__":
    main()
