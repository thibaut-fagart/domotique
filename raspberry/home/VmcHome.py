#!/usr/bin/python 
import time,sys
import RPi.GPIO as GPIO
from getsnmp import getSnmp

VentiloSdbPin     = 23
VentiloCouloirPin = 24
FreqPWM = 25        

GPIO.setmode(GPIO.BCM)
GPIO.setup(VentiloSdbPin, GPIO.OUT)
GPIO.setup(VentiloCouloirPin, GPIO.OUT)

VentiloSdbPWM = GPIO.PWM(VentiloSdbPin, FreqPWM)  
VentiloCouloirPWM = GPIO.PWM(VentiloCouloirPin, FreqPWM)  

VentiloSdbPWM.start(50)
VentiloCouloirPWM.start(50)

ValPWM = 0

try:
  while 1: 
    ValPWM = ValPWM + 5
    VentiloSdbPWM.ChangeDutyCycle(ValPWM)
    VentiloCouloirPWM.ChangeDutyCycle(ValPWM)
    print 'PWM speed : %i'%ValPWM
    if ValPWM > 95:
      ValPWM = 0
    time.sleep(5)
except KeyboardInterrupt:
    pass

VentiloSdbPWM.stop()
VentiloCouloirPWM.stop()
GPIO.cleanup()


ipHostSnmp      = "192.168.0.110"
oidAmpliSalonState   = "1.3.6.1.4.1.43689.1.1.1.0"
oidAmpliSdbState     = "1.3.6.1.4.1.43689.1.1.2.0"
oidAmpliCuisineState = "1.3.6.1.4.1.43689.1.1.3.0"
oidAmpliChambreState = "1.3.6.1.4.1.43689.1.1.4.0"

def main():
  while(True):
    #nameSalon,   valSalon   = getSnmp(ipHostSnmp,oidAmpliSalonState)
    #nameCuisine, valCuisine = getSnmp(ipHostSnmp,oidAmpliCuisineState)
    #nameSdb,     valSdb     = getSnmp(ipHostSnmp,oidAmpliSdbState)
    #nameChambre, valChambre = getSnmp(ipHostSnmp,oidAmpliChambreState)
    #nameVMC,     valVMC     = getSnmp(ipHostSnmp,oidVMCState)
    #nameVentilo, valVentilo = getSnmp(ipHostSnmp,oidVentiloState)

    time.sleep(5)

if __name__ == "__main__":
  time.sleep(3)
  main()
