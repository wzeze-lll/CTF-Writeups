import time, select, os
from ws import connect, recv_frame
def frame(data):
    ln=len(data); k=os.urandom(4)
    h=bytes([0x81])+bytes([0x80|ln]) if ln<126 else None
    m=bytes(x^k[i%4] for i,x in enumerate(data))
    return h+k+m
def trial(label, data, cap=8):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: frames.append(recv_frame(s)[1])
            except Exception: break
    s.sendall(frame(data))
    closed=None
    while time.time()<t0+cap:
        r,_,_=select.select([s],[],[],0.15)
        if r:
            try:
                o,d=recv_frame(s); frames.append((o,d[:120]))
                if o==8: closed="close"; break
            except Exception: closed="EOF"; break
    extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
    print(f"{label:40s} closed={closed} extra={extra}",flush=True)
    s.close()
trial("one frame two lines", b"IDENTIFY guest\nSUBSCRIBE rates\n")
trial("one frame sub only", b"SUBSCRIBE rates")
trial("one frame json", b'{"type":"subscribe","feed":"rates"}')
trial("one frame auth+sub", b"AUTH 9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813\nSUBSCRIBE ledger\n")
