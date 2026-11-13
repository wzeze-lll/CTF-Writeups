import numpy as np, sys
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
d=np.load('model_A.npz')
TG=[]
for name,nn in [('k7',10),('k4',12),('k3',14),('k0',16)]:
    a=np.sort(np.abs(np.unique(d[name].astype(np.float64))))
    TG.append((name,a,float(a.sum())))
hits=[]; cnt=0
for seed in range(start,NMAX,step):
    x=np.abs(np.random.RandomState(seed).randn(16)*0.6)
    for name,tv,ts in TG:
        L=len(tv)
        if abs(float(x[:L].sum())-ts)<1e-9 and np.allclose(np.sort(x[:L]),tv,rtol=0,atol=1e-12):
            print('HIT',seed,name,flush=True); hits.append((seed,name))
    cnt+=1
    if cnt%2000000==0: print('.',seed,flush=True)
print('worker',start,'done hits',hits,flush=True)
