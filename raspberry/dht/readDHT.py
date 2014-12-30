#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import Raspberry_Pi_Driver as driver
from pysnmp.proto import rfc1902

RaspberryPath = "/home/prog/raspberry"

# Define error constants.
DHT_SUCCESS        =  0
DHT_ERROR_TIMEOUT  = -1
DHT_ERROR_CHECKSUM = -2
DHT_ERROR_ARGUMENT = -3
DHT_ERROR_GPIO     = -4
TRANSIENT_ERRORS = [DHT_ERROR_CHECKSUM, DHT_ERROR_TIMEOUT]


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
  def getDhtPin(self):
    return self.pin
  def getDhtValues(self):
    self.hum , self.temp = readDHT(self.pin)
  def toSnmpSetTemp(self):
    return (self.oidTemp, rfc1902.Integer(self.temp*10))
  def toSnmpSetHum(self):
    return (self.oidHum, rfc1902.Integer(self.hum*10))

