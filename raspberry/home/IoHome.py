#!/usr/bin/python 
from IOPi import IOPI
import time,sys
from getsnmp import getSnmp
from setsnmp import setSnmp

ipHostSnmp      = "192.168.0.110"
ipHostSnmpAudio = "192.168.0.103"
oidAmpliSalonState   = "1.3.6.1.4.1.43689.1.1.1.0"
oidAmpliSdbState     = "1.3.6.1.4.1.43689.1.1.2.0"
oidAmpliCuisineState = "1.3.6.1.4.1.43689.1.1.3.0"
oidAmpliChambreState = "1.3.6.1.4.1.43689.1.1.4.0"
oidVmcPowerState     = "1.3.6.1.4.1.43689.1.6.1.0"
oidVentiloPowerState = "1.3.6.1.4.1.43689.1.6.2.0"
oidThermoState       = "1.3.6.1.4.1.43689.1.6.3.0"
oidLogicalSpare1     = "1.3.6.1.4.1.43689.1.6.4.0"

pinCuisine = 1
pinChambre = 3
pinVentilo = 6
pinSdb     = 7
pinVMC     = 8

pinThermo  = 2

pinxx2     = 4
pinxx3     = 5

valVMC = 1

bus1 = IOPI(0x20)
bus2 = IOPI(0x21)

bus1.setPortDirection(0, 0x00)
bus1.setPortDirection(1, 0x00)
bus2.setPortDirection(0, 0x00)
bus2.setPortDirection(1, 0x00)


def main():

  setSnmp(ipHostSnmp,oidLogicalSpare1,1)
  nameLogic,  valLogic  = getSnmp(ipHostSnmp,oidLogicalSpare1)

  while(int(valLogic)):
    nameLogic,  valLogic  = getSnmp(ipHostSnmp,oidLogicalSpare1)
    
    try:
      nameSalon,   valSalon   = getSnmp(ipHostSnmpAudio,oidAmpliSalonState)
      nameCuisine, valCuisine = getSnmp(ipHostSnmpAudio,oidAmpliCuisineState)
      nameSdb,     valSdb     = getSnmp(ipHostSnmpAudio,oidAmpliSdbState)
      nameChambre, valChambre = getSnmp(ipHostSnmpAudio,oidAmpliChambreState)
      nameVMC,     valVMC     = getSnmp(ipHostSnmp,oidVmcPowerState)
      nameVentilo, valVentilo = getSnmp(ipHostSnmp,oidVentiloPowerState)
      nameThermo,  valThermo  = getSnmp(ipHostSnmp,oidThermoState)
    except:
      print 'getSnmp Fail'

    bus1.writePin(pinCuisine, int(valCuisine))
    time.sleep(0.5)
    bus1.writePin(pinChambre, int(valChambre))
    time.sleep(0.5)
    bus1.writePin(pinSdb, int(valChambre))
    ##bus1.writePin(pinSdb, int(valSdb))
    bus1.writePin(pinVMC, int(valVMC))
    time.sleep(0.5)
    bus1.writePin(pinVentilo, int(valVentilo))
    time.sleep(0.5)
    bus1.writePin(pinThermo, int(valThermo))

if __name__ == "__main__":
  time.sleep(60)
  nameLogic,  valLogic  = getSnmp(ipHostSnmp,oidLogicalSpare1)
  if not int(valLogic):
    main()
