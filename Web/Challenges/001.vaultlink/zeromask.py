import time, select, os, struct
from ws import connect, recv_frame

def frame_zero(data, op=1):
    ln=len(data)
    h=bytes([0x80|op])
    if ln<126: h+=bytes([0x80|ln])
    elif ln<65536: h+=bytes([0x80|126])+struct.pack(">H",ln)
    else: h+=bytes([0x80|127])+struct.pack(">Q",ln)
    return h+b"\x00\x00\x00\x00"+data

msgs=[b"hello", b"IDENTIFY guest", b"SUBSCRIBE rates", b"SUBSCRIBE ledger",
      b"AUTH admin", b'{"cmd":"subscribe","feed":"rates"}', b"HELP"]
for m in msgs:
    s,resp=connect(); s.setblocking(False)
    out=[]; end=time.time()+0.6
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s)[1])
            except Exception: break
    s.sendall(frame_zero(m))
    end=time.time()+2.0
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s)[1])
            except Exception: out.append(b"EOF"); break
    print(m,"->",out)
    s.close()
