import struct, subprocess, sys, os

BIN = "/mnt/work/buuctf/other/2.39/amd64/babel/lab/babel_239"

def u32(x): return struct.pack('<I', x)
def p64(x): return struct.pack('<Q', x)

def asm(prog):
    out = b''
    for it in prog:
        op = it[0]
        if op == 'push':      out += b'\x01' + p64(it[1] & 0xffffffffffffffff)
        elif op == 'str':
            s = it[1]
            out += b'\x02' + u32(len(s)) + s
        elif op == 'dup':     out += b'\x03'
        elif op == 'pop':     out += b'\x04'
        elif op == 'add':     out += b'\x05'
        elif op == 'sub':     out += b'\x06'
        elif op == 'mul':     out += b'\x07'
        elif op == 'list':    out += b'\x08' + u32(it[1])
        elif op == 'pair':    out += b'\x09' + u32(it[1])
        elif op == 'gete':    out += b'\x0a' + u32(it[1])
        elif op == 'sete':    out += b'\x0b' + u32(it[1])
        elif op == 'getb':    out += b'\x0c' + u32(it[1])
        elif op == 'setb':    out += b'\x0d' + u32(it[1])
        elif op == 'len':     out += b'\x0e'
        elif op == 'x0f':     out += b'\x0f'
        elif op == 'ldl':     out += b'\x10' + bytes([it[1]])
        elif op == 'stl':     out += b'\x11' + bytes([it[1]])
        elif op == 'print':   out += b'\x12'
        elif op == 'raw':     out += b'\x13'
        elif op == 'hdl':     out += b'\x14' + bytes([it[1]])
        elif op == 'call':    out += b'\x15' + bytes([it[1]])
        elif op == 'input':   out += b'\x16' + u32(it[1])
        elif op == 'bget':    out += b'\x17' + u32(it[1])
        elif op == 'bset':    out += b'\x18' + u32(it[1])
        elif op == 'bind':    out += b'\x19'
        elif op == 'call2':   out += b'\x20' + bytes([it[1], it[2]])
        elif op == 'halt':    out += b'\xff'
        elif op == 'raw_bytes': out += it[1]
        else: raise ValueError(op)
    return out

def run(code, extra=b'', timeout=10):
    data = u32(len(code)) + code + extra
    p = subprocess.run([BIN], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

if __name__ == '__main__':
    tests = {
      'print42': [('push',42),('print',)],
      'printstr': [('str',b'hello'),('print',)],
      'add': [('push',2),('push',3),('add',),('print',)],
      'sub': [('push',10),('push',3),('sub',),('print',)],
      'mul': [('push',6),('push',7),('mul',),('print',)],
      'len': [('str',b'hello'),('len',),('print',)],
      'getb': [('str',b'hello'),('push',1),('pop',),('getb',1),('print',)],
      'list': [('push',7),('push',8),('push',9),('list',3),('len',),('print',)],
      'gete': [('push',7),('push',8),('push',9),('list',3),('gete',0),('print',)],
      'gete2': [('push',7),('push',8),('push',9),('list',3),('gete',2),('print',)],
      'raw':  [('push',0x41424344),('raw',)],
      'input': [('input',16),('len',),('print',)],
      'hdl0': [('hdl',0),('print',)],
      'call0': [('hdl',0),('call',0)],
      'call2_0': [('push',1),('call2',0,1)],
      'halt': [('push',1),('halt',),('print',)],
    }
    for name, prog in tests.items():
        code = asm(prog)
        try:
            rc, so, se = run(code, extra=b'A'*64)
        except subprocess.TimeoutExpired:
            print(f"{name:12s} TIMEOUT"); continue
        print(f"{name:12s} rc={rc:4d} out={so[:120]!r} err={se[:80]!r}")

def probe_tests():
    tests = {
      'bind_list': [('list',0),('push',0x1234),('bind',),('print',)],
      'bind_buf':  [('input',16),('push',0x1234),('bind',),('print',)],
      'bset_list': [('list',0),('push',0x41),('bset',0),('print',)],
      'bset_buf':  [('input',16),('push',0x41),('bset',0),('print',)],
      'bget_buf':  [('input',16),('bget',0),('print',)],
      'gete_oob':  [('push',1),('push',2),('list',2),('gete',5),('print',)],
      'getb_oob':  [('str',b'ab'),('getb',100),('print',)],
      'setb_oob':  [('str',b'ab'),('push',0x41),('setb',100),('print',)],
      'neg_idx':   [('str',b'ab'),('getb',0xffffffff),('print',)],
      'pair':      [('push',1),('push',2),('pair',2),('len',),('print',)],
      'x0f':       [('push',1),('push',2),('x0f',),('print',)],
      'callbuf':   [('input',16),('call',0)],
    }
    for name, prog in tests.items():
        code = asm(prog)
        try:
            rc, so, se = run(code)
        except subprocess.TimeoutExpired:
            print(f"{name:12s} TIMEOUT"); continue
        print(f"{name:12s} rc={rc:4d} out={so[:100]!r} err={se[:100]!r}")
