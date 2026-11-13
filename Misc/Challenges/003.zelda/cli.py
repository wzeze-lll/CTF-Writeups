#!/usr/bin/env python3
import socket, sys, time, re

HOST, PORT = "127.0.0.1", 26732

class C:
    def __init__(self):
        self.s = socket.socket()
        self.s.settimeout(6)
        self.s.connect((HOST, PORT))
        self.buf = b""
        self.s.settimeout(1.0)
        self.read_until_quiet()

    def read_until_quiet(self, quiet=0.8, total=6.0):
        end = time.time() + total
        last = time.time()
        data = b""
        while time.time() < end:
            try:
                d = self.s.recv(65536)
                if not d:
                    break
                data += d
                last = time.time()
            except socket.timeout:
                if time.time() - last > quiet:
                    break
                continue
            except Exception:
                break
        self.buf += data
        return data

    def send(self, line):
        self.s.sendall(line.encode() + b"\n")
        time.sleep(0.15)
        return self.read_until_quiet()

    def interactive(self):
        import threading
        def rd():
            while True:
                try:
                    d = self.s.recv(65536)
                    if not d:
                        print("\n[closed]"); return
                    sys.stdout.write(d.decode('utf-8', 'replace'))
                    sys.stdout.flush()
                except Exception:
                    return
        threading.Thread(target=rd, daemon=True).start()
        while True:
            try:
                line = input()
            except EOFError:
                break
            self.s.sendall(line.encode() + b"\n")

if __name__ == "__main__":
    c = C()
    print(c.buf.decode('utf-8', 'replace'))
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        c.interactive()
    else:
        for cmd in sys.argv[1:]:
            print(">>>", cmd)
            print(c.send(cmd).decode('utf-8', 'replace'))
