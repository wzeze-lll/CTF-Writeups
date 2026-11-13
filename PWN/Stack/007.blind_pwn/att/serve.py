#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把这道题按"能看见退出码"的方式部署起来（模拟远端）

  * fork 子进程跑 ./ld-linux-x86-64.so.2 --library-path . ./pwn
  * 双向转发字节
  * 子进程退出后，往连接里补一行:  EXIT=<退出码>
    —— 这样 blind pwn 的 exit-code 外带信道就成立了

用法:
    python3 serve.py 8888            # 本机
    # 然后用:  python3 exp_blind.py REMOTE=127.0.0.1:8888 EXIT_REPORT=1
"""
import os, sys, socket, subprocess, threading, select

HERE = os.path.dirname(os.path.abspath(__file__))
CMD = ["./ld-linux-x86-64.so.2", "--library-path", ".", "./pwn"]


def pump(src, dst, stop):
    try:
        while not stop.is_set():
            r, _, _ = select.select([src], [], [], 0.2)
            if not r:
                continue
            data = src.recv(4096) if isinstance(src, socket.socket) else os.read(src, 4096)
            if not data:
                break
            if isinstance(dst, socket.socket):
                dst.sendall(data)
            else:
                os.write(dst, data)
    except Exception:
        pass
    finally:
        try:
            stop.set()
        except Exception:
            pass


def handle(conn):
    p = subprocess.Popen(CMD, cwd=HERE, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         bufsize=0)
    stop = threading.Event()
    t1 = threading.Thread(target=pump, args=(conn, p.stdin.fileno(), stop), daemon=True)
    t2 = threading.Thread(target=pump, args=(p.stdout.fileno(), conn, stop), daemon=True)
    # 用 socket 版本的 join：两个方向任意一个结束就收尾
    t1.start(); t2.start()

    # 等子进程结束（它要么退出，要么被 kill），最多 30s
    try:
        rc = p.wait(timeout=30)
    except subprocess.TimeoutExpired:
        p.kill(); rc = -9
    # 把子进程剩余输出冲出来
    try:
        rest = p.stdout.read()
        if rest:
            conn.sendall(rest)
    except Exception:
        pass
    try:
        conn.sendall(b"\nEXIT=%d\n" % (rc & 0xff if rc >= 0 else 128 - rc))
    except Exception:
        pass
    for s in (conn,):
        try:
            s.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            s.close()
        except Exception:
            pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", port))
    srv.listen(16)
    print("[*] listening on 0.0.0.0:%d" % port, flush=True)
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    main()
