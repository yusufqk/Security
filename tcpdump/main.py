#!/usr/bin/python

from tcpdump_parse import MrMeeSeeks

test = MrMeeSeeks()

check = test.check_ip()

if check:
    print "valid ip address"
    print
    test.parse_dump()

else:
    print "not valid"



