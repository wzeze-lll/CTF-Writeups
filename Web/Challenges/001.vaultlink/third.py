import time, select
from ws import connect, recv_frame
def trial(label, msgs, cap=6):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: frames.append(recv_frame(s)[1])
            except Exception: break
    for m in msgs:
        s.sendall(m if isinstance(m,bytes) else m.encode())
        time.sleep(0.3)
    closed=None
    while time.time()<t0+cap:
        r,_,_=select.select([s],[],[],0.15)
        if r:
            try:
                o,d=recv_frame(s); frames.append((o,d[:120]))
                if o==8: closed="close"; break
            except Exception: closed="EOF"; break
    extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
    print(f"{label:22s} closed={closed} extra={extra}",flush=True)
    s.close()
for third in ["START\n","GO\n","ACK\n","READY\n","OK\n","STREAM\n","SUBSCRIBE\n","BEGIN\n","PULL\n","SEND\n"]:
    trial("id,sub,"+third.strip(), ["IDENTIFY guest\n","SUBSCRIBE rates\n",third])
