import numpy as np, sys, targets
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
T=targets.TARGETS
hit=[]
for seed in range(start,NMAX,step):
    z=np.abs(np.random.RandomState(seed).randn(32))
    for name,tv,ts in T:
        L=len(tv); sl=z[:L]
        ssum=float(sl.sum())
        if ssum<=0: continue
        s=ts/ssum
        cand=np.sort(sl)*s
        if np.allclose(cand,tv,rtol=1e-10,atol=1e-13):
            print('HIT',seed,name,'scale=%.6f'%s,flush=True); hit.append((seed,name,s))
print('scale-free worker',start,'done',hit,flush=True)
