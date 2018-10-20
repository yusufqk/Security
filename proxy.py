#!/usr/bin/python

"""

Author: Yusuf Kassim

This script is designed to overcome the shortcomings of proxying.py, a tcp proxy script 
that can handle multiple client requests simutaneously. 

https://twistedmatrix.com/documents/current/core/howto/servers.html

"""

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from hexdump import hexdump
import optparse
import socket


twister ="""
     |__   __|     (_)   | |
        | |_      ___ ___| |_ ___ _ __ 
        | \ \ /\ / / / __| __/ _ \ '__|
        |    |\ V  V /| \__ \ ||  __/   
        |_| \_/\_/ |_|___/\__\___|_| 
"""
print twister

class Proxy(Protocol):

    def __init__(self,remote_host,remote_port):
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.proxy = socket.socket()
        self.proxy.connect((self.remote_host,self.remote_port))
 

    def dataReceived(self,data):
        
        print "[===>] Received %d bytes from client" % len(data)
        hexdump(data)
        self.proxy.send(data)

        print "[===>] Sent to remote"
        print

        response = self.proxy.recv(4096)

        if response:

            print "[<===] Received %d bytes from remote" % len(response)
            hexdump(response)
            self.transport.write(response)
            print "[<===] Sent to client"
            print 

class Main(Factory):

    def __init__(self,remote_host,remote_port):

        self.remote_host = remote_host
        self.remote_port = remote_port

    def buildProtocol(self,addr):

        return Proxy(self.remote_host,self.remote_port)

    
def data():

    parser = optparse.OptionParser("usage: %prog" + " -host [remote host] -port [remote port]")
    parser.add_option("--host",dest="remote_host",type="string",help="specify remote host")
    parser.add_option("--port",dest="remote_port",type="int",help="specify remote port")
    (options,args) = parser.parse_args()

    remote_host = options.remote_host
    remote_port = options.remote_port

    if remote_host == None or remote_port == None:
        parser.error("[!] Error: please specify target correctly")
    
    return remote_host,remote_port


remote_host,remote_port = data()

reactor.listenTCP(9999,Main(remote_host,remote_port))
reactor.run()


