#!/usr/bin/python 
import time,sys
from setsnmp import setSnmp

ipHostSnmp           = "192.168.0.110"
oidVmcPowerState     = "1.3.6.1.4.1.43689.1.6.1.0"
oidVentiloPowerState = "1.3.6.1.4.1.43689.1.6.2.0"

if __name__ == "__main__":
  setSnmp(ipHostSnmp,oidVmcPowerState,0)
  setSnmp(ipHostSnmp,oidVentiloPowerState,1)

