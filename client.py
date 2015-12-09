#  GNU nano 2.2.6                 File: client.py                                         

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



server_address = ('localhost', 8000)
print >>sys.stderr, 'starting up on %s port %s ' % server_address
sock.connect(server_address)


while True:

    message = raw_input("enter a command: ")
    if message == "CLOSE":
        print >>sys.stderr, 'closing socket'
        sock.sendall(message)
        sock.close()
        break
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < 1:
        data = sock.recv(100000)
        amount_received = amount_received + 1
        print >>sys.stderr, 'received "%s"' % data
        if data == "":
            print >>sys.stderr, 'received infinity'
            break





