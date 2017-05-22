#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 12:47:56 2017
@author: marius


Script sencillo para cambiar a resoluciones personalizadas más rápido en linux. 

Para utilizar primero hace falta instalar el módulo 'sh'

En ubuntu:
    sudo apt-get install pip
    sudo pip install sh
En archlinux:
    sudo pacman -S pip
    sudo pip install sh

@storeCurrentResolution(): función para salvaguardar la resolución actual
@revertOrApplyChanges(resolution): función para cambiar la resolución del display actual.
@listConnectedDisplays()
@genNewModline(width,height,selectedDisplay): funcion para generar línea de modificaciones para la nueva resolución usando 'cvt'




"""
import sh
import os
from sh import xrandr
from sh import cvt
import sys


def storeCurrentResolution():
    
    Xaxis = os.popen("xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f1")
    readXaxis = Xaxis.read()
    
    Yaxis = os.popen("xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f2")
    readYaxis = Yaxis.read()
    
    resolutionBackup = readXaxis+"x"+readYaxis
    return resolutionBackup.replace("\n","")

def revertOrApplyChanges(resolution):
    
    xrandr("-s",resolution)
    
    

def listConnectedDisplays():
    
    connectedDisplays=os.popen("xrandr | grep -w connected  | awk -F'[ +]' '{print $1}'")
    readDisplays = connectedDisplays.read()
    return readDisplays.split()#devuelve como lista



def genNewModline(width,height,selectedDisplay):
    
   fullModline =os.popen("cvt "+str(width)+" "+str(height))
   readModline = fullModline.read().split("Modeline ",1)[1]
   os.system("xrandr --newmode "+readModline)
   os.system("xrandr --addmode "+selectedDisplay+" "+readModline.split()[0])
   print(readModline)



##logica de control
resolutionBackup = storeCurrentResolution()

userInput = input("Introduce la resolución en el siguiente formato  1440 900: \n")

listInput = userInput.split()

if len(listInput) > 0 :
    
    listDisplays = listConnectedDisplays()
    
    print("Selecciona una pantalla:\n")
    
    for i in range(0,len(listDisplays)):
        
        print(str(i)+". "+listDisplays[i])
        
    selectedDisplay = int(input("\nIntroduce: "))
    
    if selectedDisplay >= 0 and selectedDisplay <= len(listDisplays)-1:
        
        askUser=input("Estás seguro de añadir la resolución? S/n").lower()
        
        if askUser == 's' or askUser == 'y' or askUser == 'yes' or askUser == 'si':
            
            genNewModline(listInput[0],listInput[1],listDisplays[selectedDisplay])
            
            askUserAgain=input("Quieres aplicar la nueva resolución? S/n").lower()
            
            if askUserAgain == 's' or askUserAgain == 'y' or askUserAgain == 'yes' or askUserAgain == 'si':
                
                newResolution = listInput[0]+"x"+listInput[1]
                
                revertOrApplyChanges(newResolution)
                
                keepChanges = input("Quieres mantener los cambios? S/n")
                
                if keepChanges == 's' or keepChanges == 'y' or keepChanges == 'yes' or keepChanges == 'si':
                    
                    print("Resolución "+newResolution+"aplicada al display: "+listDisplays[selectedDisplay])
                    
                else:
                    
                    revertOrApplyChanges(resolutionBackup)
       
else:
    
    print("no has introducido nada")

