#! /usr/bin/env python
"""Echo client in socket connection: sends and receives a message."""
import sys
import socket


if __name__ == '__main__':
    """When called from terminal, creates a socket connection with a server.
    Send the argument from the command line, recieve a message and print
    to command line."""
    inputted = sys.argv[1]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(inputted)
    client_socket.shutdown(socket.SHUT_WR)
    buffsize = 32
    done = False
    msg = ''
    while not done:
        msg_part = client_socket.recv(buffsize)
        msg += msg_part
        if len(msg_part) < buffsize:
            done = True
            client_socket.close()
    sys.stdout.write('{}'.format(msg))
