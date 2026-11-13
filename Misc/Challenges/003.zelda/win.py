#!/usr/bin/env python3
"""Adaptive hunter + exploit chain for the Zelda/One-Ring CTF game."""
import socket, time, sys, os, re, datetime

HOST = os.environ.get("ZH", "127.0.0.1")
PORT = int(os.environ.get("ZP", "26732"))
LOG = os.environ.get("ZLOG", "win.log")

def log(msg):
    line = datetime.datetime.now().strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    try:
        with open(LOG, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

class Sess:
    def __init__(self, s, banner):
        self.s = s
        self.dead = False
        log("==== SESSION ====")
        log(banner.decode("utf-8", "replace").rstrip())

    def cmd(self, c, quiet=0.35):
        if self.dead:
            return ""
        log(">>> " + c)
        try:
            self.s.sendall(c.encode() + b"\n")
        except Exception as e:
            log("[send err] %s" % e); self.dead = True; return ""
        time.sleep(0.04)
        out = self.drain(quiet)
        txt = out.decode("utf-8", "replace")
        log(txt.rstrip())
        if "<EOF>" in txt:
            self.dead = True
        return txt

    def drain(self, quiet):
        self.s.settimeout(quiet)
        buf = b""; end = time.time() + 2.5
        while time.time() < end:
            try:
                d = self.s.recv(65536)
            except socket.timeout:
                break
            except Exception:
                break
            if not d:
                buf += b"<EOF>"; break
            buf += d
        return buf

    def rupees(self, txt):
        m = re.search(r"Rupees=(-?\d+)", txt)
        return int(m.group(1)) if m else None

def grab():
    s = socket.socket(); s.settimeout(2)
    try:
        s.connect((HOST, PORT))
    except Exception:
        s.close(); return None
    s.settimeout(0.35)
    buf = b""; t0 = time.time()
    while time.time() - t0 < 1.2:
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

def exploit(sess):
    st = sess.cmd("mw show")
    r = sess.rupees(st)
    log("[rupees] %s" % r)

    if r is None:
        return

    # Phase 1: money
    if r < 10000:
        for payload in ["shop buy 2 -1", "shop buy 0 -1", "shop buy 3 -1"]:
            if sess.dead: return
            sess.cmd(payload)
            st = sess.cmd("mw show")
            r2 = sess.rupees(st)
            log("[rupees after %s] %s" % (payload, r2))
            if r2 is None:
                return
            if r2 >= 10000:
                r = r2
                break

    if r >= 10000:
        out = sess.cmd("shop buy 2 1")
        log("[bought master sword attempt]")
        inv = sess.cmd("inv list")
        idx = None
        for line in inv.splitlines():
            if "Master Sword" in line:
                m = re.search(r"\[(\d+)\]", line)
                if m:
                    idx = int(m.group(1))
        log("[master sword idx] %s" % idx)
        if idx is not None:
            sess.cmd("inv equip %d" % idx)
            sess.cmd("mw show")

    # Phase 2: castle
    sess.cmd("map teleport castle")
    sess.cmd("map show")
    b = sess.cmd("battle")
    for i in range(40):
        if sess.dead: return
        out = sess.cmd("attack")
        if re.search(r"flag\{", out, re.I):
            log("[FLAG FOUND]")
            return
        if "EnemyDefeated=yes" in out or "defeated" in out.lower() or "Victory" in out:
            log("[enemy defeated]")
            break
        if "player_hp=0" in out or "Game Over" in out or "You died" in out:
            log("[player died]")
            break
    sess.cmd("mw show")
    sess.cmd("quit")

def main():
    log("win-hunter start %s:%d" % (HOST, PORT))
    n = 0
    while True:
        r = grab()
        n += 1
        if r:
            log("HIT try=%d" % n)
            sess = Sess(*r)
            try:
                exploit(sess)
            except Exception as e:
                log("[exploit err] %s" % e)
            try: sess.s.close()
            except Exception: pass
            time.sleep(20)
        else:
            if n % 20 == 0:
                log("try %d ..." % n)
            time.sleep(3)

if __name__ == "__main__":
    main()
