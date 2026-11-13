#!/usr/bin/env python3
from elftools.elf.elffile import ELFFile
from capstone import *
from capstone.x86 import *
import sys, re

path = sys.argv[1]
f = open(path, "rb")
elf = ELFFile(f)
text = elf.get_section_by_name(".text")
code = text.data(); base = text["sh_addr"]
rodata = elf.get_section_by_name(".rodata")
rdata = rodata.data(); rbase = rodata["sh_addr"]

def cstr(addr):
    off = addr - rbase
    if 0 <= off < len(rdata):
        end = rdata.find(b"\0", off)
        s = rdata[off:end]
        try: return s.decode()
        except: return None
    return None

md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
insns = list(md.disasm(code, base))
# function starts: endbr64 or targets of call
starts = set()
for i in insns:
    if i.bytes[:4] == b"\xf3\x0f\x1e\xfa":
        starts.add(i.address)
for i in insns:
    if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM:
        t = i.operands[0].imm
        if base <= t < base+len(code): starts.add(t)
# also jmp targets
for i in insns:
    if i.mnemonic in ("jmp","je","jne","jz","jnz") and i.operands and i.operands[0].type == X86_OP_IMM:
        t=i.operands[0].imm
        if base <= t < base+len(code): starts.add(t)
starts = sorted(starts)
print("functions:", len(starts))
# assign each insn to function
import bisect
def owner(a):
    i = bisect.bisect_right(starts, a)-1
    return starts[i] if i>=0 else 0
funcs = {}
for i in insns:
    s = owner(i.address)
    funcs.setdefault(s, []).append(i)

for s in starts:
    strs=[]
    for i in funcs.get(s,[]):
        for op in i.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = i.address + i.size + op.mem.disp
                c = cstr(t)
                if c and len(c)>=4: strs.append(c)
            elif op.type == X86_OP_IMM:
                c = cstr(op.imm)
                if c and len(c)>=4: strs.append(c)
    strs = list(dict.fromkeys(strs))
    interesting = [x for x in strs if re.search(r"ring|whisper|drop|puppet|Ring|flag|rupee|shop|battle|hero|Hero", x, re.I)]
    if interesting:
        print("== func 0x%x size~%d" % (s, len(funcs.get(s,[]))))
        for x in interesting[:12]:
            print("    ", x[:90])
