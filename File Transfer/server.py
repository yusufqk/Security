#!/usr/bin/python

#This code is a small module that can be used when file transfer is required
#The client code will connect and request the transfer

local_file = raw_input("Which file do you want to send: ")
print


import socket

s = socket.socket()
s.bind(('<ip address>',5555))
s.listen(5)

print "Listening to transfer files..."
print

while True:

    conn,addr = s.accept()
    print "Incoming connection from" , addr
    print
    data = conn.recv(1024)
    if data:
        print "Server recieved", str(data)
        print

    with open(local_file,'rb') as fobj:
        y = fobj.read()
    

    conn.send(y)
    print "Sending " + local_file
    print
    
    conn.close()

    print "Transfer complete!!!"
    
            
