#!/usr/bin/python 
from IOPi import IOPI
import time,sys
from getsnmp import getSnmp

ipHostSnmp      = "192.168.0.110"
oidAmpliSalonState   = "1.3.6.1.4.1.43689.1.1.1.0"
oidAmpliSdbState     = "1.3.6.1.4.1.43689.1.1.2.0"
oidAmpliCuisineState = "1.3.6.1.4.1.43689.1.1.3.0"
oidAmpliChambreState = "1.3.6.1.4.1.43689.1.1.4.0"

pinCuisine = 1
pinChambre = 3
pinVentilo = 6
pinSdb     = 7
pinVMC     = 8

pinxx1     = 2
pinxx2     = 4
pinxx3     = 5

valVMC = 1

def main():
  bus1 = IOPI(0x20)
  bus2 = IOPI(0x21)

  bus1.setPortDirection(0, 0x00)
  bus1.setPortDirection(1, 0x00)
  bus2.setPortDirection(0, 0x00)
  bus2.setPortDirection(1, 0x00)

  bus1.writePin(2, 0)
  bus1.writePin(4, 0)
  bus1.writePin(8, 0)

  while(True):
    nameSalon,   valSalon   = getSnmp(ipHostSnmp,oidAmpliSalonState)
    nameCuisine, valCuisine = getSnmp(ipHostSnmp,oidAmpliCuisineState)
    nameSdb,     valSdb     = getSnmp(ipHostSnmp,oidAmpliSdbState)
    nameChambre, valChambre = getSnmp(ipHostSnmp,oidAmpliChambreState)
    #nameVMC,     valVMC     = getSnmp(ipHostSnmp,oidVMCState)
    #nameVentilo, valVentilo = getSnmp(ipHostSnmp,oidVentiloState)

    bus1.writePin(pinCuisine, int(valCuisine))
    bus1.writePin(pinChambre, int(valChambre))
    bus1.writePin(pinSdb, int(valChambre))
    #bus1.writePin(pinSdb, int(valSdb))
    bus1.writePin(pinVMC, int(valVMC)
    #bus1.writePin(2, int(valVentilo)
  
    time.sleep(5)

if __name__ == "__main__":
  time.sleep(3)
  main()
