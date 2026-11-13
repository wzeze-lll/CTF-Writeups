import vm, struct, subprocess
BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"
def frame(p): 
    c = vm.asm(p); return struct.pack('<I',len(c))+c
# print refs of successive allocations: ref>>1 encodes (off<<3)|(tag>>1)
prog = []
prog += [('str', b'A'*0x10), ('dup',), ('print',), ('pop',)]
prog += [('push',1), ('list',1), ('dup',), ('print',), ('pop',), ('pop',)]
prog += [('input',16), ('dup',), ('print',), ('pop',)]
prog += [('hdl',1), ('dup',), ('print',), ('pop',)]
prog += [('str', b'B'*0x20), ('dup',), ('print',), ('pop',)]
p = subprocess.run([BIN], input=frame(prog), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(p.returncode, p.stdout, p.stderr[:100])
