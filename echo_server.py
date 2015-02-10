#! /usr/bin/env python
import socket


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    buffsize = 32
    while True:
        msg = ''
        done = False
        conn, addr = server_socket.accept()
        while not done:
            msg_part = conn.recv(buffsize)
            msg += msg_part
            if len(msg_part) < buffsize:
                done = True
                conn.sendall(msg)
                conn.close()
