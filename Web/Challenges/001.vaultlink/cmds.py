import time, select
from ws import connect, recv_frame
def one(cmd, cap=3.5):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: frames.append(recv_frame(s)[1])
            except Exception: break
    s.sendall(cmd+b"\n")
    while time.time()-t0<cap:
        r,_,_=select.select([s],[],[],0.15)
        if r:
            try:
                o,d=recv_frame(s); frames.append((o,d[:120]))
                if o==8: break
            except Exception: frames.append("EOF"); break
    extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
    print(f"{cmd.decode():28s} -> {extra}",flush=True)
    s.close()
for c in [b"IDENTIFY",b"identify",b"SUBSCRIBE",b"subscribe",b"AUTH",b"auth",b"HELP",b"help",b"PING",b"STATUS",b"FEEDS",b"LIST",b"WHOAMI",b"SESSION",b"SUBSCRIBE rates",b"SUBSCRIBE admin",b"SUBSCRIBE ledger"]:
    one(c)
