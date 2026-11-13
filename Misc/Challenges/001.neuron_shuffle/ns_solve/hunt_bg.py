import numpy as np, sys, targets
kind,start,step,NMAX=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
BG={'mt':np.random.MT19937,'philox':np.random.Philox,'sfc':np.random.SFC64,'pcgdxsm':np.random.PCG64DXSM}[kind]
T=targets.TARGETS; hits=[]
for seed in range(start,NMAX,step):
    r=np.random.Generator(BG(seed))
    z=np.abs(r.standard_normal(32)*0.6)
    for name,tv,ts in T:
        L=len(tv)
        if abs(float(z[:L].sum())-ts)<1e-9 and np.allclose(np.sort(z[:L]),tv,rtol=0,atol=1e-12):
            print('HIT',kind,seed,name,flush=True); hits.append((seed,name))
print('bg-worker',kind,start,'done',hits,flush=True)
