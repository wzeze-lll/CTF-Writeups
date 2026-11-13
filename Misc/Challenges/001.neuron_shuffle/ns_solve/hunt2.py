import numpy as np, multiprocessing as mp, sys
d=np.load('model_A.npz')
TG=[]
for name,nn in [('k7',10),('k4',12),('k3',14),('k0',16)]:
    a=np.sort(np.abs(np.unique(d[name].astype(np.float64))))
    TG.append((name,a,float(a.sum())))
NMAX=50_000_000
def work(args):
    start,step=args; out=[]
    for seed in range(start,NMAX,step):
        x=np.abs(np.random.RandomState(seed).randn(16)*0.6)
        for name,tv,ts in TG:
            L=len(tv)
            if abs(float(x[:L].sum())-ts)<1e-9 and np.allclose(np.sort(x[:L]),tv,rtol=0,atol=1e-12):
                out.append((seed,name))
    return out
if __name__=='__main__':
    W=4
    with mp.Pool(W) as p:
        res=p.map(work,[(i,W) for i in range(W)])
    hits=[h for r in res for h in r]
    print('tested 0..%d with %d workers; hits=%s'%(NMAX,W,hits),flush=True)
