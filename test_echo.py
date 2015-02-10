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
    process = subprocess.Popen(['./echo_client.py', inp],
                               stdout=subprocess.PIPE)
    assert inp == process.stdout.readline().rstrip().decode('utf-8')


def test_long():
    """Test server and client can handle long messages."""
    test_basic(u"Running the server script in one terminal should allow you to \
        run the client script in a separate terminal. The client script should\
         take an argument which is the message to send.  Upon completing, the \
         response from the server should be printed to stdout.")
