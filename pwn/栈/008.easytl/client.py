#!/usr/bin/env python3
import socket, ssl, struct, hashlib, sys, time

HOST = sys.argv[1] if len(sys.argv) > 1 else "host.docker.internal"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 1443

CMD_ADD     = 0x38432A87
CMD_ENC     = 0x6C5A5850
CMD_DEC     = 0x363BBED5
CMD_GET     = 0x89954D3E
CMD_UPD     = 0xDC375626
CMD_DEL     = 0xD21FEF03

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.minimum_version = ssl.TLSVersion.TLSv1_3
ctx.maximum_version = ssl.TLSVersion.TLSv1_3

s = socket.create_connection((HOST, PORT), timeout=10)
ss = ctx.wrap_socket(s)
print("[*] tls:", ss.version(), ss.cipher())

def send(cmd, payload=b""):
    ss.sendall(struct.pack("<I", cmd) + payload)
    time.sleep(0.15)

def recv(n, t=2.0):
    ss.settimeout(t)
    try:
        return ss.recv(n)
    except socket.timeout:
        return b""

key = b"A"*16
iv  = b"B"*16
data = b"hello world"
sha = hashlib.sha256(data).digest()

send(CMD_ADD, key + iv + struct.pack("<I", len(data)) + data)
send(CMD_GET, sha[:16])
print("[*] get ->", ss.recv(4096))

send(CMD_ENC, sha[:16])
send(CMD_GET, sha[:16])
r = ss.recv(4096)
print("[*] after enc get ->", r.hex())

send(CMD_DEC, sha[:16])
send(CMD_GET, sha[:16])
print("[*] after dec get ->", ss.recv(4096))

# update: new data
nd = b"second"
send(CMD_UPD, sha[:16] + struct.pack("<I", len(nd)) + nd)
send(CMD_GET, hashlib.sha256(nd).digest()[:16])
print("[*] after upd get(newhash) ->", ss.recv(4096))

# delete
send(CMD_DEL, hashlib.sha256(nd).digest()[:16])
print("[*] deleted")
time.sleep(0.2)
try:
    send(CMD_GET, hashlib.sha256(nd).digest()[:16])
    print("[*] get after delete ->", ss.recv(4096))
except Exception as e:
    print("[!] conn died:", e)
