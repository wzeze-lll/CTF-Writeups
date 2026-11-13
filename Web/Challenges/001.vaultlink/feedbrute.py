import time, select
from ws import connect, recv_frame
feeds=["rates","rate","fx","forex","reference","reference-rates","reference_rates","refrates",
"settlement","settlements","settlement-window","settlement_windows","window","windows",
"ledger","ledgers","ledger-summary","ledger_summary","summary","summaries","balance","balances",
"position","positions","account","accounts","book","books","vault","core","internal","admin",
"ops","debug","all","*","#","default","main","public","partner","feed","data","v1","v2"]
def trial(feed, prefix):
    try:
        s,resp=connect(); s.setblocking(False)
        t0=time.time()
        while time.time()-t0<0.25:
            r,_,_=select.select([s],[],[],0.04)
            if r:
                try: recv_frame(s)
                except Exception: break
        if prefix:
            s.sendall(("IDENTIFY guest\n").encode()); time.sleep(0.15)
        s.sendall((f"SUBSCRIBE {feed}\n").encode())
        end=time.time()+2.6; frames=[]
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.12)
            if r:
                try:
                    o,d=recv_frame(s); frames.append((o,d[:80]))
                    if o==8: break
                except Exception: frames.append("EOF"); break
        s.close()
        extra=[f for f in frames if f[1]!=b'READY guest' and not f[1].startswith(b'SESSION')]
        if extra: print("HIT",feed,prefix,extra,flush=True)
        return bool(extra)
    except Exception: return False
hits=0
for f in feeds:
    for pre in [False, True]:
        if trial(f,pre): hits+=1
print("done hits",hits)
