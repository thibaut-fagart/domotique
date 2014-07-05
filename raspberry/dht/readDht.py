#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import dhtreader
from setsnmp import setSnmp
from getsnmp import getSnmp

def readDht(host,oidT,oidH,pin):
  dhtreader.init()
  t, h = dhtreader.read(22, pin)
  if t and h:
      resultT = setSnmp(host,oidT,int(10*t))
      resultH = setSnmp(host,oidH,int(10*h))
  else:
      print "Failed to read from sensor, maybe try again?"
  return t, h, resultT, resultH

