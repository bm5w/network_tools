# -*- coding: utf-8 -*-
import subprocess
import pytest


def test_basic(string="This is a test."):
    process = subprocess.Popen(['./echo_client.py', string],
                               stdout=subprocess.PIPE)
    assert string == process.stdout.readline()


def test_unicode():
    with pytest.raises(AssertionError):
        inp = 'Testing «ταБЬℓσ»: 1<2 & 4+1>3, now 20 off!'
        inp = inp.decode('utf-8')
        process = subprocess.Popen(['./echo_client.py', inp],
                                   stdout=subprocess.PIPE)
        assert inp == process.stdout.readline()


def test_long():
    test_basic("Running the server script in one terminal should allow you to run \
        the client script in a separate terminal. The client script should\
        take an argument which is the message to send.  Upon completing, the\
        response from the server should be printed to stdout.")


def test_exact():
    test_basic("input me")


