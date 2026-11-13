"""Reproduce the output branch in MainActivity; registration input is separate."""
x = list(map(ord, "dd2940c04462b4dd7c450528835cca15"))
x[2] = x[2] + x[3] - 50
x[4] = x[2] + x[5] - 48
x[30] = x[31] + x[9] - 48
x[14] = x[27] + x[28] - 97
for index in range(16):
    x[index], x[31 - index] = x[31 - index], x[index]
print("flag{" + "".join(map(chr, x)) + "}")
