import time, select, hmac, hashlib, json
from ws import connect, recv_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
SEED=bytes.fromhex("9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48")
H=lambda m: hmac.new(SEED,m.encode(),hashlib.sha256).hexdigest()
lines=[
 f"IDENTIFY {TOK}", f"IDENTIFY ops {TOK}", f"IDENTIFY admin {TOK}", f"IDENTIFY {TOK} ops",
 f"IDENTIFY ops:{TOK}", f"AUTH {TOK}", f"AUTH ops {TOK}", f"AUTH admin {TOK}", f"AUTH {TOK} ops",
 f"TOKEN {TOK}", f"LOGIN ops {TOK}", f"IDENTIFY {H('ops')}", f"IDENTIFY ops {H('ops')}",
 f"AUTH {H('ops')}", f"AUTH ops {H('ops')}", f"IDENTIFY {H(TOK)}", f"AUTH {H(TOK)}",
 f"IDENTIFY {SEED.hex()}", f"AUTH {SEED.hex()}", f"IDENTIFY ops {SEED.hex()}",
 json.dumps({"type":"identify","token":TOK,"role":"ops"}),
 json.dumps({"type":"auth","token":TOK}),
 json.dumps({"type":"identify","partner":"ops","token":H("ops")}),
]
for ln in lines:
    try:
        s,resp=connect(); s.setblocking(False)
        t0=time.time(); frames=[]
        while time.time()-t0<0.3:
            r,_,_=select.select([s],[],[],0.05)
            if r:
                try: frames.append(recv_frame(s)[1])
                except Exception: break
        s.sendall((ln+"\n").encode())
        end=time.time()+2.5; closed=None
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try:
                    o,d=recv_frame(s); frames.append((o,d[:120]))
                    if o==8: closed="close"; break
                except Exception: closed="EOF"; break
        extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
        print(f"{ln[:48]:50s} closed={closed} extra={extra}",flush=True)
        s.close()
    except Exception as e: print(ln[:40],"EXC",str(e)[:40])
