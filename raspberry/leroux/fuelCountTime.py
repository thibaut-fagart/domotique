#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO

RaspberryPath = "/home/prog/raspberry"

gpioBCMPrise2   = [ 23, 24]
gpioHeadPrise2  = [ 16, 18]

pinFuel      = gpioBCMPrise2[1]

literPerSecond = 4.6/3600

GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)


if __name__ == "__main__":
  fuelFileData = RaspberryPath + "/leroux/LogFuelData.log"
  time.sleep(20)
  fileReadWrite = open(fuelFileData,'r')
  fuelData = fileReadWrite.read().split()
  burningTime   = float(fuelData[0])
  fuelBurnt     = float(fuelData[1])
  fuelRemaining = float(fuelData[2])
  fileReadWrite.close() 
  counter = 0
  previousTime = time.time()

  while True:
    counter = counter + 1
    if GPIO.input(pinFuel):
      deltaBurningTime = time.time() - previousTime
      burningTime   = burningTime + deltaBurningTime
      fuelBurnt     = fuelBurnt + deltaBurningTime * literPerSecond
      fuelRemaining = fuelRemaining - deltaBurningTime * literPerSecond
    previousTime = time.time()
    if counter > 60:
      counter = 0
      fileReadWrite = open(fuelFileData,'w')
      stringReadWrite = str(burningTime)+' '+str(fuelBurnt)+' '+str(fuelRemaining)
      fileReadWrite.write(stringReadWrite)
      fileReadWrite.close() 
    time.sleep(1)
