#!/usr/bin/env python3
"""假设 model_B.bin 是"被打乱后的模型"的加密副本：
   1) 用候选口令尝试解出 PK(ZIP) 明文；2) 载入 B；3) 用优化器(A/B 神经元签名匹配)恢复三层置换；
   4) 直接过 check.py 的 V 校验。
用法: python3 crack_B.py PASSWORD
"""
import hashlib
import io
import sys
import zipfile
import numpy as np

V = 'cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864'
A = np.load('model_A.npz')
B = open('model_B.bin', 'rb').read()


def ok(canon):
    body = hashlib.sha256(canon.encode()).hexdigest()[:32]
    return hashlib.sha256(('ns::' + body).encode()).hexdigest() == V


def try_decrypt(pw):
    from Crypto.Cipher import AES, ARC4, ChaCha20
    outs = {}
    keys = [hashlib.sha256(pw).digest(), hashlib.md5(pw).digest(),
            hashlib.sha1(pw).digest()[:16], (pw * 32)[:32], pw.ljust(16, b'\0')[:16]]
    for i, kb in enumerate(keys):
        for klen in (16, 24, 32):
            key = (kb * 2)[:klen]
            for mode, name in ((AES.MODE_ECB, 'ecb'), (AES.MODE_CBC, 'cbc'),
                               (AES.MODE_CFB, 'cfb'), (AES.MODE_OFB, 'ofb')):
                for iv in (b'\0' * 16, B[:16]):
                    try:
                        c = AES.new(key, mode, iv=iv)
                        outs[f'aes-{name}-{i}-{klen}-{iv == B[:16]}'] = c.decrypt(B)
                    except Exception:
                        pass
            try:
                outs[f'aes-ctr-{i}-{klen}'] = AES.new(key, AES.MODE_CTR, nonce=b'\0' * 8).decrypt(B)
            except Exception:
                pass
            try:
                outs[f'rc4-{i}-{klen}'] = ARC4.new(key).decrypt(B)
            except Exception:
                pass
            try:
                outs[f'chacha-{i}-{klen}'] = ChaCha20.new(key=key, nonce=b'\0' * 12).decrypt(B)
            except Exception:
                pass
    good = {}
    for nm, pt in outs.items():
        for skip in (0, 8, 16):
            body_ = pt[skip:]
            if body_[:2] == b'PK':
                try:
                    z = zipfile.ZipFile(io.BytesIO(body_))
                    good[nm] = z
                except Exception:
                    pass
    return good


def load_zip(z):
    out = {}
    for nm in z.namelist():
        if nm.endswith('.npy'):
            out[nm[:-4]] = np.load(io.BytesIO(z.read(nm)))
    return out


def signatures(arrs):
    """每层神经元签名 = (偏置, 入边列, 出边行)"""
    L = []
    for nm, bi, ii, oi in (('L1', 7, 1, 6), ('L2', 4, 6, 2), ('L3', 3, 2, 5)):
        b, inc, out = arrs[f'k{bi}'], arrs[f'k{ii}'], arrs[f'k{oi}']
        n = b.shape[0]
        L.append([(round(float(b[i]), 9), inc[:, i].tobytes(), out[i].tobytes()) for i in range(n)])
    return L


def match(SA, SB):
    """贪心/Hungarian 匹配 A 的神经元到 B 的神经元，返回列表 p(i)=j"""
    n = len(SA)
    C = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(n):
            same_b = abs(SA[i][0] - SB[j][0]) < 1e-9
            same_i = SA[i][1] == SB[j][1]
            same_o = SA[i][2] == SB[j][2]
            C[i, j] = 3 - (same_b + same_i + same_o)
    # 贪心最优匹配（无 scipy 依赖）：代价相同时按索引稳定
    p = [None] * n
    used = set()
    order = sorted(((C[i, j], i, j) for i in range(n) for j in range(n)))
    for cost, i, j in order:
        if p[i] is None and j not in used:
            p[i] = j
            used.add(j)
    for i in range(n):
        if p[i] is None:
            j = next(j for j in range(n) if j not in used)
            p[i] = j
            used.add(j)
    return p


def main():
    pw = sys.argv[1].encode() if len(sys.argv) > 1 else b''
    good = try_decrypt(pw + b'\n') or try_decrypt(pw) or try_decrypt(pw.strip())
    if not good:
        print('[-] 这个口令没解出 ZIP(PK) 明文')
        return
    for nm, z in good.items():
        arrs = load_zip(z)
        if 'k1' not in arrs:
            continue
        SA, SB = signatures({f'k{i}': A[f'k{i}'] for i in range(8)}), signatures(arrs)
        ps = [match(SA[i], SB[i]) for i in range(3)]
        cands = []
        for inv in (False, True):
            ls = []
            for p in ps:
                if inv:
                    q = [0] * len(p)
                    for a, b in enumerate(p):
                        q[b] = a
                    p = q
                ls.append(p)
            for order in ((0, 1, 2), (2, 1, 0)):
                ls2 = [ls[i] for i in order]
                c = ';'.join(','.join(map(str, l)) for l in ls2)
                cands.append(c)
                if ok(c):
                    print('[+] 命中!', c)
                    return
        print('[-] 解出模型但置换未命中; 解密方式:', nm, '示例:', cands[0][:80])


if __name__ == '__main__':
    main()
