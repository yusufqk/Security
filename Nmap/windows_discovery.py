#!/usr/bin/python

import socket

class Rocket(object):


    def __init__(self):
        self.ports = [21,22,25,80,139,445]
        self.responses = ["Microsoft","Windows"]

 
    def HansSolo(self,ip,port):

        #print ip,port

        try:
                                   
            y = socket.socket()
            y.settimeout(2)
            y.connect((ip,port))
            response = y.recv(1024)
            for item in self.responses:
                if item in response:
                    print "%s:%d  %s" % (ip,port,response)
        except:
            pass
            #print "[!] Connection refused for %s:%d" % (ip,port)

                  
        

    def ChewBacca(self,windows):

        for ip in windows:

            for port in self.ports:
                
                self.HansSolo(ip,port)
                












