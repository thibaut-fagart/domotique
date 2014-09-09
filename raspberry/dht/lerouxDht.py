#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from readDht import readDht

gpioBCMPrise1   = [ 27, 22, 10,  9, 11]
gpioHeadPrise1  = [ 13, 15, 19, 21, 23]
gpioBCMPrise2   = [ 24, 25,  8,  7]
gpioHeadPrise2  = [ 18, 22, 24, 26]
gpioBCMPrise3   = [ 23]
gpioHeadPrise3  = [ 16]
#gpioBCMPrise4   = [ 14, 15, 18]
#gpioHeadPrise4  = [  8, 10, 12]
#gpioListBCMWhite    = [  4, 17]
#gpioListHeadWhite   = [  7, 11]

pinExt       = gpioBCMPrise3[0]
pinThermoOld = gpioBCMPrise1[3]
pinThermoNew = gpioBCMPrise1[2]
pinCuisine   = gpioBCMPrise2[2]
pinRasp      = gpioBCMPrise2[1]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise1:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise3:
  GPIO.setup(pin, GPIO.IN)

oidDht22ExtTemp       = "1.3.6.1.4.1.43689.1.2.1.1.0"
oidDht22ExtHum        = "1.3.6.1.4.1.43689.1.2.1.2.0"
oidDht22CuisineTemp   = "1.3.6.1.4.1.43689.1.2.2.1.0"
oidDht22CuisineHum    = "1.3.6.1.4.1.43689.1.2.2.2.0"
oidDht22ThermoOldTemp = "1.3.6.1.4.1.43689.1.2.9.1.0"
oidDht22ThermoOldHum  = "1.3.6.1.4.1.43689.1.2.9.2.0"
oidDht22ThermoNewTemp = "1.3.6.1.4.1.43689.1.2.10.1.0"
oidDht22ThermoNewHum  = "1.3.6.1.4.1.43689.1.2.10.2.0"
oidDht22SdbOldTemp    = "1.3.6.1.4.1.43689.1.2.11.1.0"
oidDht22SdbOldHum     = "1.3.6.1.4.1.43689.1.2.11.2.0"
oidDht22SdbNewTemp    = "1.3.6.1.4.1.43689.1.2.12.1.0"
oidDht22SdbNewHum     = "1.3.6.1.4.1.43689.1.2.12.2.0"
oidDht22RaspTemp      = "1.3.6.1.4.1.43689.1.2.13.1.0"
oidDht22RaspHum       = "1.3.6.1.4.1.43689.1.2.13.2.0"
ipHostSnmp            = "192.168.0.199"

def printlog(datelog,text):
  fileToBeWriten = "/home/dimi/prog/raspberry/leroux/lerouxDhtLog.log"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()   

if __name__ == "__main__":
  try:
    readDht(ipHostSnmp,oidDht22ExtTemp,oidDht22ExtHum,pinExt)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinExt)
  try:
    readDht(ipHostSnmp,oidDht22ThermoOldTemp,oidDht22ThermoOldHum,pinThermoOld)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinThermoOld)
  try:
    readDht(ipHostSnmp,oidDht22ThermoNewTemp,oidDht22ThermoNewHum,pinThermoNew)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinThermoNew)
  try:
    readDht(ipHostSnmp,oidDht22CuisineTemp,oidDht22CuisineHum,pinCuisine)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinCuisine)
  try:
    readDht(ipHostSnmp,oidDht22RaspTemp,oidDht22RaspHum,pinRasp)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinRasp)
