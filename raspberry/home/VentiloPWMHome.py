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



def main():
  time.sleep(5)

if __name__ == "__main__":
  time.sleep(3)
  main()
