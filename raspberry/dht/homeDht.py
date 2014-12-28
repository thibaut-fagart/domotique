#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from readDht import readDht

RaspberryPath = "/home/prog/raspberry"

gpioBCMPrise1   = [ 4]
gpioHeadPrise1  = [ 7]
gpioBCMPrise2   = [17]
gpioHeadPrise2  = [11]
gpioBCMPrise3   = [27]
gpioHeadPrise3  = [13]
gpioBCMPrise4   = [ 9]
gpioHeadPrise4  = [21]
gpioBCMPrise5   = [11]
gpioHeadPrise5  = [23]

pinSdb       = gpioBCMPrise1[0]
pinSalon     = gpioBCMPrise2[0]
pinExt       = gpioBCMPrise3[0]
pinRasp      = gpioBCMPrise4[0]
pinCave      = gpioBCMPrise5[0]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise1:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise3:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise4:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise5:
  GPIO.setup(pin, GPIO.IN)

oidDht22ExtTemp       = "1.3.6.1.4.1.43689.1.2.1.1.0"
oidDht22ExtHum        = "1.3.6.1.4.1.43689.1.2.1.2.0"
oidDht22SalonTemp     = "1.3.6.1.4.1.43689.1.2.4.1.0"
oidDht22SalonHum      = "1.3.6.1.4.1.43689.1.2.4.2.0"
oidDht22SdbTemp       = "1.3.6.1.4.1.43689.1.2.3.1.0"
oidDht22SdbHum        = "1.3.6.1.4.1.43689.1.2.3.2.0"
oidDht22CaveTemp      = "1.3.6.1.4.1.43689.1.2.8.1.0"
oidDht22CaveHum       = "1.3.6.1.4.1.43689.1.2.8.2.0"
oidDht22RaspTemp      = "1.3.6.1.4.1.43689.1.2.13.1.0"
oidDht22RaspHum       = "1.3.6.1.4.1.43689.1.2.13.2.0"
ipHostSnmp            = "192.168.0.110"

def printlog(datelog,text):
  fileToBeWriten = RaspberryPath + "/home/homeDhtLog.log"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()   

if __name__ == "__main__":
#  try:
#    readDht(ipHostSnmp,oidDht22CaveTemp,oidDht22CaveHum,pinCave)
#  except:
#    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinCave)

  try:
    readDht(ipHostSnmp,oidDht22SalonTemp,oidDht22SalonHum,pinSalon)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinSalon)

  try:
    readDht(ipHostSnmp,oidDht22ExtTemp,oidDht22ExtHum,pinExt)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinExt)

  try:
    readDht(ipHostSnmp,oidDht22RaspTemp,oidDht22RaspHum,pinRasp)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinRasp)

  try:
    readDht(ipHostSnmp,oidDht22SdbTemp,oidDht22SdbHum,pinSdb)
  except:
    printlog(time.asctime(),' : no dht22 answer from pin %s sensor'%pinSdb)
