import vm, struct, subprocess

BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"

def frame(prog):
    code = vm.asm(prog)
    return struct.pack('<I', len(code)) + code

data = b''
# F1: dead string at offset 0 (0xFF00 bytes)
data += frame([('str', b'A'*0xFF00), ('pop',)])
# F2: live list at offset ~0xFF10, keep ref in local 0 and print it
data += frame([('push', 0x1234), ('list', 1), ('stl', 0), ('ldl', 0), ('print',), ('pop',)])
# F3..: fill heap with dead strings
for i in range(300):
    data += frame([('str', b'B'*0xFF00), ('pop',)])
# last: print the live list's ref (after GC it should have been rewritten)
data += frame([('ldl', 0), ('print',), ('pop',)])

p = subprocess.run([BIN], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
print("rc=", p.returncode)
print("out=", p.stdout)
print("err=", p.stderr[:200])
