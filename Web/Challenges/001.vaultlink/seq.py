import time, select
from ws import connect, recv_frame, send_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
def trial(label, payloads, gap=0.8, cap=8):
    try:
        s,resp=connect(); s.setblocking(False)
        t0=time.time(); frames=[]
        while time.time()-t0<0.4:
            r,_,_=select.select([s],[],[],0.05)
            if r:
                try: frames.append(recv_frame(s)[1])
                except Exception: break
        i=0; closed=None; nxt=t0+0.2
        while time.time()-t0<cap:
            if i<len(payloads) and time.time()>=nxt:
                send_frame(s,payloads[i]); i+=1; nxt=time.time()+gap
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try:
                    o,d=recv_frame(s); frames.append((o,d[:60]))
                    if o==8: closed=time.time()-t0; break
                except Exception:
                    closed=time.time()-t0; break
        print(f"{label:46s} sent={i} closed={round(closed,1) if closed else '>8'} frames={[f for f in frames if f not in (b'READY guest',) and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]}",flush=True)
        s.close()
    except Exception as e:
        print(label,"EXC",str(e)[:60],flush=True)
trial("1 msg", [b"hello"])
trial("2 msgs", [b"hello", b"hello"])
trial("3 msgs", [b"hello"]*3)
trial("ident,sub", [b"IDENTIFY guest", b"SUBSCRIBE rates"])
trial("ident,sub,sub", [b"IDENTIFY guest", b"SUBSCRIBE rates", b"SUBSCRIBE rates"])
trial("json ident,sub", [b'{"type":"identify","id":"guest"}', b'{"type":"subscribe","feed":"rates"}', b'{"type":"subscribe","feed":"rates"}'])
trial("auth x3", [b"AUTH "+TOK.encode()]*3)
trial("sub x3", [b"SUBSCRIBE rates"]*3)
