#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from readDHT import readDHTSnmp

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
pinSdbNew    = [gpioBCMPrise1[4], gpioTagPrise1[4]]
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

if __name__ == "__main__":
  try:
    readDHTSnmp(ipHostSnmp,oidDht22ExtTemp,oidDht22ExtHum,pinExt)
  except:
    print "fail"

  try:
    readDHTSnmp(ipHostSnmp,oidDht22SdbNewTemp,oidDht22SdbNewHum,pinSdbNew)
  except:
    print "fail"

  try:
    readDHTSnmp(ipHostSnmp,oidDht22ThermoOldTemp,oidDht22ThermoOldHum,pinThermoOld)
  except:
    print "fail"

  try:
    readDHTSnmp(ipHostSnmp,oidDht22ThermoNewTemp,oidDht22ThermoNewHum,pinThermoNew)
  except:
    print "fail"

  try:
    readDHTSnmp(ipHostSnmp,oidDht22CuisineTemp,oidDht22CuisineHum,pinCuisine)
  except:
    print "fail"

  try:
    readDHTSnmp(ipHostSnmp,oidDht22RaspTemp,oidDht22RaspHum,pinRasp)
  except:
    print "fail"

