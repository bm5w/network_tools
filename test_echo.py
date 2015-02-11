# -*- coding: utf-8 -*-
from echo_client import client


# def test_basic(string=u"This is a test."):
#     """Test function to test echo server and client with inputted string."""
#     process = subprocess.Popen(['./echo_client.py', string],
#                                stdout=subprocess.PIPE)
#     assert string == process.stdout.readline().rstrip()


# def test_exact32():
#     """Test echo server and client with string length 32, the buffer size."""
#     test_basic(u"12345678901234567890123456789012")


# def test_unicode():
#     """Test that server and client handle encoding and decoding of unicode."""
#     inp = u'Testing «ταБЬℓσ»: 1<2 & 4+1>3, now 20 off!'
#     inp = inp.encode('utf-8')
#     process = subprocess.Popen(['./echo_client.py', inp],
#                                stdout=subprocess.PIPE)
#     assert inp == process.stdout.readline().rstrip()


# def test_long():
#     """Test server and client can handle long messages."""
#     test_basic(u"Running the server script in one terminal should allow you to \
#         run the client script in a separate terminal. The client script should\
#          take an argument which is the message to send.  Upon completing, the \
#          response from the server should be printed to stdout.")


def test_response_ok():
    """Test that function returns appropriate byte string."""
    from echo_server import response_ok
    assert response_ok() == \
        'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\neverything is okay'


def test_response_error():
    """Test that function returns appropriate byte string."""
    from echo_server import response_error
    assert response_error(404, 'Not Found') == 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nNot Found'


def test_simple_parse_request():
    """Test that function returns appropriate URI."""
    from echo_server import parse_request
    assert parse_request('GET /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n\r\n') == \
        '/path/to/index.html'


def test_put_parse_request():
    """Test that function returns error when PUT method requested."""
    from echo_server import parse_request
    assert parse_request('PUT /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n') == \
        'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nMethod Not Allowed'


def test_HTTP10_parse_request():
    """Test that function returns error on HTTP/1.0 request."""
    from echo_server import parse_request
    assert parse_request('GET /path/to/index.html HTTP/1.0\r\nHost: www.host1.com:80\r\n') == \
        'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


def test_HTTP20_parse_request():
    """Test that function returns error on HTTP/2.0 request."""
    from echo_server import parse_request
    assert parse_request('GET /path/to/index.html HTTP/2.0\r\nHost: www.host1.com:80\r\n') == \
        'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


def test_server():
    """In response to incoming request, server responds with 200 ok message."""
    from echo_server import response_ok
    assert client('GET /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n\r\n') == response_ok()


def test_server_505():
    """In response to HTTP20 request, server responds with error."""
    assert client('GET /path/to/index.html HTTP/2.0\r\nnHost: www.host1.com:80\r\n\r\n') == \
        'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


def test_server_405():
    """In response to HTTP20 request, server responds with error."""
    assert client('PUT /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n\r\n') == \
        'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nMethod Not Allowed'


def test_server_505_2():
    """In response to HTTP20 SET request, server responds with error."""
    assert client('SET /path/to/index.html HTTP/2.0\r\nHost: www.host1.com:80\r\n\r\n') == \
        'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


def test_server_url():
    """Test server by going to URL."""
    import urllib2
    response = urllib2.urlopen('http://127.0.0.1:50000/')
    assert response.read() == 'everything is okay'
