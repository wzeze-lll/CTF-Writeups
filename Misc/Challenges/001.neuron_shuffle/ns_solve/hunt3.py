import numpy as np, sys, targets
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
T=targets.TARGETS
hits=[]
for seed in range(start,NMAX,step):
    x=np.abs(np.random.RandomState(seed).randn(32)*0.6)
    for name,tv,ts in T:
        L=len(tv)
        if abs(float(x[:L].sum())-ts)<1e-9 and np.allclose(np.sort(x[:L]),tv,rtol=0,atol=1e-12):
            print('HIT',seed,name,flush=True); hits.append((seed,name))
print('worker',start,'done',hits,flush=True)
