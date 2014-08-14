#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO

gpioBCMPrise1   = [ 27, 22, 10,  9, 11]
gpioHeadPrise1  = [ 13, 15, 19, 21, 23]
gpioBCMPrise2   = [ 23, 24, 25,  8,  7]
gpioHeadPrise2  = [ 16, 18, 22, 24, 26]
gpioBCMPrise3   = [ 14, 15, 18]
gpioHeadPrise3  = [  8, 10, 12]
gpioListBCMWhite    = [  4, 17]
gpioListHeadWhite   = [  7, 11]

pinExt       = gpioBCMPrise2[3]
pinThermoOld = gpioBCMPrise1[3]
pinThermoNew = gpioBCMPrise1[2]
pinCuisine   = gpioBCMPrise2[4]
pinRasp      = gpioBCMPrise2[2]
pinEdf       = gpioBCMPrise2[0]
pinFuel      = gpioBCMPrise2[1]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise1:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)


def printlog(datelog,text):
  fileToBeWriten = "/home/dimi/prog/raspberry/leroux/log.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()   

if __name__ == "__main__":
  printlog(time.asctime(),str(GPIO.input(pinFuel)))
