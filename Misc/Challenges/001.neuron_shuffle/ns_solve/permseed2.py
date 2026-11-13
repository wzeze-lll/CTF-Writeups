import numpy as np, hashlib, sys, random
V="cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"
def ok(c):
    b=hashlib.sha256(c.encode()).hexdigest()[:32]
    return hashlib.sha256(("ns::"+b).encode()).hexdigest()==V
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
dims=(32,40,48); hits=[]
def chk(ls,tag,seed):
    for order in ((0,1,2),(2,1,0)):
        for base in (0,1):
            if ok(";".join(",".join(str(int(x)+base) for x in ls[i]) for i in order)):
                print('HIT',tag,seed,order,base,flush=True); hits.append((tag,seed,order,base))
BG=[('mt19937',np.random.MT19937),('philox',np.random.Philox),('sfc64',np.random.SFC64),('pcgdxsm',np.random.PCG64DXSM)]
for seed in range(start,NMAX,step):
    # python random
    r=random.Random(seed); ls=[]
    for n in dims:
        p=list(range(n)); r.shuffle(p); ls.append(p)
    chk(ls,'py',seed)
    # numpy 其它 BitGenerator
    for nm,B in BG:
        try:
            g=np.random.Generator(B(seed)); chk([g.permutation(n) for n in dims],nm,seed)
        except Exception: pass
print('permseed2-worker',start,'done',hits,flush=True)
