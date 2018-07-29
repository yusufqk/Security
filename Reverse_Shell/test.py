#!/usr/bin/python



def welcome():

    print "[1] monthly [2] Weekly"


welcome()
choice = raw_input("Please enter an option: ")
print

while choice.lower() != "quit":

    if choice.lower() == "monthly":
        print "montly"
    elif choice.lower()  == "weekly":
        with open("datap","rb") as fobj:
            data = fobj.read()
        print data
    else:
        print "choose an option"

    
    welcome()
    choice = raw_input("Please enter an option: ")
    print



