# -*- coding: utf-8 -*-
# from echo_client import client
# import pytest
# from echo_server import Error404
import os


def test_server_home():
    """Test that html server returns directory listing as html."""
    import urllib2
    response = urllib2.urlopen('http://127.0.0.1:50000/')
    assert response.read() == '<!DOCTYPE html><html><ul><p>. contains:</p><li>a_web_page.html</li><li>images</li><li>make_time.py</li><li>sample.txt</li></ul></html>'


def test_server_html():
    """Test that html server returns HTML file."""
    import urllib2
    response = urllib2.urlopen('http://127.0.0.1:50000/a_web_page.html').read()
    assert response == '<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n'


def test_server_txt():
    """Test that html server returns txt file."""
    import urllib2
    response = urllib2.urlopen('http://127.0.0.1:50000/sample.txt').read()
    assert response == 'This is a very simple text file.\nJust to show that we can server it up.\nIt is three lines long.\n'


def test_server_file():
    """Test that html server returns JPEG."""
    import urllib2
    response = urllib2.urlopen('http://127.0.0.1:50000/images/JPEG_example.jpg').read()
    os.chdir('/Users/mark/projects/network_tools/webroot')
    actual = open('images/JPEG_example.jpg', 'rb').read()
    assert actual == response

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


# def test_response_ok():
#     """Test that function returns appropriate byte string."""
#     from echo_server import response_ok
#     assert response_ok() == \
#         'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\neverything is okay'


# def test_response_error():
#     """Test that function returns appropriate byte string."""
#     from echo_server import response_error
#     assert response_error(404, 'Not Found') == 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nNot Found'


# def test_simple_parse_request():
#     """Test that function returns appropriate URI."""
#     from echo_server import parse_request
#     assert parse_request('GET /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n\r\n') == \
#         '/path/to/index.html'


# def test_put_parse_request():
#     """Test that function returns error when PUT method requested."""
#     from echo_server import parse_request
#     assert parse_request('PUT /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n') == \
#         'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nMethod Not Allowed'


# def test_HTTP10_parse_request():
#     """Test that function returns error on HTTP/1.0 request."""
#     from echo_server import parse_request
#     assert parse_request('GET /path/to/index.html HTTP/1.0\r\nHost: www.host1.com:80\r\n') == \
#         'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


# def test_HTTP20_parse_request():
#     """Test that function returns error on HTTP/2.0 request."""
#     from echo_server import parse_request
#     assert parse_request('GET /path/to/index.html HTTP/2.0\r\nHost: www.host1.com:80\r\n') == \
#         'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


# def test_server():
#     """In response to incoming request, server responds with 200 ok message."""
#     from echo_server import response_ok
#     assert client('GET /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n\r\n') == response_ok()


# def test_server_505():
#     """In response to HTTP20 request, server responds with error."""
#     assert client('GET /path/to/index.html HTTP/2.0\r\nnHost: www.host1.com:80\r\n\r\n') == \
#         'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


# def test_server_405():
#     """In response to HTTP20 request, server responds with error."""
#     assert client('PUT /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n\r\n') == \
#         'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nMethod Not Allowed'


# def test_server_505_2():
#     """In response to HTTP20 SET request, server responds with error."""
#     assert client('SET /path/to/index.html HTTP/2.0\r\nHost: www.host1.com:80\r\n\r\n') == \
#         'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nHTTP Version Not Supported'


# def test_server_url():
#     """Test server by going to URL."""
#     import urllib2
#     response = urllib2.urlopen('http://127.0.0.1:50000/')
#     assert response.read() == 'everything is okay'

# def test_resource_uri_folder():
#     from echo_server import resource_uri
#     uri = 'images'
#     print resource_uri(uri)
#     assert resource_uri(uri) == ('text/html', '<!DOCTYPE html><html><ul><p>images contains:</p><li>JPEG_example.jpg</li><li>sample_1.png</li><li>Sample_Scene_Balls.jpg</li></ul></html>')


# def test_resource_uri_file():
#     from echo_server import resource_uri
#     uri = 'a_web_page.html'
#     print resource_uri(uri)
#     assert resource_uri(uri) == ('text/html', '<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n')


# def test_resource_uri_404():
#     from echo_server import resource_uri
#     uri = 'image'
#     with pytest.raises(Error404):
#         resource_uri(uri)