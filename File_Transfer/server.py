#!/usr/bin/python


local_file = raw_input("Which file do you want to send: ")
print


import socket

s = socket.socket()
s.bind(('192.168.1.132',5555))
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
    
            
