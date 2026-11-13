import numpy as np, sys
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
T=np.load('all926.npy'); TS=float(T.sum()); n=len(T)
hit=[]
for seed in range(start,NMAX,step):
    z=np.sort(np.abs(np.random.RandomState(seed).randn(n)*0.6))
    if np.allclose(z,T,rtol=1e-11,atol=1e-13):
        print('HIT-seed',seed,'(scale 0.6 全体匹配)',flush=True); hit.append(seed)
        continue
    s=TS/float(np.abs(z).sum())
    if np.allclose(z*s,T,rtol=1e-9,atol=1e-12):
        print('HIT-seed',seed,'scale=%.6f'%s,flush=True); hit.append((seed,s))
print('set-worker',start,'done',hit,flush=True)
