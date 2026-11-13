import time, select, hmac, hashlib, base64, json
from ws import connect, recv_frame, send_frame
SEED=bytes.fromhex("9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48")
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
def hx(m): return hmac.new(SEED,m.encode(),hashlib.sha256).hexdigest()
def b64(m): return base64.b64encode(hmac.new(SEED,m.encode(),hashlib.sha256).digest()).decode()
def trial(label, msgs, cap=4.0):
    try:
        s,resp=connect(); s.setblocking(False)
        t0=time.time(); frames=[]
        while time.time()-t0<0.35:
            r,_,_=select.select([s],[],[],0.05)
            if r:
                try: frames.append(recv_frame(s)[1])
                except Exception: break
        sid=None
        for f in frames:
            if isinstance(f,bytes) and f.startswith(b"SESSION"): sid=f.split()[-1].decode()
        i=0; closed=None
        for m in msgs:
            send_frame(s,m)
            end=time.time()+0.9
            while time.time()<end:
                r,_,_=select.select([s],[],[],0.1)
                if r:
                    try:
                        o,d=recv_frame(s); frames.append((o,d[:100]))
                        if o==8: closed=True; break
                    except Exception: closed=True; break
            if closed: break
            i+=1
        extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
        print(f"{label:52s} sent={i} extra={extra}",flush=True)
        s.close()
        return sid, extra
    except Exception as e:
        print(label,"EXC",str(e)[:50],flush=True); return None,None
# first get a session id
s,resp=connect(); s.setblocking(False)
time.sleep(0.3)
sid=None
try:
    while True:
        r,_,_=select.select([s],[],[],0.1)
        if not r: break
        d=recv_frame(s)[1]
        if d.startswith(b"SESSION"): sid=d.split()[-1].decode()
except Exception: pass
s.close()
print("sid sample",sid)
cands=[]
for name,h in [("hex",hx),("b64",b64)]:
    for m in ["guest","ops","admin",sid,"rates.partner-forex.example.com",f"guest:{sid}",f"{sid}:guest"]:
        cands.append((f"{name}({m[:14]})",h(m)))
msgsets=[]
for label,tok in cands:
    msgsets.append((f"IDENTIFY {sid} {label}", [f"IDENTIFY {sid} {tok}".encode(), b"SUBSCRIBE rates"]))
    msgsets.append((f"IDENTIFY {label}", [f"IDENTIFY {tok}".encode(), b"SUBSCRIBE rates"]))
msgsets.append(("IDENTIFY guest <TOK>", [f"IDENTIFY guest {TOK}".encode(), b"SUBSCRIBE rates"]))
msgsets.append(("IDENTIFY <TOK>", [f"IDENTIFY {TOK}".encode(), b"SUBSCRIBE rates"]))
for label,msgs in msgsets[:30]:
    trial(label,msgs)
