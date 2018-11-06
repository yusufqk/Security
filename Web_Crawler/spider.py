#!/usr/bin/python

"""

Author: Yusuf Kassim

This script will crawl through a target website to find web content. The wordlist and target ip 
will be given as command-line arguments

"""

import sys
import threading
import Queue
import urllib
import urllib2
import base64
import time
from colorama import Fore


class DarkArmy(object):

    def __init__(self):

        self.wordlist = sys.argv[1]
        self.target = "http://"+sys.argv[2]
        self.workers = 45
        self.user_agent = "Googlebot"
        self.progress = list("[--------------------]")

    def buildpaths(self):
        
        with open(self.wordlist,'rb') as fobj:

            word = fobj.read().splitlines()
        
        paths_list = []

        for i in range(len(word)):
            
            if "." in word[i]:
                paths_list.append("/%s" % word[i])
            else:
                paths_list.append("/%s/" % word[i])
        
        mr_robot = Queue.Queue()

        for i in range(len(paths_list)):

            mr_robot.put(paths_list[i])

        
        return mr_robot,mr_robot.qsize()

    
    def crawl(self,mr_robot,size):
        
        count = 0
        progress_count = 0

        while not mr_robot.empty():
            
            count += 1
            
            fraction = int(size/20)

            percentage = int(float(count)/float(size) * 100)

            if count%fraction == 0:

                progress_count += 1

                self.progress[progress_count] = "#"

                sys.stdout.write("".join(self.progress) + " " + str(percentage) + "% "  + "\r")
                sys.stdout.flush()

            else:
                sys.stdout.write("".join(self.progress) + " "  +str(percentage) + "% " +"\r")
                sys.stdout.flush()

            if percentage == 100:

                print
                print
                print "[*] Crawl is Complete. Goodbye Mr.MeeSeeks!"
                time.sleep(1)
                sys.exit()
            


            attack = mr_robot.get()

            url_path = "%s%s" % (self.target,urllib.quote(attack))            
            
            try:

                headers = {}
                headers["User-Agent"] = self.user_agent
                request = urllib2.Request(url_path,headers=headers)
                response = urllib2.urlopen(request)

            except urllib2.URLError,e:

                if e.code == 404:
                    continue
                else:
                    print "[!] [%d] ==> %s+\n" % (e.code,url_path)

            else:
                        
                if len(response.read()):
                    if response.code == 200:
                        print Fore.GREEN + "[*] " + "[" + str(response.code) + "]" + " ==> " + url_path +"\n"+ Fore.RESET


    def main(self):
        
        mr_robot,size = self.buildpaths()
        
        for i in range(self.workers):
            t = threading.Thread(target=self.crawl(mr_robot,size))
            t.start()

        
try:
    test = DarkArmy()
except:
    print "Usage Example: './spider.py <name of wordlist> <IP of target>"
else:
    print
    print "[*] I'm Mr.MeeSeeks! Look at me!"
    print
    time.sleep(2)
    print "[*] Let's web crawl " + sys.argv[2]
    time.sleep(2)
    print

    test.main()


