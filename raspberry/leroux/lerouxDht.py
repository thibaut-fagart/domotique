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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in gpioBCMPrise1:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise2:
  GPIO.setup(pin, GPIO.IN)
for pin in gpioBCMPrise3:
  GPIO.setup(pin, GPIO.IN)

oidDht22RaspTemp      = "1.3.6.1.4.1.43689.1.2.13.1.0"
ipHostSnmp            = "192.168.0.199"


class SenseurDHT :
  def __init__(self, aLabel, anOidTemp, andOidHum, aPinBCM):
    self.label =  aLabel
    self.oidTemp = anOidTemp
    self.oidHum = andOidHum
    self.pin = aPinBCM
  def getDhtValues(self):
    self.valHum , self.valTemp = readDHT(self.pin)
  def toSnmpSetTemp(self):
    return (self.oidTemp, rfc1902.Integer(self.valTemp*10))
  def toSnmpSetHum(self):
    return (self.oidHum, rfc1902.Integer(self.valHum*10))


if __name__ == "__main__":
  allSenseurs = [
    SenseurDHT('Ext', "1.3.6.1.4.1.43689.1.2.1.1.0", "1.3.6.1.4.1.43689.1.2.1.2.0", 23),
    SenseurDHT('Cuisine', "1.3.6.1.4.1.43689.1.2.2.1.0", "1.3.6.1.4.1.43689.1.2.2.2.0", 8),
    SenseurDHT('ThermoOld', "1.3.6.1.4.1.43689.1.2.9.1.0", "1.3.6.1.4.1.43689.1.2.9.2.0", 9),
    SenseurDHT('ThermoNew', "1.3.6.1.4.1.43689.1.2.10.1.0", "1.3.6.1.4.1.43689.1.2.10.2.0", 10),
    SenseurDHT('SdbNew', "1.3.6.1.4.1.43689.1.2.12.1.0", "1.3.6.1.4.1.43689.1.2.12.2.0", 11),
    SenseurDHT('Rasp', "1.3.6.1.4.1.43689.1.2.13.1.0", "1.3.6.1.4.1.43689.1.2.13.2.0", 25),
    # SenseurDHT('SdbOld', "1.3.6.1.4.1.43689.1.2.11.1.0", "1.3.6.1.4.1.43689.1.2.11.2.0", pinSdbOld),
  ]
  dic = {} 
  for senseur in allSenseurs :
    senseur.getDhtValues()
    dic[senseur.label] = senseur
    # print(" %s , hum %s , temp: %s " % (senseur.label, senseur.valHum,senseur.valTemp))

  cmdGen = cmdgen.CommandGenerator()

  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget((ipHostSnmp, 161)),
    dic['Ext'].toSnmpSetHum(),
    dic['Ext'].toSnmpSetTemp(),
    dic['Cuisine'].toSnmpSetHum(),
    dic['Cuisine'].toSnmpSetTemp(),
    dic['ThermoOld'].toSnmpSetHum(),
    dic['ThermoOld'].toSnmpSetTemp(),
    dic['ThermoNew'].toSnmpSetHum(),
    dic['ThermoNew'].toSnmpSetTemp(),
    dic['SdbNew'].toSnmpSetHum(),
    dic['SdbNew'].toSnmpSetTemp(),
    dic['Rasp'].toSnmpSetHum(),
    dic['Rasp'].toSnmpSetTemp(),
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

