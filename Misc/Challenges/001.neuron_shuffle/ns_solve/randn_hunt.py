import numpy as np
d=np.load('model_A.npz')
tg=[]
for name,nn in [('k7',10),('k4',12),('k3',14),('k0',16)]:
    a=np.sort(np.abs(np.unique(d[name].astype(np.float64))))
    tg.append((name,a,float(a.sum())))
print('targets',[(t[0],len(t[1])) for t in tg],flush=True)
hits=[]
NMAX=50000000
for seed in range(NMAX):
    x=np.abs(np.random.RandomState(seed).randn(16)*0.6)
    for name,tv,ts in tg:
        L=len(tv)
        if abs(float(x[:L].sum())-ts)<1e-9 and np.allclose(np.sort(x[:L]),tv,rtol=0,atol=1e-12):
            print('HIT',seed,name,flush=True); hits.append((seed,name))
    if seed and seed%10000000==0: print('.',seed,flush=True)
print('done',hits,flush=True)
