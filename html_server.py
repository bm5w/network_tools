#! /usr/bin/env python
"""Echo server in socket connection: receives and sends back a message."""
import os
import mimetypes


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


class Error404(BaseException):
    def __init__(self):
        self.out = response_error(404, 'Not Found')

    def __str__(self):
        return self.out


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


def get_message(socket, address):
    buffsize = 4096
    msg = ''
    # Receive entire message
    while True:
        # msg_part = conn.recv(buffsize)
        msg_part = socket.recv(buffsize)
        msg += msg_part
        if len(msg_part) < buffsize:
            break
    # Check that msg isn't 0 byte message, that Chrome was sending
    # If not, generate response
    if msg:
        out = html_response(msg)
        socket.sendall(out)
    socket.close()


def html_response(msg):
    """Generate response from request."""
    first_line = parse_request2(msg)
    try:
        uri = check_request(first_line)
        tupl = resource_uri(uri)
        out = response_ok(tupl)
    except (Error405, Error505, Error404) as e:
        out = str(e)
    return out


def start():
    """Run from terminal, this will recieve a messages and send them back."""
    # set root directory appropriately
    os.chdir('/Users/mark/projects/network_tools/webroot')
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 50000), get_message)
    print('Starting echo server on port 50000')
    server.serve_forever()

if __name__ == '__main__':
    start()
