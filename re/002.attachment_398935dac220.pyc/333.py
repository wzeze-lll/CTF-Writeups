
code = [
    '\x1f', '\x12', '\x1d', '(', '0', '4',
    '\x01', '\x06', '\x14', '4', ',', '\x1b',
    'U', '?', 'o', '6', '*', ':',
    '\x01', 'D', ';', '%', '\x13'
]

l = len(code)

# 第一步：逆向 XOR
for i in range(l - 2, -1, -1):
    a = ord(code[i])
    b = ord(code[i + 1])

    value = a ^ b
    code[i] = chr(value)

# 第二步：撤销加下标
flag = ""

for i in range(l):
    a = ord(code[i])
    value = (a - i) % 128
    flag += chr(value)

print(flag)
