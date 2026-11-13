text = 'killshadow'
key = 'adsfkndcls'
flag = ''
v5 = len(key)
for i in range(10):   #输入十次字符，所以循环十次
    for j in range(ord('A'), ord('z')+1):  #将所有字母进行尝试，寻找可以使if判断成功的字符
        str2 = (j -39 - ord(key[i % v5]) +97) % 26 + 97 #将原本的加密直接照搬过来，这里需要ord(key[i % v5])是因为python不能直接将字符串转成ascii码
        if chr(str2) == text[i]:  #将算出来的ascii码chr()转成ascii码与text内容比较
            flag += chr(j)    
            break   #这里的break作用是如果if判断成功了一次就结束这个内层循环，开始第二个外层循环，如果没有break会输出很多满足条件的别的字符
print(flag)
