#! /usr/bin/env python
"""Echo server in socket connection: receives and sends back a message."""
import socket


def response_ok():
    """Return byte string 200 ok response."""
    return u"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\neverything is okay".encode('utf-8')


def response_error(error_code, reason):
    """Return byte string error code."""
    return u"HTTP/1.1 {} {}\r\nContent-Type: text/plain\r\nContent-length: {}\r\n\r\n{}".format(error_code, reason, len(reason), reason).encode('utf-8')


# def parse_request(request):
#     """Parse HTTP request and return URI requested.
#     If not GET requests, raises error.
#     If not HTTP/1.1 request, raises error."""
#     first_line = request.split("\n")[0].split()
#     if first_line[2] == 'HTTP/1.1':
#         if first_line[0] == 'GET':
#             return first_line[1]
#         else:
#             return response_error(405, 'Method Not Allowed')
#     else:
#         return response_error(505, 'HTTP Version Not Supported')


class Error405(BaseException):
    def __init__(self):
        self.out = response_error(405, 'Method Not Allowed')

    def __str__(self):
        return self.out


class Error505(BaseException):
    def __init__(self):
        self.out = response_error(505, 'HTTP Version Not Supported')

    def __str__(self):
        return self.out


def parse_request2(request):
    """Parse HTTP request and returns first line as a list."""
    return request.split("\n")[0].split()


def check_request(first_line):
    if first_line[2] != 'HTTP/1.1':
        raise Error505
    if first_line[0] != 'GET':
        raise Error405
    return response_ok()

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
                    # print 'msg:\n{}'.format(msg)
                    done = True
                    first_line = parse_request2(msg)
                    try:
                        out = check_request(first_line)
                    except (Error405, Error505) as e:
                        out = str(e)
                    # print 'response:\n{}'.format(out)
                    conn.sendall(out)
                    conn.shutdown(socket.SHUT_WR)
                    conn.close()
    except KeyboardInterrupt:
        print 'I successfully stopped.'
        server_socket.close()
