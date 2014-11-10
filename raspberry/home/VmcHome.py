#!/usr/bin/python 
import time,sys
from getsnmp import getSnmp
from setsnmp import setSnmp

ipHostSnmp           = "192.168.0.110"
oidVmcPowerState     = "1.3.6.1.4.1.43689.1.6.1.0"
oidVentiloPowerState = "1.3.6.1.4.1.43689.1.6.2.0"
oidDht22ExtTemp      = "1.3.6.1.4.1.43689.1.2.1.1.0"
oidDht22ExtHum       = "1.3.6.1.4.1.43689.1.2.1.2.0"
oidDht22SalonHum     = "1.3.6.1.4.1.43689.1.2.4.2.0"
oidDht22SdbHum       = "1.3.6.1.4.1.43689.1.2.3.2.0"


def logic_VMC():
  tempExtEte = 180

  nameTempExt,  valTempExt  = getSnmp(ipHostSnmp,oidDht22ExtTemp)
  nameHumExt,   valHumExt   = getSnmp(ipHostSnmp,oidDht22ExtHum)
  nameHumSalon, valHumSalon = getSnmp(ipHostSnmp,oidDht22SalonHum)
  nameHumSdb,   valHumSdb   = getSnmp(ipHostSnmp,oidDht22SdbHum)

  valTempExt = int(valTempExt)
  valHumExt = int(valHumExt)
  valHumSalon = int(valHumSalon)
  valHumSdb = int(valHumSdb)

  valHumMed = max(valHumSalon,valHumExt)

  if (valTempExt > tempExtEte + 5.):
    setSnmp(ipHostSnmp,oidVmcPowerState,1)
    setSnmp(ipHostSnmp,oidVentiloPowerState,0)
  else:
    if (valHumSdb > valHumMed + 200.):
      setSnmp(ipHostSnmp,oidVmcPowerState,1)
      setSnmp(ipHostSnmp,oidVentiloPowerState,0)
    if ((valHumSdb < valHumMed + 100.) and (valTempExt < tempExtEte - 5.)):
      setSnmp(ipHostSnmp,oidVmcPowerState,0)
      setSnmp(ipHostSnmp,oidVentiloPowerState,1)

if __name__ == "__main__":
  logic_VMC()
