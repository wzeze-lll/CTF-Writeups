import numpy as np, sys
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
M=np.load('all926.npy'); M=np.sort(np.concatenate([M,-M]))  # 保留符号：用原始值集合
d=np.load('model_A.npz')
raw=np.sort(np.concatenate([np.array(d[f'k{i}'],dtype=np.float64).ravel() for i in range(8)]))
# 目标：模型的全体 5384 个值（含重复）排序
MS=raw; n=len(MS)
hits=[];cnt=0
for seed in range(start,NMAX,step):
    z=np.sort(np.random.RandomState(seed).randn(n))
    a,b=np.polyfit(z,MS,1)
    resid=float(np.max(np.abs(a*z+b-MS)))
    if resid<1e-9:
        print('HIT linear',seed,'a=%.6f b=%.6f'%(a,b),flush=True); hits.append((seed,a,b))
    cnt+=1
print('lin-worker',start,'done',hits,flush=True)
