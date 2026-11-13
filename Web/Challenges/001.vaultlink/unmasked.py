import time, select, struct
from ws import connect, recv_frame
def frame(data, op=1, masked=False, maskkey=b"\x00\x00\x00\x00"):
    ln=len(data); h=bytes([0x80|op])
    mb=0x80 if masked else 0
    if ln<126: h+=bytes([mb|ln])
    elif ln<65536: h+=bytes([mb|126])+struct.pack(">H",ln)
    else: h+=bytes([mb|127])+struct.pack(">Q",ln)
    if masked:
        return h+maskkey+bytes(x^maskkey[i%4] for i,x in enumerate(data))
    return h+data
def trial(label, payloads, masked, gap=0.7, cap=6):
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
                s.sendall(frame(payloads[i],1,masked)); i+=1; nxt=time.time()+gap
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try:
                    o,d=recv_frame(s); frames.append((o,d[:80]))
                    if o==8: closed=time.time()-t0; break
                except Exception:
                    closed=time.time()-t0; break
        extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
        print(f"{label:44s} sent={i} closed={round(closed,1) if closed else '>6'} extra={extra}",flush=True)
        s.close()
    except Exception as e:
        print(label,"EXC",str(e)[:60],flush=True)
for masked in [False, True]:
    trial(f"hello x5 masked={masked}", [b"hello"]*5, masked)
    trial(f"ident/sub masked={masked}", [b"IDENTIFY guest", b"SUBSCRIBE rates", b"SUBSCRIBE rates"], masked)
