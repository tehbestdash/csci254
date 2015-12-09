import socket
import sys
import os.path
import string

"""def isRead(file):
    try:
        f = open(file, 'r')
        f.close()
 
    except IOError as e:
        return False 
    return True"""


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 8000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
inF = open('proj4.html', "r")
outF = open('proj4o.html', "w")
line = inF.read()
files = " "
fails = " "
sock.listen(1)

while True:

#   command = message[:3]
#   else if command == "GET"


    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    count = 0

    try:
        print >>sys.stderr, 'connection from', client_address
        while True:
            data = connection.recv(100000)
            path = data[4:]
            command = data[:3]
            if data == "CLOSE":
                connection.close()
                print >>sys.stderr, 'files read: "%s"' %count
                print >>sys.stderr, 'closing...'
                result = line.replace("%NUMBER%", str(count), 3)
                result = result.replace("%FILE%", files, 3)
                result = result.replace("%FAILS%", fails,3)
                print outF.write(result)
                break

            if command != "GET" or len(data) == 0:
                print >>sys.stderr, 'Bad Request'
                print >>sys.stderr, 'recieved "%s"' % data
                connection.sendall('400 Bad Request')


            elif command == "GET":

                if len(path) == 0:
                    print >>sys.stderr, 'not even a space'
                    connection.sendall('no space sent')

                elif path == "/STATUS":
                    connection.sendall('Server is Running')

                elif path[0] == "/":
                    fileName = path[1:]

                    if os.path.isfile(fileName):
                        files += fileName
                        files += " "
                        count = count + 1
                        f = open(fileName, 'r')
                        ztringz = f.read()
                        print >>sys.stderr, 'recieved "%s"' % data
                        print >>sys.stderr, 'file sent to client'
                        connection.sendall(ztringz)
                        print >>sys.stderr, 'files read: "%s"' %count

                    else:
                        fails += fileName
                        fails += " "
                        print >>sys.stderr, 'FILE NOT FOUND'
                        connection.sendall('404 Not Found')


                else:
                    print >>sys.stderr, 'nothing sent to client'
                    connection.sendall('NOTHINGisHERE')

                    #   break

                #   else:
                #       print >>sys.stderr, 'FILE NOT FOUND'
                #       connection.sendall('404 Not Found')
                #       break           
                #   break

            else:
                print >>sys.stderr, 'command not recognized'

        break

    finally:
        connection.close()
