#!/usr/bin/env python3
"""拿到任意提示后，一条命令出 flag。

用法：
  python3 try_hint.py canon "7,10,12;...;..."      # 直接给 canon 字符串
  python3 try_hint.py canon-file answer.txt        # 从文件读（等价于 check.py 的第二种用法）
  python3 try_hint.py rule sort:asc:index:0        # 规则名：模式:方向:输出:基
  python3 try_hint.py sweep                        # 重扫全部已知规则并打印结果
"""
import sys, hashlib, itertools, collections
import numpy as np

V = "cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"

def flag_of(canon: str):
    body = hashlib.sha256(canon.encode()).hexdigest()[:32]
    return ("flag{%s}" % body), hashlib.sha256(("ns::" + body).encode()).hexdigest() == V

def load():
    d = np.load('model_A.npz')
    return {i: np.array(d[f'k{i}'], dtype=np.float64) for i in range(8)}

def build(K, bi, mode, dirn, out, base):
    v = K[bi]; n = len(v)
    g = collections.OrderedDict()
    for i, x in enumerate(v):
        g.setdefault(round(float(x), 12), []).append(i)
    items = sorted(g.items(), key=lambda kv: kv[0] if dirn == 'asc' else -kv[0])
    if mode == 'sort':
        p = list(map(int, np.argsort(v if dirn == 'asc' else -v, kind='stable')))
        if out == 'index':
            return [x + base for x in p]
        r = [0] * n
        for a, b in enumerate(p):
            r[b] = a
        return [x + base for x in r]
    lab = [0] * n
    for L, (k, ms) in enumerate(items):
        for m in ms:
            lab[m] = L
    if out == 'index':
        return [x + base for x in lab]
    return [m + base for k, ms in items for m in ms]

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    cmd = sys.argv[1]
    if cmd == 'canon':
        canon = sys.argv[2]
    elif cmd == 'canon-file':
        canon = open(sys.argv[2]).read()
    elif cmd == 'rule':
        mode, dirn, out, base = sys.argv[2].split(':')
        K = load(); base = int(base)
        ls = [build(K, bi, mode, dirn, out, base) for bi in (7, 4, 3)]
        canon = ";".join(",".join(map(str, l)) for l in ls)
    elif cmd == 'sweep':
        K = load(); hits = 0; total = 0
        for mode in ('sort', 'group'):
            for dirn in ('asc', 'desc'):
                for out in ('index', 'rank'):
                    for base in (0, 1):
                        for order in ((7, 4, 3), (3, 4, 7)):
                            ls = [build(K, bi, mode, dirn, out, base) for bi in order]
                            canon = ";".join(",".join(map(str, l)) for l in ls)
                            fl, ok = flag_of(canon)
                            total += 1
                            if ok:
                                print("PASS", mode, dirn, out, base, order, fl); hits += 1
        print(f"sweep 完成：{total} 条规则，命中 {hits}")
        return
    else:
        print(__doc__); return
    # 规范化（与 check.py 一致）
    try:
        norm = ";".join(",".join(str(int(v)) for v in s.split(",")) for s in canon.strip().split(";"))
    except Exception:
        print("[-] canon 无法解析为整数列表"); return
    fl, ok = flag_of(norm)
    print(f"[*] canon 长度 {len(norm)}，前 60：{norm[:60]}")
    print(f"[*] check.py 公式判定：{'PASS ✅' if ok else 'FAIL'}")
    print(f"[*] 按 check.py 公式计算的 flag：{fl}")
    print("    （若 FAIL：该 canon 不是作者用的那个；若平台接受此 flag 则说明平台不校验 V）")

if __name__ == '__main__':
    main()
