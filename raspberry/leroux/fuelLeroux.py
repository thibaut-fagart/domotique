#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from setsnmp import setSnmp

gpioBCMPrise2   = [ 23, 24]
gpioHeadPrise2  = [ 16, 18]

pinFuel      = gpioBCMPrise2[1]

literPerSecond = 4.6/3600

oidFuelBurningTime  = "1.3.6.1.4.1.43689.1.5.1.0"
oidFuelBurnt        = "1.3.6.1.4.1.43689.1.5.2.0"
oidFuelRemaining    = "1.3.6.1.4.1.43689.1.5.3.0"
ipHostSnmp          = "192.168.0.199"

GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)


if __name__ == "__main__":
  fuelFileData = "/home/dimi/prog/raspberry/leroux/fuelFileData.txt"
  time.sleep(20)
  fileReadWrite = open(fuelFileData,'r')
  fuelData = fileReadWrite.read().split()
  burningTime   = float(fuelData[0])
  fuelBurnt     = float(fuelData[1])
  fuelRemaining = float(fuelData[2])
  fileReadWrite.close() 
  setSnmp(ipHostSnmp,oidFuelBurningTime,int(burningTime))
  setSnmp(ipHostSnmp,oidFuelBurnt,int(fuelBurnt))
  setSnmp(ipHostSnmp,oidFuelRemaining,int(fuelRemaining))
  counter = 0
  previousTime = time.time()

  while True:
    counter = counter + 1
    if GPIO.input(pinFuel):
      deltaBurningTime = time.time() - previousTime
      previousTime = time.time()
      burningTime   = burningTime + deltaBurningTime
      print burningTime
      fuelBurnt     = fuelBurnt + deltaBurningTime * literPerSecond
      fuelRemaining = fuelRemaining - deltaBurningTime * literPerSecond
    if counter > 60:
      counter = 0
      fileReadWrite = open(fuelFileData,'w')
      stringReadWrite = str(burningTime)+' '+str(fuelBurnt)+' '+str(fuelRemaining)
      fileReadWrite.write(stringReadWrite)
      fileReadWrite.close() 
    time.sleep(1)
