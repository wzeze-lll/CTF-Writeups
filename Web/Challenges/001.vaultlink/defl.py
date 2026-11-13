import zlib, os, struct, time, select
from ws import connect, recv_frame, GW, INNER

def frame(data, op=1, rsv1=True):
    c=zlib.compressobj(9, zlib.DEFLATED, -15)
    comp=c.compress(data)+c.flush(zlib.Z_SYNC_FLUSH)
    assert comp.endswith(b"\x00\x00\xff\xff")
    comp=comp[:-4]
    b1=(0x80 if rsv1 else 0)|op; ln=len(comp)
    k=os.urandom(4); m=bytes(x^k[i%4] for i,x in enumerate(comp))
    if ln<126: h=bytes([b1,0x80|ln])
    elif ln<65536: h=bytes([b1,0x80|126])+struct.pack(">H",ln)
    else: h=bytes([b1,0x80|127])+struct.pack(">Q",ln)
    return h+k+m

msgs=[b"hello", b"IDENTIFY guest", b"SUBSCRIBE rates", b'{"cmd":"subscribe","feed":"rates"}', b'{"cmd":"identify","id":"guest"}', b"AUTH guest"]
import socket
for msg in msgs:
    s,resp=connect(extra_headers={"Sec-WebSocket-Extensions":"permessage-deflate"}); s.setblocking(False)
    out=[]; end=time.time()+0.8
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s))
            except Exception: out.append("EOF"); break
    s.sendall(frame(msg))
    end=time.time()+2.0
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s))
            except Exception: out.append("EOF"); break
    print(msg, "->", out)
    s.close()
