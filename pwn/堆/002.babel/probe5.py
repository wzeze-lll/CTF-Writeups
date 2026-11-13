import vm, os, subprocess, struct
BIN="/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"
def run_trace(name, prog):
    code = vm.asm(prog)
    data = struct.pack('<I', len(code)) + code
    open('/tmp/in.bin','wb').write(data)
    p = subprocess.run(['strace','-f','-e','trace=openat,read,write,close,execve','-o','/tmp/tr.txt',BIN],
                       stdin=open('/tmp/in.bin','rb'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tr = open('/tmp/tr.txt').read()
    interesting = [l for l in tr.splitlines() if ('openat' in l or 'execve' in l) or ('read(0' in l) or ('write(1' in l)]
    print("==",name,"rc=",p.returncode,"out=",p.stdout[:60], "err=",p.stderr[:60])
    for l in interesting[:12]: print("   ", l.strip()[:150])

run_trace('h0_c1', [('push',1),('hdl',0),('call',1)])
run_trace('h1_c1', [('push',1),('hdl',1),('call',1)])
run_trace('h2_c1', [('push',1),('hdl',2),('call',1)])
run_trace('h1_c2', [('push',1),('push',2),('hdl',1),('call',2)])
run_trace('h0_c2', [('push',1),('push',2),('hdl',0),('call',2)])
run_trace('h2_c2', [('push',1),('push',2),('hdl',2),('call',2)])
