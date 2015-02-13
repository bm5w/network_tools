"""Tests for html server, v3. Starts server with fixture."""
import os
import sys
import pytest
import urllib2
from html_server import html_response
import threading


def test_server_home(start_server):
    """Test that html server returns directory listing as html."""
    response = urllib2.urlopen('http://localhost:7474/')
    assert response.read() == '<!DOCTYPE html><html><ul><p>. contains:</p><li><a href="./a_web_page.html">a_web_page.html</a></li><li><a href="./images">images</a></li><li><a href="./make_time.py">make_time.py</a></li><li><a href="./sample.txt">sample.txt</a></li></ul></html>'


def test_server_html(start_server):
    """Test that html server returns HTML file."""
    response = urllib2.urlopen('http://localhost:7474/a_web_page.html').read()
    assert response == '<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n'


def test_server_txt(start_server):
    """Test that html server returns txt file."""
    response = urllib2.urlopen('http://localhost:7474/sample.txt').read()
    assert response == 'This is a very simple text file.\nJust to show that we can server it up.\nIt is three lines long.\n'


def test_server_file(start_server):
    """Test that html server returns JPEG."""
    response = urllib2.urlopen('http://localhost:7474/images/JPEG_example.jpg').read()
    os.chdir('/Users/mark/projects/network_tools/webroot')
    actual = open('images/JPEG_example.jpg', 'rb').read()
    assert actual == response


def test_server_error_HTTP10():
    """Test that html server returns error on HTTP/1.0 request."""
    assert html_response('GET /path/to/index.html HTTP/1.0\r\nHost: www.host1.com:80\r\n') == \
        'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 26\r\n\r\nHTTP Version Not Supported'


def test_server_error_HTTP20():
    """Test that html server returns error on HTTP/2.0 request."""
    assert html_response('GET /path/to/index.html HTTP/2.0\r\nHost: www.host1.com:80\r\n') == \
        'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\nContent-length: 26\r\n\r\nHTTP Version Not Supported'


def test_server_error_server_404():
    """In response to HTTP20 request, server responds with correct error."""
    with pytest.raises(urllib2.HTTPError) as error:
        urllib2.urlopen('http://localhost:7474/images/JPEG_example2.jpg')
    assert str(error.value) == 'HTTP Error 404: Not Found'


def test_server_error_server_405():
    """In response to PUT request, server responds with correct error."""
    assert html_response('PUT /path/to/index.html HTTP/1.1\r\nHost: www.host1.com:80\r\n\r\n') == \
        'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-length: 18\r\n\r\nMethod Not Allowed'


@pytest.fixture(scope='session')
def start_server():
    """Fixture to start server for tests. """
    print 'started fixture'
    target = None
    # if len(sys.argv) > 1:
    #     server_method = sys.argv.pop(1)
    #     if server_method not in ['select', 'gevent']:
    #         print "server method must be one of 'select' or 'gevent'"
    #         sys.exit(1)
    #     if server_method == 'select':
    #         from select_echo_server import server as target
    #     else:
    #         from gevent.server import StreamServer
    #         from gevent_echo_server import echo
    #         from gevent.monkey import patch_all
    #         patch_all()
    #         server = StreamServer(('localhost', 7474), echo)
    #         target = server.serve_forever
    # else:
    from html_server import start as target

    server_thread = threading.Thread(target=target)
    server_thread.daemon = True
    server_thread.start()
    print 'server started'
