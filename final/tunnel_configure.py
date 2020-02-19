# for input parsing 
import os
import csv
with open('input.csv') as csvfile:
    filep = csv.reader(csvfile, delimiter=',')
    next(filep, None)
    for line in filep:
        if line == []:
            break
        elif line[2]=="L3":
           os.system("sudo python l3.py "+line[0]+" "+line[1])
        elif line[2]=="Bridge":
           os.system("sudo python l2.py "+line[0]+" "+line[1])
        elif line[2]=="VXLAN":
           os.system("sudo python vxlan.py "+line[0]+" "+line[1])
        elif line[2]=="GRE":
           os.system("sudo python gre.py "+line[0]+" "+line[1])
        else:
           print("please enter input in correct format")                              
