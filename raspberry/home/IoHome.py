#!/usr/bin/python 
from IOPi import IOPI
import time,sys
from getsnmp import getSnmp

ipHostSnmp      = "192.168.0.110"
oidAmpliSalonState   = "1.3.6.1.4.1.43689.1.1.1.0"
oidAmpliSdbState     = "1.3.6.1.4.1.43689.1.1.2.0"
oidAmpliCuisineState = "1.3.6.1.4.1.43689.1.1.3.0"
oidAmpliChambreState = "1.3.6.1.4.1.43689.1.1.4.0"

def main():
  bus1 = IOPI(0x20)
  bus2 = IOPI(0x21)

  bus1.setPortDirection(0, 0x00)
  bus1.setPortDirection(1, 0x00)
  bus2.setPortDirection(0, 0x00)
  bus2.setPortDirection(1, 0x00)

  bus1.writePin(2, 0)
  bus1.writePin(4, 0)
  bus1.writePin(6, 0)
  bus1.writePin(8, 0)

  while(True):
    nameSalon,   valSalon   = getSnmp(ipHostSnmp,oidAmpliSalonState)
    nameCuisine, valCuisine = getSnmp(ipHostSnmp,oidAmpliCuisineState)
    nameSdb,     valSdb     = getSnmp(ipHostSnmp,oidAmpliSdbState)
    nameChambre, valChambre = getSnmp(ipHostSnmp,oidAmpliChambreState)

    bus1.writePin(1, int(valCuisine))
    bus1.writePin(3, int(valChambre))
    bus1.writePin(5, 1)  # vmc
    bus1.writePin(7, int(valSdb))
  
    time.sleep(5)

if __name__ == "__main__":
  time.sleep(30)
  main()
