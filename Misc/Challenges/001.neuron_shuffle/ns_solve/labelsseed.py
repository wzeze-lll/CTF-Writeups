import numpy as np, hashlib, sys
V="cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"
def ok(c):
    b=hashlib.sha256(c.encode()).hexdigest()[:32]
    return hashlib.sha256(("ns::"+b).encode()).hexdigest()==V
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
hits=[]
for seed in range(start,NMAX,step):
    for rng_ctor in (lambda s: np.random.default_rng(s), lambda s: np.random.RandomState(s % (2**32))):
        for ranges in ((10,12,14),(10,11,13)):
            r=rng_ctor(seed)
            try:
                if isinstance(r,np.random.Generator):
                    ls=[r.integers(0,k,n) for k,n in zip(ranges,(32,40,48))]
                else:
                    ls=[r.randint(0,k,n) for k,n in zip(ranges,(32,40,48))]
            except Exception: continue
            for order in ((0,1,2),(2,1,0)):
                for base in (0,1):
                    if ok(";".join(",".join(str(int(x)+base) for x in ls[i]) for i in order)):
                        print('HIT',seed,ranges,order,base,flush=True); hits.append((seed,ranges,order,base))
print('labelsseed-worker',start,'done',hits,flush=True)
