import torch, numpy as np, sys, targets
torch.set_num_threads(1)
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
T=targets.TARGETS; TS=np.load('all926.npy'); TSS=float(TS.sum())
hits=[]
for seed in range(start,NMAX,step):
    torch.manual_seed(seed)
    z=np.abs(torch.randn(32,dtype=torch.float64).numpy()*0.6)
    for name,tv,ts in T:
        L=len(tv)
        if abs(float(z[:L].sum())-ts)<1e-9 and np.allclose(np.sort(z[:L]),tv,rtol=0,atol=1e-12):
            print('HIT-block',seed,name,flush=True); hits.append((seed,name))
    if seed%200000==0:
        torch.manual_seed(seed)
        w=np.sort(np.abs(torch.randn(926,dtype=torch.float64).numpy()*0.6))
        if np.allclose(w,TS,rtol=1e-11,atol=1e-13): print('HIT-set',seed,flush=True); hits.append((seed,'set'))
print('torch-worker',start,'done',hits,flush=True)
