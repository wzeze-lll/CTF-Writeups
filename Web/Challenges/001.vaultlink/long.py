import time, select
from ws import connect, send_frame, recv_frame
s,resp=connect(); s.setblocking(False)
print(resp.strip().replace("\r\n"," | "))
t0=time.time(); sent=False
while time.time()-t0<25:
    r,_,_=select.select([s],[],[],0.2)
    if r:
        try:
            op,d=recv_frame(s); print(f"{time.time()-t0:5.1f}s frame {op} {d[:120]}")
            if op==8: break
        except Exception as e:
            print("closed",e); break
    if not sent and time.time()-t0>5:
        send_frame(s,b"SUBSCRIBE rates"); print("sent SUBSCRIBE"); sent=True
print("done")
