#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from readDHT import readDHT

gpioBCMPrise1   = [ 27, 22, 10,  9, 11]
gpioHeadPrise1  = [ 13, 15, 19, 21, 23]
gpioTagPrise1   = [ 'Prise1-0', 'Prise1-1', 'ThermoNew', 'ThermoOld', 'Sdb']
gpioBCMPrise2   = [ 24, 25,  8,  7]
gpioHeadPrise2  = [ 18, 22, 24, 26]
gpioTagPrise2   = [ 'Prise2-0', 'Rasp', 'Cuisine', 'Prise2-3']
gpioBCMPrise3   = [ 23]
gpioHeadPrise3  = [ 16]
gpioTagPrise3   = [ 'Ext']
#gpioBCMPrise4   = [ 14, 15, 18]
#gpioHeadPrise4  = [  8, 10, 12]
#gpioListBCMWhite    = [  4, 17]
#gpioListHeadWhite   = [  7, 11]

pinExt       = [gpioBCMPrise3[0], gpioTagPrise3[0]]
pinThermoOld = [gpioBCMPrise1[3], gpioTagPrise1[3]]
pinThermoNew = [gpioBCMPrise1[2], gpioTagPrise1[2]]
pinSdb       = [gpioBCMPrise1[4], gpioTagPrise1[4]]
pinCuisine   = [gpioBCMPrise2[2], gpioTagPrise2[2]]
pinRasp      = [gpioBCMPrise2[1], gpioTagPrise2[1]]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise1:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise3:
  GPIO.setup(pin, GPIO.IN)

if __name__ == "__main__":
    print readDHT(pinExt[0])
    print readDHT(pinSdb[0])
    print readDHT(pinThermoOld[0])
    print readDHT(pinThermoNew[0])
    print readDHT(pinCuisine[0])
    print readDHT(pinRasp[0])

