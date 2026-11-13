import numpy as np, hashlib, sys
V="cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"
def body(c): return hashlib.sha256(c.encode()).hexdigest()[:32]
def ok(c): return hashlib.sha256(("ns::"+body(c)).encode()).hexdigest()==V
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
D=(32,40,48); hits=[]; cnt=0
for seed in range(start,NMAX,step):
    r=np.random.default_rng(seed)
    p=[r.permutation(n) for n in D]
    for order in ((0,1,2),(2,1,0)):
        for base in (0,1):
            cnt+=1
            if ok(";".join(",".join(str(int(x)+base) for x in p[i]) for i in order)): hits.append(('dr',seed,order,base)); print('HIT dr',seed,order,base,flush=True)
    r=np.random.RandomState(seed % (2**32))
    q=[r.permutation(n) for n in D]
    for order in ((0,1,2),(2,1,0)):
        for base in (0,1):
            cnt+=1
            if ok(";".join(",".join(str(int(x)+base) for x in q[i]) for i in order)): hits.append(('rs',seed,order,base)); print('HIT rs',seed,order,base,flush=True)
    if seed and seed % 2000000 == 0: print('.',seed,flush=True)
print('pl-worker',start,'done',cnt,hits,flush=True)
