#!/usr/bin/python

#The client code will connect to the server and obtain the file

import socket 

s = socket.socket()
s.connect(('<server ip adress>',5555))
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
