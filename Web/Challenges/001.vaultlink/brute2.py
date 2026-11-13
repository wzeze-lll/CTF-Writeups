import time, select, hmac, hashlib, json
from ws import connect, send_frame, recv_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
SEED=bytes.fromhex("9b62aed8c3d31cc08cb70535ee8917176125acc68bf3191617773c452d16cc48")

def h(k,m): return hmac.new(k,m.encode(),hashlib.sha256).hexdigest()

msgs=[]
for partner in ["guest","ops","admin","rates.partner-forex.example.com","partner"]:
    msgs += [f"IDENTIFY {partner}", f"identify {partner}", f"HELLO {partner}", f"HELLO {partner} "]
for feed in ["rates","settlement","settlements","ledger","summary","ledger_summary","all"]:
    msgs += [f"SUBSCRIBE {feed}", f"sub {feed}", f"subscribe {feed}", f"SUB {feed}",
             f"STREAM {feed}", f"FEED {feed}",
             json.dumps({"cmd":"subscribe","feed":feed}),
             json.dumps({"type":"subscribe","feed":feed}),
             json.dumps({"op":"subscribe","feed":feed}),
             json.dumps({"action":"subscribe","feed":feed}),
             json.dumps({"method":"subscribe","params":[feed]}),
             json.dumps({"jsonrpc":"2.0","id":1,"method":"subscribe","params":[feed]})]
msgs += ["HELP","help","PING","PONG","STATUS","FEEDS","LIST","WHOAMI",
         f"AUTH {TOK}", f"AUTH admin {TOK}", f"AUTH ops {TOK}",
         json.dumps({"cmd":"auth","token":TOK}), json.dumps({"type":"auth","token":TOK})]

found=[]
for m in msgs:
    try:
        s,resp=connect(); s.setblocking(False)
        out=[]; end=time.time()+0.4
        sid=None
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.08)
            if r:
                try:
                    op,d=recv_frame(s); out.append(d)
                    if d.startswith(b"SESSION"): sid=d.split()[-1].decode()
                except Exception: break
        # variants that depend on session id
        cands=[m]
        if sid:
            cands.append(f"AUTH {h(SEED,sid)}")
            cands.append(f"IDENTIFY {sid} {h(SEED,sid)}")
            cands.append(json.dumps({"cmd":"auth","sig":h(SEED,sid),"session":sid}))
        for c in cands:
            send_frame(s,c)
            end=time.time()+0.6
            while time.time()<end:
                r,_,_=select.select([s],[],[],0.08)
                if r:
                    try: out.append(recv_frame(s)[1])
                    except Exception: out.append(b"EOF"); break
        s.close()
        extra=[x for x in out if not x.startswith(b"SESSION") and x!=b"READY guest"]
        if extra:
            found.append((m,extra)); print("HIT",m,extra, flush=True)
    except Exception as e:
        pass
print("done, hits:",len(found))
