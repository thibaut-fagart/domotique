#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
from getsnmp import getSnmp
from setsnmp import setSnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

oidDht22Test1Temp = "1.3.6.1.4.1.43689.1.2.3.1.0"
oidDht22Test1Hum  = "1.3.6.1.4.1.43689.1.2.3.2.0"
oidDht22Test2Temp = "1.3.6.1.4.1.43689.1.2.4.1.0"
oidDht22Test2Hum  = "1.3.6.1.4.1.43689.1.2.4.2.0"
oidDht22Test3Temp = "1.3.6.1.4.1.43689.1.2.5.1.0"
oidDht22Test3Hum  = "1.3.6.1.4.1.43689.1.2.5.2.0"
oidDht22Test4Temp = "1.3.6.1.4.1.43689.1.2.6.1.0"
oidDht22Test4Hum  = "1.3.6.1.4.1.43689.1.2.6.2.0"
ipHostSnmp        = "192.168.0.199"

def mainOldGet():

    print "start of Get Snmp Values"
    nameTest1Temp,  valTemp1   = getSnmp(ipHostSnmp,oidDht22Test1Temp)
    nameTest1Hum,   valHum1    = getSnmp(ipHostSnmp,oidDht22Test1Hum)
    nameTest2Temp,  valTemp2   = getSnmp(ipHostSnmp,oidDht22Test2Temp)
    nameTest2Hum,   valHum2    = getSnmp(ipHostSnmp,oidDht22Test2Hum)
    nameTest3Temp,  valTemp3   = getSnmp(ipHostSnmp,oidDht22Test3Temp)
    nameTest3Hum,   valHum3    = getSnmp(ipHostSnmp,oidDht22Test3Hum)
    nameTest4Temp,  valTemp4   = getSnmp(ipHostSnmp,oidDht22Test4Temp)
    nameTest4Hum,   valHum4    = getSnmp(ipHostSnmp,oidDht22Test4Hum)


def mainSet():
    print "start of Set Snmp Values"
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
      cmdgen.CommunityData('private', mpModel=0),
      cmdgen.UdpTransportTarget((ipHostSnmp, 161)),
      (oidDht22Test1Temp, rfc1902.Integer(0)),
      (oidDht22Test1Hum, rfc1902.Integer(1)),
      (oidDht22Test2Temp, rfc1902.Integer(2)),
      (oidDht22Test2Hum, rfc1902.Integer(3)),
      (oidDht22Test3Temp, rfc1902.Integer(4)),
      (oidDht22Test3Hum, rfc1902.Integer(5)),
      (oidDht22Test4Temp, rfc1902.Integer(6)),
      (oidDht22Test4Hum, rfc1902.Integer(7))
    )
    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
        return False
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
                )
            )
            return False

if __name__ == "__main__":
  mainSet()
