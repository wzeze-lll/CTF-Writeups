#!/usr/bin/env python3
"""三个最小实验：①精确签名匹配的可辨识性 ②一致性置换集合是否为空 ③model_B 是否可解析"""
import collections, hashlib, itertools, math, zlib
import numpy as np

A = np.load('model_A.npz')
K = {i: A[f'k{i}'].astype(np.float64) for i in range(8)}
RAW = open('model_A.npz', 'rb').read()
B = open('model_B.bin', 'rb').read()
V = "cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"

def part(keys):
    g = collections.OrderedDict()
    for i, k in enumerate(keys):
        g.setdefault(k, []).append(i)
    return g

print('=' * 70)
print('实验 1：精确签名匹配（入边列 + bias + 出边行）')
print('=' * 70)
LAY = [(32, 7, 1, 6), (40, 4, 6, 2), (48, 3, 2, 5)]   # (n, bias, incoming, outgoing)
sig_all = {}
for n, bi, ii, oi in LAY:
    b, inc, out = K[bi], K[ii], K[oi]
    sig = [(round(float(b[i]), 15), inc[:, i].tobytes(), out[i].tobytes()) for i in range(n)]
    uniq = len(set(sig))
    sig_all[n] = sig
    print(f'  L{n}: 精确签名种类 = {uniq}/{n}  ->  {"全部可区分（匹配唯一=恒等置换）" if uniq==n else "存在不可区分神经元"}')

print()
print('=' * 70)
print('实验 2：是否存在“使模型自洽”的置换（即恢复原始顺序）')
print('=' * 70)
tot = 1
for n, bi, ii, oi in LAY:
    b, inc, out = K[bi], K[ii], K[oi]
    gT = part([round(float(x), 12) for x in b])                     # 出边+bias 的类
    gC = part([inc[:, j].tobytes() for j in range(n)])              # 入边 的类
    szT = sorted((len(v) for v in gT.values()), reverse=True)
    szC = sorted((len(v) for v in gC.values()), reverse=True)
    tmap = {m: t for t, ms in enumerate(gT.values()) for m in ms}
    cmap = {m: c for c, ms in enumerate(gC.values()) for m in ms}
    cross = len({(tmap[i], cmap[i]) for i in range(n)})
    print(f'  L{n}: 出边类 {len(gT)} 组 {szT}')
    print(f'        入边类 {len(gC)} 组 {szC}')
    print(f'        类大小多重集是否相同: {szT == szC}   交叉组合数 {cross}/{n}')
    tot *= math.factorial(len(gT)) * math.factorial(len(gC))
print('\n  结论：置换同时搬动两套标签，“交叉关系”是不变量。')
print('  三层均为完全交叉(n/n) 且类大小多重集不同 => 不存在任何置换能让二者对齐。')
print('  “恢复原始顺序”的答案集合 = 空集。')

print()
print('=' * 70)
print('实验 3：类编号自由度（规范顺序信息是否在文件里）')
print('=' * 70)
print(f'  仅出边/bias 一侧：10!·12!·14! = {math.factorial(10)*math.factorial(12)*math.factorial(14):.3e}')
print(f'  两侧一起：        10!·10! · 12!·11! · 14!·13! = {math.factorial(10)**2*math.factorial(12)*math.factorial(11)*math.factorial(14)*math.factorial(13):.3e}')
# 两种“自然”规则给出不同答案 -> 规则本身不可由数据裁决
def perm_first(n, keys):
    g = part(keys)
    lab = [0]*n
    for L, ms in enumerate(g.values()):
        for m in ms: lab[m] = L
    return sorted(range(n), key=lambda i: lab[i])
def perm_value(n, keys):
    g = part(keys)
    order = sorted(g.items(), key=lambda kv: kv[0] if isinstance(kv[0], float) else kv[0])
    lab = {}
    for L, (k, ms) in enumerate(order):
        for m in ms: lab[m] = L
    return sorted(range(n), key=lambda i: lab[i])
