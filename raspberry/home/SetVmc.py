#!/usr/bin/python 
import time,sys
from setsnmp import setSnmp
from getsnmp import getSnmp

ipHostSnmp           = "192.168.0.110"
oidForceVmc          = "1.3.6.1.4.1.43689.1.6.5.0"

if __name__ == "__main__":
  nameForceVMC,  valForceVMC  = getSnmp(ipHostSnmp,oidForceVmc)
  if int(valForceVMC):
    setSnmp(ipHostSnmp,oidForceVmc,0)
    print 'VMC is On and will be set to automatic mode'
  else:
    setSnmp(ipHostSnmp,oidForceVmc,1)
    print 'VMC is in automatic mode and will be forced to On'

