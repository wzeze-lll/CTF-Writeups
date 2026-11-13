import numpy as np, sys
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
MS=np.load('signed926.npy'); n=len(MS)
hits=[]
for seed in range(start,NMAX,step):
    z=np.sort(np.random.RandomState(seed).randn(n))
    a,b=np.polyfit(z,MS,1)
    if float(np.max(np.abs(a*z+b-MS)))<1e-10:
        print('HIT-linear',seed,'a=%.9f b=%.9f'%(a,b),flush=True); hits.append((seed,a,b))
    # 另测：纯缩放（b=0）与纯平移（a=1）
    if float(np.max(np.abs(a*z-MS)))<1e-10 or float(np.max(np.abs(z+b-MS)))<1e-10:
        print('HIT-simple',seed,flush=True); hits.append((seed,'simple'))
print('lin2-worker',start,'done',hits,flush=True)
