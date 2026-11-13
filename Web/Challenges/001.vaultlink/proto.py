import time, select
from ws import connect, send_frame, recv_frame
cases=[
 ("sub v2", {"Sec-WebSocket-Protocol":"v2"}),
 ("sub vaultlink.v2", {"Sec-WebSocket-Protocol":"vaultlink.v2"}),
 ("sub v1,v2", {"Sec-WebSocket-Protocol":"v1, v2"}),
 ("deflate", {"Sec-WebSocket-Extensions":"permessage-deflate"}),
 ("deflate+v2", {"Sec-WebSocket-Extensions":"permessage-deflate","Sec-WebSocket-Protocol":"v2"}),
 ("origin", {"Origin":"https://partner.vaultlink.example"}),
]
for name,h in cases:
    try:
        s,resp=connect(extra_headers=h); s.setblocking(False)
        out=[]; end=time.time()+1.2
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s))
                except Exception: out.append("EOF"); break
        print("==",name,"\n",resp.strip().replace("\r\n"," | "),"\n  frames:",out)
        s.close()
    except Exception as e: print(name,"EXC",e)