for n, bi, ii, oi in LAY:
    b = K[bi]
    p1 = perm_first(n, [round(float(x), 12) for x in b])
    p2 = perm_value(n, [round(float(x), 12) for x in b])
    print(f'  L{n}: “首现序”与“数值升序”两个同样自然的规则 -> 置换相同? {p1 == p2}')

print()
print('=' * 70)
print('实验 4：model_B.bin 可解析性电池')
print('=' * 70)
print(f'  大小 {len(B)}；熵 {-(sum(c/len(B)*math.log2(c/len(B)) for c in collections.Counter(B).values())):.4f}')
magics = {
    'ZIP/PK': b'PK\x03\x04', 'NPY': b'\x93NUMPY', 'gzip': b'\x1f\x8b',
    'zlib': b'\x78\x9c', 'bz2': b'BZh', 'xz': b'\xfd7zXZ', 'zstd': b'\x28\xb5\x2f\xfd',
    'lz4': b'\x04\x22\x4d\x18', 'HDF5': b'\x89HDF', 'pickle': b'\x80\x04',
    'safetensors-json': b'{', 'GGUF': b'GGUF', 'ONNX-proto': b'\x08',
    'blosc': b'\x02\x01', 'arrow': b'ARROW1', 'parquet': b'PAR1',
}
print('  魔数扫描:', {k: (B.find(v) if len(v) > 1 else None) for k, v in magics.items()})
ok_zip = ok_npy = False
for off in range(0, min(len(B), 4096)):
    if B[off:off+4] == b'PK\x03\x04': ok_zip = True; print('    PK at', off)
    if B[off:off+6] == b'\x93NUMPY': ok_npy = True; print('    NPY at', off)
print('  zip/npy 明文:', ok_zip, ok_npy)

# A 的浮点值是否出现在 B 中（决定性）
vals = sorted({v for i in range(8) for v in K[i].ravel().tolist()})
pat8 = {v: np.float64(v).tobytes() for v in vals}
hit8 = sum(1 for v, p in pat8.items() if B.find(p) >= 0)
hit4 = 0
for v in vals:
    f4 = np.float32(v).tobytes()
    if B.find(f4) >= 0: hit4 += 1
print(f'  A 的 {len(vals)} 个去重 float64 值在 B 中出现: {hit8} 个（期望 0）')
print(f'  其 float32 形式在 B 中出现: {hit4} 个（期望约 {len(vals)*len(B)/2**32:.2e}）')

# 块级多重集：若 B 是 A 的浮点/块置换，n 字节块多重集应相同
for blk in (4, 8, 16, 32):
    n = len(RAW) // blk
    a_set = sorted(RAW[i*blk:(i+1)*blk] for i in range(n))
    b_set = sorted(B[i*blk:(i+1)*blk] for i in range(n))
    same = a_set == b_set
    print(f'  {blk:2d} 字节块多重集 A vs B 相同: {same}')
    if not same:
        inter = len(set(a_set) & set(b_set))
        print(f'      A 的 {n} 个块中有 {inter} 个也出现在 B 中')

print('\n  --- 统计检验 ---')
c = collections.Counter(B); n = len(B)
chi = sum((v - n/256)**2/(n/256) for v in c.values())
print(f'  卡方(df=255) = {chi:.1f}')
print(f'  zlib 压缩 {len(B)} -> {len(zlib.compress(B, 9))}')
bits = np.unpackbits(np.frombuffer(B, dtype=np.uint8))
print(f'  单比特比例 = {bits.mean():.5f}（0.5 为随机）')
print(f'  最长 0 游程 = {max(len(x) for x in "".join(map(str, bits.tolist())).split("1"))}')
print()
print('=' * 70)
print(f'V = {V[:16]}...（只能验证答案，无法反推）')
print('=' * 70)
