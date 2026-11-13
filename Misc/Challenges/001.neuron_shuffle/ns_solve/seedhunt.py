import numpy as np, sys
d=np.load('model_A.npz')
targets=[]
for name in ['k0','k3','k4','k7']:   # 16,14,12,10 个值的偏置基
    v=np.sort(np.abs(np.unique(d[name].astype(np.float64))))
    targets.append((name, v, v.sum(), (v**2).sum()))
Lset=sorted(set(len(t[1]) for t in targets))
print('targets', [(t[0],len(t[1])) for t in targets], flush=True)
S=700
hits=[]
def scan(gen, label, seeds):
    for s in seeds:
        r = np.random.default_rng(s) if label=='dr' else np.random.RandomState(s)
        x = np.abs((r.standard_normal(S)*0.6) if label=='dr' else (r.randn(S)*0.6))
        c=np.cumsum(np.concatenate(([0.0],x)))
        for name,tv,tsum,tsq in targets:
            L=len(tv)
            ws=c[L:]-c[:-L]
            idx=np.where(np.abs(ws-tsum)<1e-7)[0]
            for i in idx:
                w=np.sort(x[i:i+L])
                if w.shape==tv.shape and np.allclose(w,tv,rtol=0,atol=1e-13):
                    print('HIT',label,s,name,i, flush=True); hits.append((label,s,name,int(i)))
                    return True
    return False
for label in ('dr','rs'):
    scan(gen=None,label=label,seeds=range(2000000))
    print('done',label,flush=True)
print('hits',hits)
