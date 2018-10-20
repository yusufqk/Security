#!/usr/bin/python

"""
*Taken and Adapted from the great book Black Hat Python
*I need to learn how the Resume section works
"""

import urllib2
import threading
import Queue
import urllib
import base64
from colorama import Fore

workers = 50
target = "http://192.168.1.110"
wordlist_file = "all.txt"
resume = None
user_agent = "Googlebot"

def build_wordlist(wordlist_file):

    with open(wordlist_file,'rb') as fobj:
        raw_words = fobj.readlines()

    
    found_resume = None
    words = Queue.Queue()

    for word in raw_words:

        word = word.rstrip() #must get rid of \r and \n

        if resume is not None:

            if found_resume:
                words.put(word) #This is how you resume a script after interruption
            else:
                if word == resume:
                    found_resume = True
                    print "[*] Resuming wordlist from: %s" % resume
        
        else:
            words.put(word)

    return words


def dir_bruter(word_queue):

    while not word_queue.empty():
        
        attempt = word_queue.get()
        
        attempt_list = []

        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)

        for brute in attempt_list:

            url = "%s%s" % (target,urllib.quote(brute))
            
            try:
                headers = {}
                headers["User-Agent"] = user_agent
                #headers["Connection"] = "keep-alive"
                #headers["Upgrade-Insecure-Requests"] = 1
                request = urllib2.Request(url,headers=headers)
                response = urllib2.urlopen(request)
                
                if len(response.read()):
                    if response.code == 200:
                        print Fore.GREEN + "[*] " + "[" + str(response.code) + "]" + " ==> " + url + Fore.RESET

            except urllib2.URLError,e:

                if hasattr(e,'code') and e.code != 404:
                    print "[!] [%d] ==> %s" % (e.code,url)
                pass


word_queue = build_wordlist(wordlist_file)
                                            #I IMPORTED A FUNCTION, HAD TO GET RID OF THESE LINES
for i in range(workers):
    t = threading.Thread(target=dir_bruter(word_queue))
    t.start()


















