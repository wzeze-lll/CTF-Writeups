import numpy as np, math
d=np.load('model_A.npz')
v=np.unique(np.concatenate([d[f'k{i}'].astype(np.float64).ravel() for i in range(8)]))
n=len(v); s_hat=v.std(ddof=1); mx=np.abs(v).max(); ZR=3.6541528853610088
def ll(x,s): 
    x=np.asarray(x,float); return float(-len(x)*math.log(s)-((x**2).sum())/(2*s*s)-len(x)/2*math.log(2*math.pi))
print(f'n={n}  sigma_hat={s_hat:.6f}  max|v|={mx:.9f}')
s_leg=s_hat; s_zig=max(mx/ZR, s_hat)
print(f'H_legacy(无上界)  MLE s={s_leg:.6f}   LL={ll(v,s_leg):.3f}')
print(f'H_ziggurat(上界) 约束 MLE s={s_zig:.6f}   LL={ll(v,s_zig):.3f}')
print(f'ΔLL = {ll(v,s_leg)-ll(v,s_zig):.3f}  (似然比 e^ΔLL = {math.exp(ll(v,s_leg)-ll(v,s_zig)):.2f})')
print(f'若真实 sigma={s_zig:.4f}，观测到 sigma_hat={s_hat:.4f} 的 z 分数 = '
      f'{(s_hat-s_zig)/(s_zig/math.sqrt(2*n)):.2f}')
rng=np.random.default_rng(0)
N=4000
# legacy s=0.6 模拟
mx_leg=[]; sh_leg=[]
for _ in range(N):
    x=rng.standard_normal(n)*0.6; mx_leg.append(np.abs(x).max()); sh_leg.append(x.std(ddof=1))
mx_leg=np.array(mx_leg); sh_leg=np.array(sh_leg)
print(f'\n[legacy s=0.6 模拟 {N} 组]  P(max>=观测)={np.mean(mx_leg>=mx):.4f}   '
      f'E[max]={mx_leg.mean():.3f}  E[sigma_hat]={sh_leg.mean():.4f}±{sh_leg.std():.4f}')
# ziggurat s=0.6 模拟：直接截断（等价于上界）
x=rng.standard_normal(2000000)*0.6
print(f'[ziggurat s=0.6] 理论上限 {0.6*ZR:.6f}，观测 max {mx:.6f} 超界 {(mx/(0.6*ZR)-1)*100:.2f}%')
# ziggurat 需要的最小 s
print(f'[ziggurat 相容所需最小 s] {mx/ZR:.6f}（非圆整数；若作者写 0.6 则不成立）')
