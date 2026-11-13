# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.9.6 (default, Apr 17 2026, 18:15:52) 
# [Clang 21.0.0 (clang-2100.1.1.101)]
# Embedded file name: encode.py
# Compiled at: 2019-08-19 21:01:57
print 'Welcome to Re World!'
print 'Your input1 is your flag~'
l = len(input1)
for i in range(l):
    num = ((input1[i] + i) % 128 + 128) % 128
    code += num

for i in range(l - 1):
    code[i] = code[i] ^ code[i + 1]

print code
code = [4, 5, 6, 7, 8, 9, 10, 11, 12, 9, 13, 14, 15, 16, 17, 18, 19, 20, 
 10, 21, 22, 23, 24]
return

# okay decompiling /home/ctf/Desktop/retool/buu/398935dac2207070e4e6a1e42219f49fbf68c1038e35e4e819bd8e568f1a43a5.pyc
