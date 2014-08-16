#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
from setsnmp import setSnmp

oidFuelBurningTime  = "1.3.6.1.4.1.43689.1.5.1.0"
oidFuelBurnt        = "1.3.6.1.4.1.43689.1.5.2.0"
oidFuelRemaining    = "1.3.6.1.4.1.43689.1.5.3.0"
ipHostSnmp          = "192.168.0.199"

if __name__ == "__main__":
  fuelFileData = "/home/dimi/prog/raspberry/leroux/fuelFileData.txt"
  fileReadWrite = open(fuelFileData,'r')
  fuelData = fileReadWrite.read().split()
  burningTime   = float(fuelData[0])
  fuelBurnt     = float(fuelData[1])
  fuelRemaining = float(fuelData[2])
  fileReadWrite.close() 
  setSnmp(ipHostSnmp,oidFuelBurningTime,int(burningTime))
  setSnmp(ipHostSnmp,oidFuelBurnt,int(fuelBurnt))
  setSnmp(ipHostSnmp,oidFuelRemaining,int(fuelRemaining))
