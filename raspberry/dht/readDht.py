#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import Adafruit_DHT
from setsnmp import setSnmp
from timeout import timeout

def printlog(datelog,text):
  fileToBeWriten = "/home/dimi/prog/raspberry/dht/readDhtLog.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()

def readDht(host,oidT,oidH,pin):
  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
  if humidity is not None and temperature is not None:
      if -40 < temperature < 60:
        resultT = setSnmp(host,oidT,int(10*temperature))
      else:
        printlog(time.asctime(), "temperature out of range for pin : %s on host %s"%(pin,host) )
      if 0 < humidity < 100:
        resultH = setSnmp(host,oidH,int(10*humidity))
      else:
        printlog(time.asctime(), "humidity out of range for pin : %s on host %s"%(pin,host) )
      return temperature, humidity, resultT, resultH
  else:
      printlog(time.asctime(), "Failed to read from sensor on pin : %s on host %s"%(pin,host) )

