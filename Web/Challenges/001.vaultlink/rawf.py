import time, select, os, struct
from ws import connect, recv_frame
def send_raw(payload):
    pass
def trial(desc, raw):
    s,resp=connect(); s.setblocking(False)
    out=[]; end=time.time()+0.8
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s))
            except Exception: out.append("EOF"); break
    s.sendall(raw)
    end=time.time()+2.0
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s))
            except Exception: out.append("EOF"); break
        else:
            try:
                d=s.recv(4096)
                if not d: out.append("TCP-EOF"); break
                else: out.append(("raw",d[:50]))
            except Exception: pass
    print(desc,out); s.close()
trial("unmasked text", b"\x81\x05hello")
trial("opcode 3", bytes([0x83,0x80])+b"\x00\x00\x00\x00")
trial("bad rsv", bytes([0xC1,0x80])+b"\x00\x00\x00\x00")
