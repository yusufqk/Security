#!/usr/bin/python

import sys
import time
from geoip import open_database
from colorama import Fore

class MrMeeSeeks(object):
        

    def check_ip(self):

        numbers = []
        for i in range(0,256):

            numbers.append(str(i))

        self.address = raw_input("Whats the source ip address: ")

        breakdown = self.address.split(".")

        if len(breakdown) != 4:
            print "not a valid ip"
            sys.exit()

        count = 0
        for i in range(len(breakdown)):

            first = breakdown[i]

            if first in numbers:
                count += 1

        if count == 4:
            return True
        else:
            return False
    
    def auxillary(self,string):

        pieces = string.find(">")
        first_ip = string[:pieces]
        second_ip = string[pieces+1:len(string)].strip()
         
        list1 = first_ip.split(".")[-1]
        find_port1 = first_ip.find(list1)
        first_real = first_ip[:find_port1-1]
        
        list2 = second_ip.split(".")[-1]
        find_port2 = second_ip.find(list2)
        second_real = second_ip[:find_port2-1]


        return first_real,second_real
    
    def filter(self,final,ip_address):
        
        output = []

        for i in range(len(final)):

            if final[i][0][0] == ip_address:

                output.append(final[i])
        
        return output

    def sort_list(self,result):

        numbers = []

        for i in range(len(result)):

            numbers.append(result[i][2])
        
        sorted_num = sorted(numbers,reverse=True)

        real_list = []

        for num in range(len(sorted_num)):
            
            for ip in range(len(result)):
                
                if sorted_num[num] == result[ip][2]:
                    
                    real_list.append(result[ip])
                    break
        
        return real_list


    def parse_dump(self):

        with open('tcpdump_file.txt', 'rb') as fobj:
            lines = fobj.read().splitlines()
        
        final = []

        for i in range(len(lines)):
            
            if "length" not in lines[i]:
                continue

            first = lines[i].find("IP")
            second = lines[i].find("Flags")
            ip_ports = lines[i][first + 2:second - 2].strip()

            size_where = lines[i].find("length")
            size = lines[i][size_where + 7:len(lines[i])]
            
            first_ip,second_ip = self.auxillary(ip_ports)
            
            output = [[],[],0,""]

            output[0].append(first_ip)
            output[1].append(second_ip)
            output[2] += int(size)
            output[3] = output[0][0].strip() + "-" + output[1][0].strip()

                    
            final.append(output)
        
        result = self.filter(final,self.address)

        real_list = self.sort_list(result)


        mr_robot = {}
            
        for i in range(len(real_list)):

            dst = real_list[i][1][0]
            size = real_list[i][2]
            
            if dst in mr_robot:
                mr_robot[dst] += size
            else:
                mr_robot[dst] = size

        
        sort_num = []

        for k,v in mr_robot.items():

            sort_num.append(v)

        sort_num = sorted(sort_num, reverse=True)

        ordered = []

        for i in range(len(sort_num)):
            for k,v in mr_robot.items():

                if sort_num[i] == mr_robot[k]:

                    ordered.append(k)
                    break
        
        print "Source IP"+"\t" + "Destination IP"+"\t" + "Packet Size"
        print

        for i in range(len(sort_num)):

            print self.address+"\t" + ordered[i]+"\t" + str(sort_num[i])


        db = open_database('/home/binyamin/Downloads/GeoLite2-City_20181023/GeoLite2-City.mmdb')

        print
        

        print Fore.GREEN + "[*] Calculating locations for top 5 IP addresses..." + Fore.RESET
        print
        time.sleep(2)
        print "IP address"+"\t" + "    "+"\t" + "Country"+"\t" + "Coordinates"
        print

        for i in range(5):

            match = db.lookup(ordered[i])
            
            if match is not None:

                x,y = str(match.location[0]), str(match.location[1])

                print ordered[i]+"\t" + " --->"+"\t" + match.country+"\t" + x+","+y

            else:

                continue






















