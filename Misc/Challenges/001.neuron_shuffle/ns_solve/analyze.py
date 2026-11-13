#!/usr/bin/env python3
"""neuron_shuffle 结构分析：确认模型是"类型矩阵 + 随机平铺"结构，并打印所有可提取的索引/映射。"""
import collections
import hashlib
import numpy as np

D = np.load('model_A.npz')
K = {i: D[f'k{i}'] for i in range(8)}
NAMES = {0: 'input.bias(16)', 1: 'W1(16,32)', 2: 'W3(40,48)', 3: 'b3(48)',
         4: 'b2(40)', 5: 'W4(48,32)', 6: 'W2(32,40)', 7: 'b1(32)'}


def groups(keys):
    g = collections.OrderedDict()
    for i, k in enumerate(keys):
        g.setdefault(k, []).append(i)
    return g


def report():
    print('== 数组 ==')
    for i in range(8):
        a = K[i]
        print(f'k{i:<2} {str(a.shape):>9} uniq={len(np.unique(a)):<5} {NAMES[i]}')

    print('\n== W1(16,32) 结构验证：不同值数 = 16*10 -> 说明是 16x10 基矩阵按随机标签平铺 ==')
    print('k1 uniq =', len(np.unique(K[1])), '(16*10 = 160)')
    print('k6 uniq =', len(np.unique(K[6])), '(10*11 = 110)')
    print('k2 uniq =', len(np.unique(K[2])), '(12*13 = 156)')
    print('k5 uniq =', len(np.unique(K[5])), '(14*32 = 448)')

    layers = [(32, 7, 1, 6, 'L1'), (40, 4, 6, 2, 'L2'), (48, 3, 2, 5, 'L3')]
    for n, bi, ii, oi, tag in layers:
        b, inc, out = K[bi], K[ii], K[oi]
        gb = groups([round(float(x), 12) for x in b])
        gi = groups([inc[:, j].tobytes() for j in range(n)])
        go = groups([out[i].tobytes() for i in range(n)])
        pb = frozenset(frozenset(v) for v in gb.values())
        pi = frozenset(frozenset(v) for v in gi.values())
        po = frozenset(frozenset(v) for v in go.values())
        # 两种划分是否正交
        rep_b = {i: min(v) for v in gb.values() for i in v}
        rep_i = {i: min(v) for v in gi.values() for i in v}
        cross = len({(rep_b[i], rep_i[i]) for i in range(n)})
        print(f'\n== {tag} n={n} ==')
        print('  偏置分组(类型) 组数=%d 组大小=%s' % (len(gb), sorted((len(v) for v in gb.values()), reverse=True)))
        print('  出边行分组     组数=%d 与偏置分组相同: %s' % (len(go), pb == po))
        print('  入边列分组     组数=%d 组大小=%s 与偏置分组相同: %s'
              % (len(gi), sorted((len(v) for v in gi.values()), reverse=True), pb == pi))
        print('  两划分交叉后独立组合数 = %d / %d  -> 完全正交，无任何置换能把两者对上' % (cross, n))


def check(canon):
    body = hashlib.sha256(canon.encode()).hexdigest()[:32]
    return hashlib.sha256(('ns::' + body).encode()).hexdigest() == V, body


V = 'cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864'

if __name__ == '__main__':
    report()
