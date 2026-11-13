import numpy as np, sys
start,step,NMAX,N=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
T=np.load('all926.npy'); n=len(T)
best=(0,None); hits=[]
for seed in range(start,NMAX,step):
    z=np.sort(np.abs(np.random.RandomState(seed).randn(N)*0.6))
    idx=np.searchsorted(z,T)
    idx=np.clip(idx,1,N-1)
    d=np.minimum(np.abs(z[idx]-T),np.abs(z[idx-1]-T))
    score=int((d<1e-13).sum())
    if score>best[0]: best=(score,seed)
    if score==n:
        print('HIT subset',seed,'N=',N,flush=True); hits.append(seed)
print(f'subset-worker start={start} N={N} done hits={hits} best_match={best}',flush=True)
