#! /usr/bin/env python
"""Echo server in socket connection: receives and sends back a message."""
import socket


def response_ok():
    """Return byte string 200 ok response."""
    return u"HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-length: 18\n\r\neverything is okay".encode('utf-8')


def response_error(error_code, reason):
    """Return byte string error code."""
    return u"HTTP/1.1 {} {}".format(error_code, reason).encode('utf-8')



if __name__ == '__main__':
    """Run from terminal, this will recieve a messages and send them back."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    buffsize = 32
    try:
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
                    conn.shutdown(socket.SHUT_WR)
                    conn.close()
    except KeyboardInterrupt:
        print 'I successfully stopped.'
        server_socket.close()
