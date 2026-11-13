#!/usr/bin/env python3
"""neuron_shuffle: 候选答案生成 + 本地校验（不需要服务器）。
   任何"规则"都可以在这里加一行，脚本会立刻告诉你是否命中 check.py 里的 V。
"""
import collections
import hashlib
import itertools
import numpy as np

V = 'cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864'
D = np.load('model_A.npz')
k = {i: D[f'k{i}'] for i in range(8)}
LAY = [(32, 7, 1, 6), (40, 4, 6, 2), (48, 3, 2, 5)]   # (n, bias, incoming, outgoing)


def body(canon):
    return hashlib.sha256(canon.encode()).hexdigest()[:32]


def hit(canon):
    return hashlib.sha256(('ns::' + body(canon)).encode()).hexdigest() == V


def groups(keys):
    g = collections.OrderedDict()
    for i, x in enumerate(keys):
        g.setdefault(x, []).append(i)
    return list(g.values())


def keys_of(n, b, inc, out):
    return {
        'bias': [round(float(x), 12) for x in b],
        'inc': [inc[:, j].tobytes() for j in range(n)],
        'out': [out[i].tobytes() for i in range(n)],
    }


def rules():
    """返回 {规则名: [层1列表, 层2列表, 层3列表]}"""
    R = {}
    per = []
    for n, bi, ii, oi in LAY:
        b, inc, out = k[bi], k[ii], k[oi]
        C = {}
        for kn, keys in keys_of(n, b, inc, out).items():
            g = groups(keys)
            first = [g.index(next(x for x in g if i in x)) for i in range(n)]
            C[f'{kn}_label_first'] = first
            C[f'{kn}_label_first_1based'] = [x + 1 for x in first]
            C[f'{kn}_reps'] = [min(x) for x in g]
            C[f'{kn}_sizes'] = [len(x) for x in g]
            C[f'{kn}_dups'] = sorted(i for x in g for i in x[1:])
            C[f'{kn}_groupcat'] = [i for x in g for i in x]
            p = sorted(range(n), key=lambda i: first[i])
            C[f'{kn}_grouporder'] = p
            inv = [0] * n
            for a, v in enumerate(p):
                inv[v] = a
            C[f'{kn}_grouporder_inv'] = inv
        C['bias_argsort'] = list(np.argsort(b, kind='stable'))
        invb = [0] * n
        for a, v in enumerate(C['bias_argsort']):
            invb[v] = a
        C['bias_argsort_inv'] = invb
        C['bias_argsort_desc'] = list(np.argsort(-b, kind='stable'))
        C['bias_rank_desc'] = list(np.argsort(np.argsort(-b, kind='stable')))
        per.append((n, C))
    names = set(per[0][1]) & set(per[1][1]) & set(per[2][1])
    for nm in names:
        for order in ((0, 1, 2), (2, 1, 0)):
            R[f'{nm}@{order}'] = [per[i][1][nm] for i in order]
    return R


def main():
    R = rules()
    ok = [nm for nm, ls in R.items()
          if hit(';'.join(','.join(map(str, l)) for l in ls))]
    print(f'候选规则数: {len(R)}  命中: {ok if ok else "无"}')
    for nm, ls in list(R.items())[:3]:
        print(' 示例:', nm, '->', ';'.join(','.join(map(str, l)) for l in ls)[:90], '...')


if __name__ == '__main__':
    main()
