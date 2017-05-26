#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:42:38 2017

@author: marius
"""

import string
import random
from sh import passwd
from sh import useradd
from sh import chpasswd
from sh import echo
from sh import groupadd
from sh import cat
from sh import grep
import csv



#useradd -m -g groupName -s /bin/bash userName
#chage -d 0 userName  


def exportToCSV(listOfUsers):
    with open("users.csv",'wt') as csvfile:
        
        spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        for i in range(0, len(listOfUsers)):
            
        
        spamwriter.writerow([listOfUsers[0], 'Password'])

exportToCSV()

def generateUsers(quant,groupName):
    
    userRow = []
    listOfUsers = []
    
    try:
        
        
        doesGroupExist = grep(cat("/etc/passwd"), "asdasda")
        print(doesGroupExist)
    except Exception:
            
        print("No existe el grupo, créandolo...")
            
        groupadd(groupName)
    
    for i in range(quant+1):
        userRow = []
        randomUserName = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        userName = groupName+randomUserName
        randomPasswd = ''.join(random.SystemRandom().
                               choice(string.ascii_uppercase +
                                      string.digits +
                                      string.ascii_letters +
                                      string.punctuation) for _ in range(25))
        
        userRow.append(userName)
        userRow.append(groupName)
        userRow.append(randomPasswd)
        listOfUsers.append(userRow)
        
            
        useradd("-m", "-g", groupName, "-s", "/bin/bash", userName)
            
        chpasswd(echo(str(userName+":"+randomPasswd)))
        
    return listOfUsers
    
            


quant = int(input("introduce el número de usuarios: "))
groupName = input("introduce el nombre del grupo: ")

listOfUsers = generateUsers(quant,groupName)
exportToCSV(listOfUsers)
