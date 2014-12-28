#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from readDHT import SenseurDHT
from teleinfoEJP import Edf as Edf
from teleinfoEJP import teleinfoEJP as teleinfoEJP

RaspberryPath = "/home/prog/raspberry"
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

ipHostSnmp            = "192.168.0.199"

class Fuel :
  def __init__(self):
    self.oidFuelBurningTime  = "1.3.6.1.4.1.43689.1.5.1.0"
    self.oidFuelBurnt        = "1.3.6.1.4.1.43689.1.5.2.0"
    self.oidFuelRemaining    = "1.3.6.1.4.1.43689.1.5.3.0"
  
  def readFuelData(self):
    fuelFileData = RaspberryPath + "/leroux/fuelFileData.log"
    with open(fuelFileData, 'r') as fileReadWrite:
      fuelData = fileReadWrite.read().split()
    self.burningTime = float(fuelData[0])
    self.fuelBurnt = float(fuelData[1])
    self.fuelRemaining = float(fuelData[2])
  def toSnmpBurningTime(self):
    return (self.oidFuelBurningTime, rfc1902.Integer(self.burningTime))
  def toSnmpFuelBurnt(self):
    return (self.oidFuelBurnt, rfc1902.Integer(self.fuelBurnt))
  def toSnmpFuelRemaining(self):
    return (self.oidFuelRemaining, rfc1902.Integer(self.fuelRemaining))

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

  fuel = Fuel()
  fuel.readFuelData()
  edf=teleinfoEJP()
  edfFilePath = RaspberryPath + "/leroux/edf.log"
  edf.saveStats(edfFilePath)

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
    fuel.toSnmpBurningTime(),
    fuel.toSnmpFuelBurnt(),
    fuel.toSnmpFuelRemaining(),
    edf.etiquettes['EJPHN'].toSnmp(),
    edf.etiquettes['EJPHPM'].toSnmp(),
    edf.etiquettes['IINST1'].toSnmp(),
    edf.etiquettes['IINST2'].toSnmp(),
    edf.etiquettes['IINST3'].toSnmp(),
    edf.etiquettes['ISOUSC'].toSnmp(),
    edf.etiquettes['PAPP'].toSnmp(),
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

