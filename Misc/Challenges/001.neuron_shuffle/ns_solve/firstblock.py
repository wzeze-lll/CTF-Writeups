import numpy as np
d=np.load('model_A.npz')
tg={}
for name,n in [('k7',10),('k4',12),('k3',14),('k0',16)]:
    v=np.sort(np.abs(np.unique(d[name].astype(np.float64))))
    tg[n]=(v, float(v.sum()))
print('targets', {n:tg[n][1] for n in tg}, flush=True)
hits=[]
def run(gen, N):
    for seed in range(N):
        if gen=='dr':
            x=np.abs(np.random.default_rng(seed).standard_normal(16))*0.6
        else:
            x=np.abs(np.random.RandomState(seed % (2**32)).randn(16))*0.6
        for n,(tv,ts) in tg.items():
            if abs(float(x[:n].sum())-ts) < 1e-9 and np.allclose(np.sort(x[:n]), tv, rtol=0, atol=1e-12):
                print('HIT',gen,seed,n, flush=True); hits.append((gen,seed,n))
        if seed and seed % 5000000 == 0: print('.',seed,flush=True)
run('dr', 20000000)
run('rs', 8000000)
print('done', hits, flush=True)
