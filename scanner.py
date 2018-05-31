#!/usr/bin/python

"""

Author: Yusuf Kassim

This script will conduct a scan that will find all Webservers and Windows Servers on a subnet.
The scan will start with a ping scan to find all machines that are alive. Web servers
will be discovered using the urllib module, where any machine responding to a HTTP GET
request is assumed to be hosting a web service. Windows Servers will be discovered by scanning
the ports unique to the Windows OS. This will be done using the socket module looking for ports 135,139,and 445.

https://github.com/johanlundberg/python-nmap/blob/master/nmap/example.py

"""

import nmap
import sys
import optparse
import urllib2
import socket
from datetime import datetime
from colorama import Fore

class StormTrooper(object):
    
    def ping_sweep(self,target):

        ping = nmap.PortScanner()

        try:
            
            print
            print "[*] Initiating ping scan now..."
            print
            ping.scan(hosts=target,arguments="-n -sP")

        except:

            print "[!] An error has occured with the ping scan. Check configurations"
            print
            sys.exit()

        else:
            
            ping_list = ping.all_hosts()
            print "[*] The following device(s) have been found..."
            print

            for ip in ping_list:

                print "\t%s" % ip
            
            print

            return ping_list

    def scanner(self,ping_list):

        
        print
        print "[*] Scanning all live hosts..."
        print

        ping_list = " ".join(ping_list)

        scanner = nmap.PortScanner()

        try:
            scanner.scan(hosts=ping_list,arguments="-v -A -sV --version-intensity 5")
        except:
            print
            print "[!] Error. Check configuration. Exiting Scan"
            print
            sys.exit()
        else:

            for item in scanner.all_hosts():
                
                print
                print Fore.GREEN + "Information for " + item + Fore.RESET
                print
                print "\thostname: %s" % scanner[item].hostname()
                print "\tState: %s" % scanner[item].state()

                for protocol in scanner[item].all_protocols():

                    
                    print
                    print "\tProtocol: %s" % protocol
                    ports = list(scanner[item][protocol].keys())
                    ports.sort()
                    for port in ports:

                        #print "\t\tport: %s, state: %s" % (port, scanner[item][protocol][port]['state'])
                        
                        if scanner[item][protocol][port]['state'].lower() == 'open':

                            try:
                                c = socket.socket()
                                c.settimeout(2)
                                c.connect((item,port))
                                c.send("GET HTTP/1.1 \r\n")
                                response = c.recv(1024)

                            except:

                                print "\t\tport: %s, state: %s" % (port, scanner[item][protocol][port]['state'])                                
                            else:
                                print "\t\tport: %s, service: %s" % (port,response)
                                c.close()
                        else:
                            print "\t\tport: %s, state: %s" % (port, scanner[item][protocol][port]['state'])
        

        
            


    def web(self,ping_list):

        print
        print "[*] Finding all webservers now..."
        print
        
        webs = []

        for ip in ping_list:
            
            headers = {}
            headers["User-Agent"] = "Googlebot"
            url = "http://" + ip

            try:
                request = urllib2.Request(url,headers=headers)
                response = urllib2.urlopen(request,timeout=2)
                if response.code == 200:
                    print "[%d] ===> %s" % (response.code,ip)
                    webs.append(ip)
            except:
                pass

        return webs


    def windows_machines(self,ping_list):

        ports = [139,445]
        windows = []
        
        print
        print "[*] Checking socket connections for commonly used ports on Windows Machines..."
        print

        for ip in ping_list:
            for port in ports:

                try:
                    y = socket.socket()
                    y.settimeout(2)
                    y.connect((ip,port))
                except:
                    continue
                else:
                    print "%s:%d" % (ip,port)
                    windows.append(ip)
        
        windows = list(set(windows))

        return windows




    def main(self):

        parser = optparse.OptionParser("usage: %prog " + "-t [target subnet]")
        parser.add_option("-t","--target",dest="target",type="string",help="specify target address")
        (options,args) = parser.parse_args()
        target = options.target

        if target == None:
            parser.error("[!] Error. Please enter a target")

        else:

            ping_list = self.ping_sweep(target)
            
            self.scanner(ping_list)

            #webs = self.web(ping_list)
            
            #for ip in webs:
            #    with open("webservers.txt","a") as fobj:
            #        fobj.write(ip+"\n")
            
            #windows = self.windows_machines(ping_list)

            #DarthVader = Rocket()
            
            #print
            #print "[*] The following are POSSIBLY Windows Machines. Be careful, you might be tricked!"
            #print

            #DarthVader.ChewBacca(windows)
                   

Darkness = StormTrooper()
Darkness.main()
