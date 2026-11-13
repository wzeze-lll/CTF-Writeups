#!/usr/bin/env python3
"""Resilient client for the Zelda/One-Ring CTF service."""
import socket, time, sys

HOST, PORT = "127.0.0.1", 26732
BANNER_MARK = b"Hero starts at Great Plateau"

class Game:
    def __init__(self, tries=60):
        self.s = None
        self.buf = b""
        for i in range(tries):
            if self._try_connect():
                return
        raise RuntimeError("connect failed")

    def _try_connect(self):
        s = socket.socket()
        s.settimeout(6)
        try:
            s.connect((HOST, PORT))
        except Exception:
            s.close(); time.sleep(1); return False
        time.sleep(0.35)
        s.settimeout(1.2)
        data = b""
        try:
            while True:
                d = s.recv(65536)
                if not d:
                    break
                data += d
                if BANNER_MARK in data:
                    break
        except socket.timeout:
            pass
        except Exception:
            pass
        if BANNER_MARK in data:
            self.s = s
            self.buf = data
            return True
        s.close()
        time.sleep(1.0)
        return False

    def recv_all(self, quiet=0.45, total=4.0):
        self.s.settimeout(quiet)
        data = b""
        end = time.time() + total
        while time.time() < end:
            try:
                d = self.s.recv(65536)
                if not d:
                    break
                data += d
            except socket.timeout:
                break
            except Exception:
                break
        self.buf += data
        return data

    def cmd(self, line, quiet=0.45):
        if self.s is None:
            raise RuntimeError("closed")
        self.s.sendall(line.encode() + b"\n")
        time.sleep(0.08)
        return self.recv_all(quiet=quiet).decode("utf-8", "replace")

    def close(self):
        if self.s:
            try: self.s.close()
            except Exception: pass
            self.s = None

if __name__ == "__main__":
    g = Game()
    print("[banner]", g.buf.decode("utf-8", "replace"))
    for line in sys.argv[1:]:
        print(">>>", line)
        try:
            print(g.cmd(line))
        except Exception as e:
            print("[err]", e); break
    g.close()
