import numpy as np, hashlib, sys
V="cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"
def ok(c):
    b=hashlib.sha256(c.encode()).hexdigest()[:32]
    return hashlib.sha256(("ns::"+b).encode()).hexdigest()==V
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
dims=(32,40,48); hits=[]
for seed in range(start,NMAX,step):
    # default_rng: permutation 序列
    r=np.random.default_rng(seed)
    p=[r.permutation(n) for n in dims]
    for order in ((0,1,2),(2,1,0)):
        for base in (0,1):
            if ok(";".join(",".join(str(int(x)+base) for x in p[i]) for i in order)):
                print('HIT dr',seed,order,base,flush=True); hits.append(('dr',seed,order,base))
    # default_rng: argsort(random)
    r=np.random.default_rng(seed)
    q=[np.argsort(r.random(n)) for n in dims]
    for order in ((0,1,2),(2,1,0)):
        for base in (0,1):
            if ok(";".join(",".join(str(int(x)+base) for x in q[i]) for i in order)):
                print('HIT drr',seed,order,base,flush=True); hits.append(('drr',seed,order,base))
    # RandomState: permutation
    r=np.random.RandomState(seed % (2**32))
    s=[r.permutation(n) for n in dims]
    for order in ((0,1,2),(2,1,0)):
        for base in (0,1):
            if ok(";".join(",".join(str(int(x)+base) for x in s[i]) for i in order)):
                print('HIT rs',seed,order,base,flush=True); hits.append(('rs',seed,order,base))
    # RandomState: argsort(rand)
    r=np.random.RandomState(seed % (2**32))
    t=[np.argsort(r.random_sample(n)) for n in dims]
    for order in ((0,1,2),(2,1,0)):
        for base in (0,1):
            if ok(";".join(",".join(str(int(x)+base) for x in t[i]) for i in order)):
                print('HIT rsr',seed,order,base,flush=True); hits.append(('rsr',seed,order,base))
print('permseed-worker',start,'done',hits,flush=True)
