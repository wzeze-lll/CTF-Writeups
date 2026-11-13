import sys, time, select
from ws import connect, send_frame, recv_frame

s,resp=connect()
s.setblocking(False)
def drain(t=2.0):
    end=time.time()+t; out=[]
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.3)
        if r:
            try: out.append(recv_frame(s))
            except BlockingIOError: continue
            except Exception as e: out.append(("ERR",str(e))); break
    return out
print(resp)
print("initial:", drain(2))
for msg in sys.argv[1:]:
    send_frame(s,msg); print(">>",msg,"->",drain(2))
