import sys, struct
port=int(sys.argv[1])
d=bytearray(open('easytl','rb').read())
imm=0x40447c-0x400000+3
d[imm:imm+4]=struct.pack('<I',port)
open(f'easytl_{port}','wb').write(bytes(d))
print("built easytl_"+str(port))
