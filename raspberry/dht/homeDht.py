#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from readDht import readDht

gpioBCMPrise1   = [ 4, 0]
gpioHeadPrise1  = [ 7, 0]
gpioBCMPrise2   = [17, 0]
gpioHeadPrise2  = [11, 0]
gpioBCMPrise3   = [27, 0]
gpioHeadPrise3  = [13, 0]
gpioBCMPrise4   = [22, 0]
gpioHeadPrise4  = [15, 0]
gpioBCMPrise5   = [10, 0]
gpioHeadPrise5  = [19, 0]

pinCave      = gpioBCMPrise1[0]
pinExt       = gpioBCMPrise2[0]
pinRasp      = gpioBCMPrise3[0]
pinSalon     = gpioBCMPrise4[0]
pinSdb       = gpioBCMPrise5[0]

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
oidDht22CuisineTemp   = "1.3.6.1.4.1.43689.1.2.2.1.0"
oidDht22CuisineHum    = "1.3.6.1.4.1.43689.1.2.2.2.0"
oidDht22SdbTemp       = "1.3.6.1.4.1.43689.1.2.3.1.0"
oidDht22SdbHum        = "1.3.6.1.4.1.43689.1.2.3.2.0"
oidDht22CaveTemp      = "1.3.6.1.4.1.43689.1.2.8.1.0"
oidDht22CaveHum       = "1.3.6.1.4.1.43689.1.2.8.2.0"
oidDht22RaspTemp      = "1.3.6.1.4.1.43689.1.2.13.1.0"
oidDht22RaspHum       = "1.3.6.1.4.1.43689.1.2.13.2.0"
ipHostSnmp            = "192.168.0.110"

def printlog(datelog,text):
  fileToBeWriten = "/home/dimi/prog/raspberry/home/homeDhtLog.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()   

if __name__ == "__main__":
    print 'Start'
    #readDht(ipHostSnmp,oidDht22ExtTemp,oidDht22ExtHum,pinExt)
    #print 'Ext'
    readDht(ipHostSnmp,oidDht22SdbTemp,oidDht22SdbHum,pinSdb)
    print 'Sdb'
    readDht(ipHostSnmp,oidDht22CuisineTemp,oidDht22CuisineHum,pinCuisine)
    print 'Cuisine'
    readDht(ipHostSnmp,oidDht22SalonTemp,oidDht22SalonHum,pinSalon)
    print 'Salon'
    readDht(ipHostSnmp,oidDht22RaspTemp,oidDht22RaspHum,pinRasp)
    print 'Rasp'
