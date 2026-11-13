import hashlib, sys, itertools
V="cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"
def ok(s):
    b=hashlib.sha256(s.encode()).hexdigest()[:32]
    return hashlib.sha256(("ns::"+b).encode()).hexdigest()==V
mode=sys.argv[1]; shard=int(sys.argv[2]); nsh=int(sys.argv[3])
hits=[]
if mode=='quad':
    for a in range(shard,101,nsh):
        sa=str(a)
        for b in range(101):
            sab=sa+";"+str(b)
            for c in range(101):
                sabc=sab+";"+str(c)
                for dd in range(101):
                    if ok(sabc+";"+str(dd)): print('HIT',a,b,c,dd,flush=True); hits.append((a,b,c,dd))
elif mode=='pent':
    for a in range(shard,41,nsh):
        sa=str(a)
        for b in range(41):
            sab=sa+";"+str(b)
            for c in range(41):
                sabc=sab+";"+str(c)
                for dd in range(41):
                    sabd=sabc+";"+str(dd)
                    for e in range(41):
                        if ok(sabd+";"+str(e)): print('HIT',a,b,c,dd,e,flush=True); hits.append((a,b,c,dd,e))
print(mode,'shard',shard,'done',hits,flush=True)
