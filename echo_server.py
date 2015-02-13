#! /usr/bin/env python
"""Echo server in socket connection: receives and sends back a message."""
import socket
import os
import mimetypes
import binascii


def response_ok(tuple):
    """Return byte string 200 ok response."""
    # u"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\neverything is okay".encode('utf-8')
    okay = u"HTTP/1.1 200 OK\r\nContent-Type: "
    c_len = u"\r\nContent-length: "
    crlf = u"\r\n\r\n"
    return "{}{}{}{}{}{}".format(okay, tuple[0], c_len, len(tuple[1]), crlf, tuple[1])

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

class Error404(BaseException):
    def __init__(self):
        self.out = response_error(404, '404 Not Found')

    def __str__(self):
        return self.out


class Error405(BaseException):
    def __init__(self):
        self.out = response_error(405, '405 Method Not Allowed')

    def __str__(self):
        return self.out


class Error505(BaseException):
    def __init__(self):
        self.out = response_error(505, '505 HTTP Version Not Supported')

    def __str__(self):
        return self.out


def parse_request2(request):
    """Parse HTTP request and returns first line as a list."""
    return request.split("\n")[0].split()


def check_request(first_line):
    """Check HTTP 1.1 and GET, then return uri."""
    print "first_line: {}".format(first_line)
    if first_line[2] != 'HTTP/1.1':
        raise Error505
    if first_line[0] != 'GET':
        raise Error405
    return first_line[1]


def resource_uri(uri):
    """Given URI, returns tuple with a type header and a body.
    If directory, returns html listing of directory.
    If file, returns content of file as body.
    If resource not found, raise Error404.
    """
    # if asking for root change uri to '.'
    if uri == '/':
        uri = '.'
    # remove / from beginning of string
    if uri[0] == '/':
        uri = uri[1:]
    # Determine if directory, file or not found
    if os.access(uri, os.F_OK):
        if os.path.isdir(uri):
            # print directory into html
            head = 'text/html'
            contents = os.listdir(uri)
            body = '<!DOCTYPE html><html><ul><p>{} contains:</p>'.format(uri)
            for file_ in contents:
                body = '{}<li>{}</li>'.format(body, file_)
            body = '{}</ul></html>'.format(body)
        if os.path.isfile(uri):
            head = mimetypes.guess_type(uri)[0]
            body = open(uri, 'rb').read()
        return (head, body)
    else:
        raise Error404


# def tuple_into_response(tup):
#     """Given a tuple with header content-type and body, return response."""
#     return "HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-length: {}\r\n\r\n{}\r\n".format(tup[0], len(tup[1]), tup[1])


if __name__ == '__main__':
    """Run from terminal, this will recieve a messages and send them back."""
    # set root directory appropriately
    os.chdir('/Users/mark/projects/network_tools/webroot')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    buffsize = 4096
    try:
        # After closing a connection, wait for another connection
        while True:
            msg = ''
            done = False
            conn, addr = server_socket.accept()
            # Receive entire message
            while not done:
                msg_part = conn.recv(buffsize)
                msg += msg_part
                if len(msg_part) < buffsize:
                    # # for some reason the server is receiving a blank request
                    # if len(msg) == 0:
                    #     print "msg length 0"
                    #     break
                    done = True
            # Check that msg isn't 0 byte message, that Chrome was sending
            # If not, send back response
            if msg:
                first_line = parse_request2(msg)
                try:
                    uri = check_request(first_line)
                    tupl = resource_uri(uri)
                    out = response_ok(tupl)
                except (Error405, Error505, Error404) as e:
                    out = str(e)
                conn.sendall(out)
            conn.shutdown(socket.SHUT_WR)
            conn.close()
    except KeyboardInterrupt:
        print 'I successfully stopped.'
        server_socket.close()
