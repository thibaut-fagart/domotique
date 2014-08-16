#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import dhtreader
from setsnmp import setSnmp

def printlog(datelog,text):
  fileToBeWriten = "/home/dimi/prog/raspberry/leroux/readDhtLog.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()

def readDht(host,oidT,oidH,pin):
  dhtreader.init()
  t, h = dhtreader.read(22, pin)
  if t and h:
      if -40 < t < 60:
        resultT = setSnmp(host,oidT,int(10*t))
      else:
        printlog(time.asctime(), "temperature out of range" )
      if 0 < h < 100:
        resultH = setSnmp(host,oidH,int(10*h))
      else:
        printlog(time.asctime(), "humidity out of range" )
  else:
      printlog(time.asctime(), "Failed to read from sensor, maybe try again?" )
  return t, h, resultT, resultH

