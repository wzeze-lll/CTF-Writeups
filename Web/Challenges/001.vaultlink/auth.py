import time, select, base64
from ws import connect, recv_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
SEED="9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48"
cases={
 "basic ops:ops": {"Authorization":"Basic "+base64.b64encode(b"ops:ops").decode()},
 "basic ops:TOK": {"Authorization":"Basic "+base64.b64encode(f"ops:{TOK}".encode()).decode()},
 "basic admin:TOK": {"Authorization":"Basic "+base64.b64encode(f"admin:{TOK}".encode()).decode()},
 "basic rates:TOK": {"Authorization":"Basic "+base64.b64encode(f"rates.partner-forex.example.com:{TOK}".encode()).decode()},
 "bearer TOK": {"Authorization":"Bearer "+TOK},
 "bearer SEED": {"Authorization":"Bearer "+SEED},
 "x-api-key TOK": {"X-Api-Key":TOK},
 "cookie partner": {"Cookie":"partner=ops; role=admin"},
 "cookie session": {"Cookie":f"vault_session={TOK}"},
}
for name,h in cases.items():
    try:
        s,resp=connect(extra_headers=h); s.setblocking(False)
        out=[]; end=time.time()+1.0
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        print(f"{name:24s}", out)
    except Exception as e:
        print(name,"EXC",e)
