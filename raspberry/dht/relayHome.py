#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from setsnmp import setSnmp
from getsnmp import getSnmp

oidArduinoPcTemp  = "1.3.6.1.4.1.36582.3"
oidArduinoPcHum   = "1.3.6.1.4.1.36582.4"
oidDht22PcTemp    = "1.3.6.1.4.1.43689.1.1.2.5.1.0"
oidDht22PcHum     = "1.3.6.1.4.1.43689.1.1.2.5.2.0"
oidArduinoSdbTemp = "1.3.6.1.4.1.36582.5"
oidArduinoSdbHum  = "1.3.6.1.4.1.36582.6"
oidDht22SdbTemp   = "1.3.6.1.4.1.43689.1.1.2.3.1.0"
oidDht22SdbHum    = "1.3.6.1.4.1.43689.1.1.2.3.2.0"
oidArduinoExtTemp = "1.3.6.1.4.1.36582.7"
oidArduinoExtHum  = "1.3.6.1.4.1.36582.8"
oidDht22ExtTemp   = "1.3.6.1.4.1.43689.1.1.2.1.1.0"
oidDht22ExtHum    = "1.3.6.1.4.1.43689.1.1.2.1.2.0"
ipHostHome        = "192.168.0.70"
ipHostSnmp        = "192.168.0.110"

if __name__ == "__main__":

  oidPcTemp, tempPc = getSnmp(ipHostHome,oidArduinoPcTemp)
  resultSetT = setSnmp(ipHostSnmp,oidDht22PcTemp,int(tempPc))

  oidPcHum, humPc = getSnmp(ipHostHome,oidArduinoPcHum)
  resultSetH = setSnmp(ipHostSnmp,oidDht22PcHum,int(humPc))

  oidSdbTemp, tempSdb = getSnmp(ipHostHome,oidArduinoSdbTemp)
  resultSetT = setSnmp(ipHostSnmp,oidDht22SdbTemp,int(tempSdb))

  oidSdbHum, humSdb = getSnmp(ipHostHome,oidArduinoSdbHum)
  resultSetH = setSnmp(ipHostSnmp,oidDht22SdbHum,int(humSdb))

  oidExtTemp, tempExt = getSnmp(ipHostHome,oidArduinoExtTemp)
  resultSetT = setSnmp(ipHostSnmp,oidDht22ExtTemp,int(tempExt))

  oidExtHum, humExt = getSnmp(ipHostHome,oidArduinoExtHum)
  resultSetH = setSnmp(ipHostSnmp,oidDht22ExtHum,int(humExt))

