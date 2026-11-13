import time, select, struct
from ws import connect, recv_frame
def uframe(p, op=1):
    ln=len(p)
    if ln<126: return bytes([0x80|op, ln])+p
    elif ln<65536: return bytes([0x80|op,126])+struct.pack(">H",ln)+p
    else: return bytes([0x80|op,127])+struct.pack(">Q",ln)+p
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
def trial(label, msgs, cap=6):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: frames.append(recv_frame(s)[1])
            except Exception: break
    for m in msgs:
        s.sendall(uframe(m)); time.sleep(0.25)
    closed=None
    while time.time()<t0+cap:
        r,_,_=select.select([s],[],[],0.15)
        if r:
            try:
                o,d=recv_frame(s); frames.append((o,d[:120]))
                if o==8: closed="close"; break
            except Exception: closed="EOF"; break
    extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
    print(f"{label:34s} closed={closed} extra={extra}",flush=True)
    s.close()
trial("ident+sub unmasked", [b"IDENTIFY guest", b"SUBSCRIBE rates"])
trial("sub only unmasked", [b"SUBSCRIBE rates"])
trial("auth unmasked", [b"AUTH "+TOK.encode()])
trial("auth+sub unmasked", [b"AUTH "+TOK.encode(), b"SUBSCRIBE ledger"])
trial("json unmasked", [b'{"type":"subscribe","feed":"rates"}'])
