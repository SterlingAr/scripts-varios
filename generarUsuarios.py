#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:42:38 2017

@author: marius
"""

import string
import random
import sh
from sh import passwd
from sh import useradd
groupName = input("Introduce el nombre del grupo(obligatorio): ")


#useradd -m -g groupName -s /bin/bash userName
def generateUsers(quant,groupName,passwd):
    for i in range(quant+1):
        useradd("-m", "-g", groupName, "-s")
        print(str(i))

generateUsers(50)

random.choices(string.ascii_uppercase + string.digits, k=4)

