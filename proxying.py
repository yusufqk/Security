#!/usr/bin/python

"""
Author: Yusuf Kassim

This script is a tcp proxy that will be used to pivot on a network
Initially made to relay between devices communiacting via netcat
*Taken from BlackHat, but modified to my liking. This proxy cannot 
handle more than one request at a time. I must look into asynchronous
sockets. 
"""

import sys
import time
import socket
import threading
from hexdump import hexdump
import optparse

def Hernan_Cortes(local_host,local_port,remote_host,remote_port):

    server = socket.socket()
    server.bind((local_host,local_port))
    
    print "[*] Listening on %s:%d" % (local_host,local_port)

    server.listen(5)

    while True:


        client_socket,addr = server.accept()
        print
        print "[===>] Recieved connection from %s:%d" % (addr[0],addr[1])
        
        proxy_thread = threading.Thread(target=Montezuma(client_socket,remote_host,remote_port))
        proxy_thread.start()

def Aztec(socket):

    string = ""
    socket.settimeout(1)

    try:
        while True:
            data = socket.recv(4096)
            if not data:
                break
            string += data
    except:
        pass
    return string


def Conquistador(local_buffer):

    local_buffer = local_buffer + "Modifying the request"
    return local_buffer

def Mayans(remote_buffer):

    remote_buffer = remote_buffer + "I noticed the change"
    return remote_buffer



def Montezuma(client_socket,remote_host,remote_port):

    remote_socket = socket.socket()
    remote_socket.connect((remote_host,remote_port))

    while True:

        local_buffer = Aztec(client_socket)

        if len(local_buffer):

            print "[===>] Recieved %d bytes from client." % len(local_buffer)
            
            
            hexdump(local_buffer)

            #local_buffer = Conquistador(local_buffer)
        

            remote_socket.send(local_buffer)

            print "[===>] Sent to remote"
            print

        remote_buffer = Aztec(remote_socket)

        if len(remote_buffer):

            print "[<===] Recieved %d bytes from remote host." % len(remote_buffer)
            hexdump(remote_buffer)

            #remote_buffer = Mayans(remote_buffer)

            client_socket.send(remote_buffer)

            print "[<===] Sent to client"
            print


def Quetzalcoatl():


    parser = optparse.OptionParser("usage: %prog" + " -l [localhost] -p [local port] -r [remote host] -x [remote port]")
    parser.add_option("-l","--localhost",dest="local_host",type="string",help="specify local target")
    parser.add_option("-p","--localport",dest="local_port",type="int",help="specify local port")
    parser.add_option("-r","--remotehost",dest="remote_host",type="string",help="specify remote target")
    parser.add_option("-x","--remoteport",dest="remote_port",type="int",help="specify remote port")

    (options,args) = parser.parse_args()
    
    local_host = options.local_host
    local_port = options.local_port
    remote_host = options.remote_host
    remote_port = options.remote_port
    
    if local_host == None:
        parser.error("[!] Error: you must specify a traget")

    Hernan_Cortes(local_host,local_port,remote_host,remote_port)



Quetzalcoatl()



