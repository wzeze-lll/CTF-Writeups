import base64
sum = "e3nifIH9b_C@n@dH"
flag = ""
l=len(sum)
for i in range(0,l):
    flag +=chr(ord(sum[i]) - i)
print(base64.b64decode(flag))