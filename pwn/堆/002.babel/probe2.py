import vm
tests = {
 'h0c0': [('hdl',0),('call',0)],
 'h0c1_65': [('hdl',0),('push',65),('call',1)],
 'h1c1_65': [('hdl',1),('push',65),('call',1)],
 'h2c1_65': [('hdl',2),('push',65),('call',1)],
 'h0c2': [('hdl',0),('push',65),('push',66),('call',2)],
 'h1c2': [('hdl',1),('push',65),('push',66),('call',2)],
 'h2c2': [('hdl',2),('push',65),('push',66),('call',2)],
 'h3c1': [('hdl',3),('push',65),('call',1)],
 'c2_1': [('push',65),('call2',1,1)],
 'c2_0': [('push',65),('call2',0,1)],
 'c2_2': [('push',65),('call2',2,1)],
}
for name, prog in tests.items():
    code = vm.asm(prog)
    try:
        rc, so, se = vm.run(code)
    except Exception as e:
        print(name, 'EXC', e); continue
    print(f"{name:10s} rc={rc:4d} out={so[:80]!r} err={se[:100]!r}")
