import socket,time,sys
cmds=[l.rstrip("\n") for l in sys.stdin if l.strip()]
s=socket.socket(); s.settimeout(3); s.connect(("127.0.0.1",31337)); s.settimeout(0.35)
def rd():
    b=b""
    while True:
        try: d=s.recv(65536)
        except Exception: break
        if not d: break
        b+=d
    return b.decode("utf-8","replace")
time.sleep(0.2); print(rd(),flush=True)
for c in cmds:
    try: s.sendall(c.encode()+b"\n")
    except Exception as e: print("[send err]",e); break
    time.sleep(0.1); print(">>> "+c); print(rd(),flush=True)
s.close()
