#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import Raspberry_Pi_Driver as driver
import RPi.GPIO as GPIO
from pysnmp.proto import rfc1902

RaspberryPath = "/home/prog/raspberry"

# Define error constants.
DHT_SUCCESS        =  0
DHT_ERROR_TIMEOUT  = -1
DHT_ERROR_CHECKSUM = -2
DHT_ERROR_ARGUMENT = -3
DHT_ERROR_GPIO     = -4
TRANSIENT_ERRORS = [DHT_ERROR_CHECKSUM, DHT_ERROR_TIMEOUT]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def printlog(datelog, text):
    fileToBeWriten = RaspberryPath + "/dht/LogReadDht.log"
    fichierWrite = open(fileToBeWriten, 'a')
    fichierWrite.write(datelog)
    fichierWrite.write(text)
    fichierWrite.write('\n')
    fichierWrite.close()


def readDHT_once(pin, sensor=22):
    # Validate pin is a valid GPIO.
    if pin is None or int(pin) < 0 or int(pin) > 31:
        raise ValueError('Pin must be a valid GPIO number 0 to 31.')
    # Get a reading from C driver code.
    result, humidity, temp = driver.read(sensor, int(pin))
    if result in TRANSIENT_ERRORS:
        # Signal no result could be obtained, but the caller can retry.
        return (None, None)
    elif result == DHT_ERROR_GPIO:
        raise RuntimeError('Error accessing GPIO. Make sure program is run as root with sudo!')
    elif result != DHT_SUCCESS:
        # Some kind of error occured.
        raise RuntimeError('Error calling DHT test driver read: {0}'.format(result))
    return (humidity, temp)

def readDHT(pin, sensor=22, retries=15, delay_seconds=2):
    for i in range(retries):
        humidity, temperature = readDHT_once(pin)
        if humidity is not None and temperature is not None:
            return (humidity, temperature)
        time.sleep(delay_seconds)
    return (None, None)

class SenseurDHT :
  def __init__(self, aLabel, anOidTemp, andOidHum, aPinBCM):
    self.label =  aLabel
    self.oidTemp = anOidTemp
    self.oidHum = andOidHum
    self.pin = aPinBCM
  def getDhtValues(self):
    self.hum , self.temp = readDHT(self.pin)
  def toSnmpSetTemp(self):
    return (self.oidTemp, rfc1902.Integer(self.temp*10))
  def toSnmpSetHum(self):
    return (self.oidHum, rfc1902.Integer(self.hum*10))
  def isValid(self):
    if (None == self.temp or None == self.hum):
      return False
      printlog(time.asctime(),'read DHT %s error With temp : %s and Hum : %s'%(self.label,self.temp,self.hum))
    else:
      return True

class DhtDef:
  def __init__(self):
    #Prise1   = [ 27, 22, 10,  9, 11]
    #Prise2   = [ 24, 25,  8,  7]
    #Prise3   = [ 23]
    #Prise4   = [ 14, 15, 18]
    #White    = [  4, 17]

    senseurList = [
      SenseurDHT('Ext', "1.3.6.1.4.1.43689.1.2.1.1.0", "1.3.6.1.4.1.43689.1.2.1.2.0", 23),
      SenseurDHT('Cuisine', "1.3.6.1.4.1.43689.1.2.2.1.0", "1.3.6.1.4.1.43689.1.2.2.2.0", 8),
      SenseurDHT('ThermoOld', "1.3.6.1.4.1.43689.1.2.9.1.0", "1.3.6.1.4.1.43689.1.2.9.2.0", 9),
      SenseurDHT('ThermoNew', "1.3.6.1.4.1.43689.1.2.10.1.0", "1.3.6.1.4.1.43689.1.2.10.2.0", 10),
      SenseurDHT('SdbNew', "1.3.6.1.4.1.43689.1.2.12.1.0", "1.3.6.1.4.1.43689.1.2.12.2.0", 11),
      SenseurDHT('Rasp', "1.3.6.1.4.1.43689.1.2.13.1.0", "1.3.6.1.4.1.43689.1.2.13.2.0", 25),
      # SenseurDHT('SdbOld', "1.3.6.1.4.1.43689.1.2.11.1.0", "1.3.6.1.4.1.43689.1.2.11.2.0", pinSdbOld),
    ]

    self.allSenseurs = {}

    for senseur in senseurList :
      GPIO.setup(senseur.pin, GPIO.IN)
      senseur.getDhtValues()
      self.allSenseurs[senseur.label] = senseur
      # print "Humidity    : ",senseur.label, dic[senseur.label].toSnmpSetHum()
      # print "Temperature : ",senseur.label, dic[senseur.label].toSnmpSetTemp()

def Dht():
  allSenseurs = DhtDef()
  return allSenseurs

if __name__ == "__main__":
    while 1==1:
        # pins = [4,9,11,17,27]
        pins = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
        for i in pins :
            result = driver.read(22,i)
            if 0 == result[0]:
                print("%d (%d,%d,%d)"%((i,)+result))
            time.sleep(1)
