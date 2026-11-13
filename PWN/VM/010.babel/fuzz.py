import random, struct, subprocess, sys
from vm import asm, run

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

OPS = []

def gen_prog():
    """Generate a semi-typed program. Track a stack model of kinds."""
    prog = []
    st = []   # kinds: 'i','s','l','b','h'
    nloc = 0
    for step in range(random.randint(1, 14)):
        choice = random.random()
        if choice < 0.18 or not st:
            kind = random.choice(['i', 'i', 's', 'l'])
            if kind == 'i':
                prog.append(('push', random.choice([0, 1, 2, 7, 255, 0xffffffff, 0x7fffffff, 0x80000000, random.getrandbits(32)]))); st.append('i')
            elif kind == 's':
                n = random.choice([0, 1, 2, 5, 16, 17, 32])
                prog.append(('str', bytes(random.getrandbits(8) for _ in range(n)))); st.append('s')
            elif kind == 'l':
                n = random.choice([0, 1, 2, 3, 5])
                if len(st) < n: n = len(st)
                for _ in range(n):
                    st.pop()
                prog.append(('list', n)); st.append('l')
        elif choice < 0.28:
            k = random.choice(['s', 'l', 'b'])
            n = random.choice([0, 1, 2, 8, 16, 64, 0x400])
            if k == 'b':
                prog.append(('input', n)); st.append('b')
            else:
                prog.append(('str', bytes(random.getrandbits(8) for _ in range(min(n, 8))))); st.append('s')
        elif choice < 0.36 and st:
            prog.append(('dup',)); st.append(st[-1])
        elif choice < 0.44 and st:
            prog.append(('pop',)); st.pop()
        elif choice < 0.50 and len(st) >= 2:
            prog.append((random.choice(['add', 'sub', 'mul']),))
            a = st.pop(); b = st.pop(); st.append('i')
        elif choice < 0.60 and 's' in st:
            idx = random.choice([0, 1, 5, 16, 100, 0xffffffff, random.getrandbits(32)])
            if random.random() < 0.5:
                prog.append(('getb', idx))
                st.append('i')
            else:
                # need a value on top: push int then setb pops (val, obj)
                prog.append(('push', random.getrandbits(8)))
                st.append('i')
                # stack order: obj deeper, val top
                if len(st) >= 2:
                    prog.append(('setb', idx))
                    st.pop(); st.pop()
        elif choice < 0.70 and 'l' in st:
            idx = random.choice([0, 1, 2, 3, 0xffffffff, random.getrandbits(32)])
            if random.random() < 0.5:
                prog.append(('gete', idx)); st.append(random.choice(['i', 's', 'l', 'b']))
            else:
                prog.append(('push', random.getrandbits(32))); st.append('i')
                prog.append(('sete', idx)); st.pop(); st.pop()
        elif choice < 0.76 and 'b' in st:
            idx = random.choice([0, 1, 15, 16, 64, 0x400, 0xffffffff, random.getrandbits(32)])
            if random.random() < 0.5:
                prog.append(('bget', idx)); st.append('i')
            else:
                prog.append(('push', random.getrandbits(8))); st.append('i')
                prog.append(('bset', idx)); st.pop(); st.pop()
        elif choice < 0.82:
            prog.append(('hdl', random.choice([0, 1, 2, 3, 7, 15]))); st.append('h')
        elif choice < 0.88 and 'h' in st:
            nargs = random.choice([0, 1, 2, 3, 20])
            for _ in range(min(nargs, len(st) - 1)):
                st.pop()
            prog.append(('call', nargs))
        elif choice < 0.92:
            nargs = random.choice([0, 1, 2, 3])
            for _ in range(min(nargs, len(st))):
                st.pop()
            prog.append(('call2', random.choice([0, 1, 2, 3, 15]), nargs))
            st.append('i')
        elif choice < 0.95:
            # bind attempt: push value, push obj
            prog.append(('push', random.getrandbits(32))); st.append('i')
            prog.append(('bind',))
            if len(st) >= 2: st.pop(); st.pop()
        elif choice < 0.98 and st:
            prog.append(('len',)); st.pop(); st.append('i')
        else:
            if st:
                prog.append(('print',)); st.pop()
    return prog

bad = []
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
for it in range(N):
    prog = gen_prog()
    code = asm(prog)
    if len(code) == 0 or len(code) > 0x10000: continue
    try:
        rc, so, se = run(code, extra=b'', timeout=5)
    except subprocess.TimeoutExpired:
        print("TIMEOUT", prog); continue
    if rc < 0 or (rc == 0 and se and b'trap' not in se) or (rc not in (0, 1)):
        print("ANOMALY rc=%d out=%r err=%r prog=%r" % (rc, so[:60], se[:80], prog))
        bad.append(prog)
print("done, anomalies:", len(bad))
