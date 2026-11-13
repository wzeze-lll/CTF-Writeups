import time, select
from ws import connect, recv_frame
def trial(label, payload, cap=10):
    try:
        s,resp=connect(); s.setblocking(False)
        t0=time.time(); frames=[]
        while time.time()-t0<0.3:
            r,_,_=select.select([s],[],[],0.05)
            if r:
                try: frames.append(recv_frame(s)[1])
                except Exception: break
        s.sendall(payload)
        closed=None
        while time.time()<t0+cap:
            r,_,_=select.select([s],[],[],0.2)
            if r:
                try:
                    o,d=recv_frame(s); frames.append((o,d[:120]))
                    if o==8: closed="close"; break
                except Exception: closed="EOF"; break
        extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
        print(f"{label:44s} closed={closed} extra={extra}",flush=True)
        s.close()
    except Exception as e: print(label,"EXC",str(e)[:50])
trial("ident+sub one write", b"IDENTIFY guest\nSUBSCRIBE rates\n")
trial("sub only one write", b"SUBSCRIBE rates\n")
trial("lower one write", b"identify guest\nsubscribe rates\n")
trial("json one write", b'{"type":"identify","id":"guest"}\n{"type":"subscribe","feed":"rates"}\n')
trial("ident+ledger", b"IDENTIFY guest\nSUBSCRIBE ledger\n")
