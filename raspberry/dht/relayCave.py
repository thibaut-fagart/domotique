#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from setsnmp import setSnmp
from getsnmp import getSnmp

oidArduinoCaveTemp = "1.3.6.1.4.1.36582.1"
oidArduinoCaveHum  = "1.3.6.1.4.1.36582.2"
oidDht22CaveTemp   = "1.3.6.1.4.1.43689.1.2.8.1.0"
oidDht22CaveHum    = "1.3.6.1.4.1.43689.1.2.8.2.0"
ipHostCave        = "192.168.0.71"
ipHostSnmp        = "192.168.0.110"

if __name__ == "__main__":

  oidCaveTemp, tempCave = getSnmp(ipHostCave,oidArduinoCaveTemp)
  resultSetT = setSnmp(ipHostSnmp,oidDht22CaveTemp,int(tempCave))

  oidCaveHum, humCave = getSnmp(ipHostCave,oidArduinoCaveHum)
  resultSetH = setSnmp(ipHostSnmp,oidDht22CaveHum,int(humCave))

