#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO

RaspberryPath = "/home/prog/raspberry"

pinFuel = 24

literPerSecond = 4.6/3600

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinFuel, GPIO.IN)


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
