import vm, struct, subprocess
BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"
def frame(p):
    c = vm.asm(p); return struct.pack('<I',len(c))+c
for n in (0x100, 0x1000, 0x7ff0, 0x8000, 0xff00):
    prog = [('str', b'A'*n), ('pop',), ('push',1), ('list',1), ('dup',), ('print',), ('pop',), ('pop',)]
    p = subprocess.run([BIN], input=frame(prog), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    out = p.stdout
    print(hex(n), p.returncode, out[:40], p.stderr[:60])
