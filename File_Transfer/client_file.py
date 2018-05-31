#!/usr/bin/python

import socket 

s = socket.socket()
s.connect(('192.168.1.132',5555))
s.send(("Send me that file"))

with open('test.txt','a') as fobj:
    
    buffer = ""
    
    print "Receiving the data now..."
    print

    while True:

        data = s.recv(1024)

        if not data:
            break
        buffer += data

    fobj.write(buffer)

print "File transfer done"
