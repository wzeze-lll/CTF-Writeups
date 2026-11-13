import random, sys, targets
start,step,NMAX=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
T=targets.TARGETS
hit=[]
for seed in range(start,NMAX,step):
    r=random.Random(seed)
    x=[abs(r.gauss(0.0,0.6)) for _ in range(32)]
    for name,tv,ts in T:
        L=len(tv)
        s=sum(x[:L])
        if abs(s-ts)<1e-9 and sorted(x[:L])==tv.tolist():
            print('HIT',seed,name,flush=True); hit.append((seed,name))
print('py-random worker',start,'done',hit,flush=True)
