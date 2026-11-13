import vm
tests = {
 'c2_0_print': [('push',65),('call2',0,1),('print',)],
 'c2_1_print': [('push',65),('call2',1,1),('print',)],
 'c2_2_print': [('push',65),('call2',2,1),('print',)],
 'c2_0_n2': [('push',65),('push',66),('call2',0,2),('print',)],
 'c2_3_idx': [('push',65),('call2',3,1),('print',)],
 'c2_15_idx': [('push',65),('call2',15,1),('print',)],
 'h0_call1': [('push',65),('hdl',0),('call',1),('print',)],
 'h1_call1': [('push',65),('hdl',1),('call',1),('print',)],
 'h2_call1': [('push',65),('hdl',2),('call',1),('print',)],
 'h0_call0': [('hdl',0),('call',0),('print',)],
 'h0_call2': [('push',65),('push',66),('hdl',0),('call',2),('print',)],
 'h0_str': [('str',b'/flag'),('hdl',0),('call',1),('print',)],
 'h1_str': [('str',b'/flag'),('hdl',1),('call',1),('print',)],
 'h2_str': [('str',b'/flag'),('hdl',2),('call',1),('print',)],
}
for name, prog in tests.items():
    code = vm.asm(prog)
    try:
        rc, so, se = vm.run(code)
    except Exception as e:
        print(name, 'EXC', e); continue
    print(f"{name:14s} rc={rc:4d} out={so[:80]!r} err={se[:100]!r}")
