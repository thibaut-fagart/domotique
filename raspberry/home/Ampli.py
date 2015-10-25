#!/usr/bin/python 
from IOPi import IOPI
import time,sys

ipHostSnmp      = "192.168.0.110"
ipHostSnmpAudio = "192.168.0.103"
oidAmpliSalonState   = "1.3.6.1.4.1.43689.1.1.1.0"
oidAmpliSdbState     = "1.3.6.1.4.1.43689.1.1.2.0"
oidAmpliCuisineState = "1.3.6.1.4.1.43689.1.1.3.0"
oidAmpliChambreState = "1.3.6.1.4.1.43689.1.1.4.0"

pinCuisine = 1
pinChambre = 3
pinSdb     = 7

bus1 = IOPI(0x20)
bus2 = IOPI(0x21)

#bus1.setPortDirection(0, 0x00)
#bus1.setPortDirection(1, 0x00)
#bus2.setPortDirection(0, 0x00)
#bus2.setPortDirection(1, 0x00)


def AmpliOn():
    bus1.writePin(pinCuisine, 1)
    time.sleep(1)
    bus1.writePin(pinChambre, 1)
    time.sleep(1)
    bus1.writePin(pinSdb, 1)

def AmpliOff():
    bus1.writePin(pinCuisine, 0)
    time.sleep(1)
    bus1.writePin(pinChambre, 0)
    time.sleep(1)
    bus1.writePin(pinSdb, 0)

if __name__ == "__main__":
  if (bus1.readPin(pinCuisine) or bus1.readPin(pinCuisine) or bus1.readPin(pinCuisine)):
    AmpliOff()
    print "Ampli set to Off"
  else:
    AmpliOn()
    print "Ampli set to On"
   
  time.sleep(0.5)
