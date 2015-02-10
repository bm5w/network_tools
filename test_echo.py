# -*- coding: utf-8 -*-
import subprocess
import pytest


def test_basic(string="This is a test."):
    """Test function to test echo server and client with inputted string."""
    process = subprocess.Popen(['./echo_client.py', string],
                               stdout=subprocess.PIPE)
    assert string == process.stdout.readline().rstrip()


def test_exact32():
    """Test echo server and client with string length 32, the buffer size."""
    test_basic("12345678901234567890123456789012")


def test_unicode():
    """Test that server and client handle decoding and encoding of unicode."""
    with pytest.raises(AssertionError):
        inp = 'Testing «ταБЬℓσ»: 1<2 & 4+1>3, now 20 off!'
        inp = inp.decode('utf-8')
        process = subprocess.Popen(['./echo_client.py', inp],
                                   stdout=subprocess.PIPE)
        assert inp == process.stdout.readline().rstrip()


def test_long():
    """Test server and client can handle long messages."""
    test_basic("Running the server script in one terminal should allow you to \
        run the client script in a separate terminal. The client script should\
         take an argument which is the message to send.  Upon completing, the \
         response from the server should be printed to stdout.")
