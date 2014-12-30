#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pysnmp.proto import rfc1902

RaspberryPath = "/home/prog/raspberry"

class Fuel :
  def __init__(self):
    self.oidFuelBurningTime  = "1.3.6.1.4.1.43689.1.5.1.0"
    self.oidFuelBurnt        = "1.3.6.1.4.1.43689.1.5.2.0"
    self.oidFuelRemaining    = "1.3.6.1.4.1.43689.1.5.3.0"
  
  def readFuelData(self):
    fuelFileData = RaspberryPath + "/leroux/LogFuelData.log"
    with open(fuelFileData, 'r') as fileReadWrite:
      fuelData = fileReadWrite.read().split()
    self.burningTime = float(fuelData[0])
    self.fuelBurnt = float(fuelData[1])
    self.fuelRemaining = float(fuelData[2])
  def toSnmpBurningTime(self):
    return (self.oidFuelBurningTime, rfc1902.Integer(self.burningTime))
  def toSnmpFuelBurnt(self):
    return (self.oidFuelBurnt, rfc1902.Integer(self.fuelBurnt))
  def toSnmpFuelRemaining(self):
    return (self.oidFuelRemaining, rfc1902.Integer(self.fuelRemaining))
