import time, select, hmac, hashlib, base64
from ws import connect, recv_frame
SEED=bytes.fromhex("9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48")
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
def hx(m): return hmac.new(SEED,m.encode(),hashlib.sha256).hexdigest()
base="http://rates.partner-forex.example.com"
creds=[
 ("ops",hx("ops")),("admin",hx("admin")),("ops",TOK),("admin",TOK),
 ("ops","ops"),("admin","admin"),("rates.partner-forex.example.com",hx("rates.partner-forex.example.com")),
 ("app",hx("app")),("partner",hx("partner")),
]
for u,p in creds:
    inner=f"{base}\\{u}:{p}@127.0.0.1:8081/ws"
    try:
        s,resp=connect(inner=inner); s.setblocking(False)
        out=[]; end=time.time()+1.0
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        print(f"{u[:20]}:{p[:12]}... -> {resp.split(chr(13)+chr(10))[0]} {out}")
    except Exception as e: print(u,"EXC",str(e)[:50])
