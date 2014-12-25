#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
import Raspberry_Pi_Driver as driver
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from readDHT import readDHT

gpioBCMPrise1   = [ 27, 22, 10,  9, 11]
gpioBCMPrise2   = [ 24, 25,  8,  7]
gpioBCMPrise3   = [ 23]
#gpioBCMPrise4   = [ 14, 15, 18]
#gpioListBCMWhite    = [  4, 17]

pinExt       = [gpioBCMPrise3[0], gpioTagPrise3[0]]
pinThermoOld = [gpioBCMPrise1[3], gpioTagPrise1[3]]
pinThermoNew = [gpioBCMPrise1[2], gpioTagPrise1[2]]
pinSdbNew    = [gpioBCMPrise1[4], gpioTagPrise1[4]]
pinCuisine   = [gpioBCMPrise2[2], gpioTagPrise2[2]]
pinRasp      = [gpioBCMPrise2[1], gpioTagPrise2[1]]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise1:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise3:
  GPIO.setup(pin, GPIO.IN)

#oidDht22ExtTemp       = "1.3.6.1.4.1.43689.1.2.1.1.0"
oidDht22ExtTemp       = "1.3.6.1.4.1.43689.1.2.4.1.0"
#oidDht22ExtHum        = "1.3.6.1.4.1.43689.1.2.1.2.0"
oidDht22ExtHum        = "1.3.6.1.4.1.43689.1.2.4.2.0"
oidDht22CuisineTemp   = "1.3.6.1.4.1.43689.1.2.2.1.0"
oidDht22CuisineHum    = "1.3.6.1.4.1.43689.1.2.2.2.0"
oidDht22ThermoOldTemp = "1.3.6.1.4.1.43689.1.2.9.1.0"
oidDht22ThermoOldHum  = "1.3.6.1.4.1.43689.1.2.9.2.0"
oidDht22ThermoNewTemp = "1.3.6.1.4.1.43689.1.2.10.1.0"
oidDht22ThermoNewHum  = "1.3.6.1.4.1.43689.1.2.10.2.0"
oidDht22SdbOldTemp    = "1.3.6.1.4.1.43689.1.2.11.1.0"
oidDht22SdbOldHum     = "1.3.6.1.4.1.43689.1.2.11.2.0"
oidDht22SdbNewTemp    = "1.3.6.1.4.1.43689.1.2.12.1.0"
oidDht22SdbNewHum     = "1.3.6.1.4.1.43689.1.2.12.2.0"
oidDht22RaspTemp      = "1.3.6.1.4.1.43689.1.2.13.1.0"
oidDht22RaspHum       = "1.3.6.1.4.1.43689.1.2.13.2.0"
ipHostSnmp            = "192.168.0.199"


class SenseurDHT :
  def __init__(self, aLabel, anOidTemp, andOidHum, aPinBCM):
    self.label =  aLabel
    self.oidTemp = anOidTemp
    self.oidHum = andOidHum
    self.pin = aPinBCM
  def fetchValues(self):
    self.valHum , self.valTemp = readDHT(self.pin)
  def toSnmpSetTemp(self):
    return (self.oidTemp, rfc1902.Integer(self.valTemp*10))
  def toSnmpSetHum(self):
    return (self.oidHum, rfc1902.Integer(self.valHum*10))


if __name__ == "__main__":
  allSenseurs = [ 
    SenseurDHT('Ext'      ,oidDht22ExtTemp    , oidDht22ExtHum    , pinExt[0]),
    SenseurDHT('Cuisine'  ,oidDht22CuisineTemp, oidDht22CuisineHum, pinCuisine[0]),
    SenseurDHT('ThermoOld',oidDht22ThermoOldTemp, oidDht22ThermoOldHum, pinThermoOld[0]),
    SenseurDHT('ThermoNew',oidDht22ThermoNewCuisineTemp, oidDht22ThermoNewCuisineHum, pinThermoNewCuisine[0]),
    SenseurDHT('SdbNew'   ,oidDht22SdbNewCuisineTemp, oidDht22SdbNewCuisineHum, pinSdbNewCuisine[0]),
    SenseurDHT('Rasp'     ,oidDht22CuisineTemp, oidDht22CuisineHum, pinCuisine[0]),
    #SenseurDHT('SdbNew'   ,oidDht22CuisineTemp, oidDht22CuisineHum, pinCuisine[0]),
  ]
  dic = {} 
  for senseur in allSenseurs :
    senseur.fetchValues()
    dic[senseur.label] = senseur
    print(" %s , hum %s , temp: %s " % (senseur.label, senseur.valHum,senseur.valTemp))

  cmdGen = cmdgen.CommandGenerator()

  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget((ipHostSnmp, 161)),
    dic['ext'].toSnmpSetHum(),
    dic['ext'].toSnmpSetTemp()
    dic['ext'].toSnmpSetHum(),
    dic['ext'].toSnmpSetTemp()
    dic['ext'].toSnmpSetHum(),
    dic['ext'].toSnmpSetTemp()
    dic['ext'].toSnmpSetHum(),
    dic['ext'].toSnmpSetTemp()
  )
  # Check for errors and print out results
  if errorIndication:
      print(errorIndication)
  else:
      if errorStatus:
          print('%s at %s' % (
              errorStatus.prettyPrint(),
              errorIndex and varBinds[int(errorIndex)-1] or '?'
               )
          )

