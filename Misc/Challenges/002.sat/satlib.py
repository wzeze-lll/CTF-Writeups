#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""卫星测控站 CTF —— 帧封装 / CCSDS / CFDP 编解码工具。
用法：被 recon.py、exploit.py import。
"""
import struct, socket, time, sys

HOST = "127.0.0.1"
PORT = 24619

# ----------------------------------------------------------------------------
# 一、外层帧封装（题面：C / F / T / E 四种帧，首字节标类型）
#     因为无附件，封装格式必须黑盒试。这里实现 5 种常见形态。
# ----------------------------------------------------------------------------
MODES = ("len2be", "len4be", "len2le", "raw", "hexline")


def frame(kind, body, mode="len2be"):
    """kind: b'C'/b'F'/b'T'/b'E' 单字节；body: bytes"""
    k = kind if isinstance(kind, bytes) else kind.encode()
    if mode == "len2be":
        return k + struct.pack(">H", len(body)) + body
    if mode == "len4be":
        return k + struct.pack(">I", len(body)) + body
    if mode == "len2le":
        return k + struct.pack("<H", len(body)) + body
    if mode == "raw":
        return k + body
    if mode == "hexline":
        return k + b" " + body.hex().encode() + b"\n"
    raise ValueError(mode)


def unframe(buf, mode="len2be"):
    """把收到的裸流拆成 [(kind, body)]，失败返回剩余字节。"""
    out, i = [], 0
    while i < len(buf):
        kind = buf[i:i + 1]
        if kind not in (b"C", b"F", b"T", b"E"):
            break
        if mode == "raw":
            out.append((kind, buf[i + 1:])); return out, b""
        if mode == "hexline":
            j = buf.find(b"\n", i)
            if j < 0: break
            out.append((kind, bytes.fromhex(buf[i + 2:j].decode())))
            i = j + 1
            continue
        hl = 2 if mode.startswith("len2") else 4
        if i + 1 + hl > len(buf): break
        n = int.from_bytes(buf[i + 1:i + 1 + hl], "big" if mode.endswith("be") else "little")
        if i + 1 + hl + n > len(buf): break
        out.append((kind, buf[i + 1 + hl:i + 1 + hl + n]))
        i += 1 + hl + n
    return out, buf[i:]


# ----------------------------------------------------------------------------
# 二、CCSDS 空间包（遥控 TC / 遥测 TM）
# ----------------------------------------------------------------------------
def ccsds_packet(apid, data, ptype=1, seqcnt=0, sechdr=0):
    """ptype=1: TC(命令)  ptype=0: TM(遥测)"""
    pkt_id = (0 << 13) | (ptype << 12) | (sechdr << 11) | (apid & 0x7FF)
    seq = (3 << 14) | (seqcnt & 0x3FFF)
    hdr = struct.pack(">HHH", pkt_id, seq, max(len(data) - 1, 0))
    return hdr + data


def ccsds_tc(apid, fcode, args=b""):
    """最常见的落地形态：数据域 = 功能码(2B) + 参数"""
    return ccsds_packet(apid, struct.pack(">H", fcode) + args, ptype=1)


def parse_ccsds(pkt):
    if len(pkt) < 6:
        return None
    pkt_id, seq, ln = struct.unpack(">HHH", pkt[:6])
    return {
        "ver": pkt_id >> 13, "type": (pkt_id >> 12) & 1, "sechdr": (pkt_id >> 11) & 1,
        "apid": pkt_id & 0x7FF, "seqflags": seq >> 14, "seqcnt": seq & 0x3FFF,
        "len": ln, "data": pkt[6:6 + ln + 1],
    }


# ----------------------------------------------------------------------------
# 三、CFDP PDU（CCSDS 727.0-B 经典头）
# ----------------------------------------------------------------------------
DIRECTIVES = {
    "EOF": 0x04, "FINISHED": 0x05, "ACK": 0x06, "METADATA": 0x07,
    "NAK": 0x08, "PROXY_PUT_REQ": 0x09, "PROXY_PUT_RESP": 0x0A, "KEEPALIVE": 0x0B,
    # 备选（部分实现用 0x00 起编）
    "EOF_ALT": 0x00, "FINISHED_ALT": 0x01, "ACK_ALT": 0x02, "METADATA_ALT": 0x03,
}


def cfdp_pdu(pdu_type, direction=0, mode=0, data=b"", src=0, dst=0, txn=1,
             crc=False, large=False):
    b0 = (0 << 5) | ((pdu_type & 1) << 4) | ((direction & 1) << 3) | \
         ((mode & 1) << 2) | ((1 if crc else 0) << 1) | (1 if large else 0)
    hdr = struct.pack(">B", b0) + struct.pack(">H", len(data))
    # entity id 长度：large=8B else 2B
    f = ">Q" if large else ">H"
    hdr += struct.pack(f, src) + struct.pack(">I", txn) + struct.pack(f, dst)
    return hdr + data


def lv(b):
    return bytes([len(b)]) + b


def cfdp_metadata(src_name, dst_name, cr=False, checksum_type=0, directive=0x07):
    """File Directive PDU: Metadata。src_name 是发送方本地路径，就是穿越点。"""
    d = bytes([directive])
    d += bytes([((0 & 0xF) << 4) | ((1 if cr else 0) << 3) | (0 << 2) | (checksum_type & 0x3)])
    d += lv(src_name.encode() if isinstance(src_name, str) else src_name)
    d += lv(dst_name.encode() if isinstance(dst_name, str) else dst_name)
    return d


def cfdp_filedata(offset, chunk, directive=0x00):
    return bytes([directive]) + struct.pack(">I", offset) + chunk


def cfdp_eof(size=0, crc=0, offset=0, directives_=None, directive=0x04):
    return bytes([directive]) + struct.pack(">I", size) + struct.pack(">I", crc)


# ----------------------------------------------------------------------------
# 四、会话
# ----------------------------------------------------------------------------
class Session:
    def __init__(self, host=HOST, port=PORT, timeout=6.0):
        self.s = socket.create_connection((host, port), timeout=timeout)
        self.s.settimeout(timeout)
        self.buf = b""

    def send(self, data):
        self.s.sendall(data)
        return self

    def recv_raw(self, t=2.0):
        self.s.settimeout(t)
        try:
            d = self.s.recv(65536)
        except socket.timeout:
            return b""
        except OSError:
            return b"<RST>"
        self.buf += d
        return d

    def drain(self, t=2.0, until=3.0):
        """读到静默 until 秒"""
        t0 = time.time(); out = b""
        while time.time() - t0 < t:
            d = self.recv_raw(until)
            if not d:
                break
            out += d
            if d == b"<RST>":
                break
        return out

    def close(self):
        try: self.s.close()
        except Exception: pass


if __name__ == "__main__":
    print("frame len2be C:", frame("C", b"\x00\x01").hex())
    print("ccsds_tc:", ccsds_tc(0x064, 0x0001).hex())
    print("cfdp md:", cfdp_pdu(0, 1, 0, cfdp_metadata("/cf/host/flag", "/cf/station/x")).hex())
