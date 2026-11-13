import numpy as np, math, collections, hashlib, itertools
d=np.load('model_A.npz'); K={i:d[f'k{i}'].astype(np.float64) for i in range(8)}
B=open('model_B.bin','rb').read()

print('='*72); print('检查①：神经元身份 = (入边组ID, 出边组ID, bias组ID) 三元组'); print('='*72)
tot_amb=1
for n,bi,ii,oi in [(32,7,1,6),(40,4,6,2),(48,3,2,5)]:
    b,inc,out=K[bi],K[ii],K[oi]
    def cls(keys):
        g={}; 
        for i,k in enumerate(keys): g.setdefault(k,i)
        return [g[k] for k in keys]
    cB=cls([round(float(x),12) for x in b])
    cC=cls([inc[:,i].tobytes() for i in range(n)])
    cO=cls([out[i].tobytes() for i in range(n)])
    trip=[(cB[i],cC[i],cO[i]) for i in range(n)]
    nB,nC,nO=len(set(cB)),len(set(cC)),len(set(cO))
    amb=math.factorial(nB)*math.factorial(nC)*math.factorial(nO)
    tot_amb*=amb
    print(f'  L{n}: 三元组种类 {len(set(trip))}/{n}  类别数 (bias {nB}, 入边 {nC}, 出边 {nO})  bias组==出边组? {cB==cO}')
    print(f'        该层编号自由度 = {nB}!·{nC}!·{nO}! = {amb:.3e}')
print(f'\n  三层编号自由度合计 = {tot_amb:.3e}')
print('  => 组合关系（谁能和谁连）唯一可恢复；规范编号顺序不可恢复（与你的结论一致）')

print(); print('='*72); print('检查②：k5 的浮点究竟来自哪个 NumPy API'); print('='*72)
allv=np.concatenate([K[i].ravel() for i in range(8)])
u=np.unique(allv); s_hat=u.std(ddof=1); mx=np.abs(u).max()
print(f'  926 个去重值：std = {s_hat:.6f}，max|v| = {mx:.15f}')
ZR=3.6541528853610088
print(f'  numpy ziggurat 上界 ziggurat_nor_r = {ZR}')
print(f'  若为 Generator.standard_normal/normal：必须 s >= {mx/ZR:.6f}（因为 |x|<=3.654）')
print(f'  若 s=0.6：需要 |x|max = {mx/0.6:.4f} > {ZR:.4f} ⇒ **ziggurat 不可能**')
# 正态极值估计
n=len(u)
print(f'  正态极值估计：E[max|x|] ≈ sigma*sqrt(2 ln(2n)) = {s_hat*math.sqrt(2*math.log(2*n)):.3f}（实测 {mx:.3f}）')
print(f'  => sigma 的最佳估计 {s_hat:.4f}；若真为 ziggurat，sigma 至少要 0.6239（差 {0.6239/s_hat:.2f} 个标准差）')
print('  结论：s≈0.6 且 max|x|=3.80 只与 legacy `np.random.randn`（Marsaglia 极坐标法，无 3.654 上界）相容；')
print('        Generator.normal 只有在 s>=0.6239 时才可能。此前的“ziggurat×0.6”表述不严谨，现纠正。')

print(); print('='*72); print('检查③：model_B 的自定义布局穷举（位打包/字节取模/uint16）'); print('='*72)
def is_perm(vals,n):
    return len(vals)==n and sorted(vals)==list(range(n))
hits=[]
# 位打包：不同位宽/偏移/长度
for width in (5,6,7,8):
    for n in (32,40,48):
        need=(n*width+7)//8
        for off in range(0, min(len(B)-need, 4096)+1):
            bits=int.from_bytes(B[off:off+need],'big')
            vals=[(bits >> (need*8 - width*(i+1))) & ((1<<width)-1) for i in range(n)]
            if is_perm(vals,n): hits.append(('bitpack',width,n,off,vals[:5]))
print(f'  位打包置换扫描: {sum(1 for (w,n) in [(w,n) for w in (5,6,7,8) for n in (32,40,48)])} 组配置 × 全偏移 -> hits={len(hits)}')
# 字节取模
for n in (32,40,48):
    for off in range(0, min(len(B)-n, 4096)+1):
        vals=[b % n for b in B[off:off+n]]
        if is_perm(vals,n): hits.append(('mod',n,off))
# uint16 < n
for n in (32,40,48):
    need=2*n
    for off in range(0, min(len(B)-need,2048)+1):
        vals=[int.from_bytes(B[off+2*i:off+2*i+2],'little') for i in range(n)]
        if is_perm(vals,n): hits.append(('u16',n,off))
# uint32 < n
for n in (32,40,48):
    need=4*n
    for off in range(0, min(len(B)-need,1024)+1):
        vals=[int.from_bytes(B[off+4*i:off+4*i+4],'little') for i in range(n)]
        if is_perm(vals,n): hits.append(('u32',n,off))
print(f'  字节mod / uint16 / uint32 置换扫描 -> hits={len(hits)}')
print('  hits:', hits[:5])
