# -*- coding: utf-8 -*-
import subprocess


def test_basic(string=u"This is a test."):
    """Test function to test echo server and client with inputted string."""
    process = subprocess.Popen(['./echo_client.py', string],
                               stdout=subprocess.PIPE)
    assert string == process.stdout.readline().rstrip()


def test_exact32():
    """Test echo server and client with string length 32, the buffer size."""
    test_basic(u"12345678901234567890123456789012")


def test_unicode():
    """Test that server and client handle encoding and decoding of unicode."""
    inp = u'Testing «ταБЬℓσ»: 1<2 & 4+1>3, now 20 off!'
    inp = inp.encode('utf-8')
    process = subprocess.Popen(['./echo_client.py', inp],
                               stdout=subprocess.PIPE)
    assert inp == process.stdout.readline().rstrip()


def test_long():
    """Test server and client can handle long messages."""
    test_basic(u"Running the server script in one terminal should allow you to \
        run the client script in a separate terminal. The client script should\
         take an argument which is the message to send.  Upon completing, the \
         response from the server should be printed to stdout.")


def test_response_ok():
    """Test that function returns appropriate byte string."""
    from echo_server import response_ok
    assert response_ok() == 'HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-length: 18\n\r\neverything is okay'


def test_response_error():
    """Test that function returns appropriate byte string."""
    from echo_server import response_error
    assert response_error(404, 'Not Found') == 'HTTP/1.1 404 Not Found'

