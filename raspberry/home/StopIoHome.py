#!/usr/bin/python 
import time,sys
from setsnmp import setSnmp

ipHostSnmp           = "192.168.0.110"
oidLogicalSpare1     = "1.3.6.1.4.1.43689.1.6.4.0"

if __name__ == "__main__":
  setSnmp(ipHostSnmp,oidLogicalSpare1,0)

