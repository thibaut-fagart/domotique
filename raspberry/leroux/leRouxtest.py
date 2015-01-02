#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from readDHT import SenseurDHT
from fuelSet import Fuel
from teleinfoEJP import Edf as Edf
from teleinfoEJP import teleinfoEJP as teleinfoEJP

RaspberryPath = "/home/prog/raspberry"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ipHostSnmp            = "192.168.0.199"

if __name__ == "__main__":
  #Prise1   = [ 27, 22, 10,  9, 11]
  #Prise2   = [ 24, 25,  8,  7]
  #Prise3   = [ 23]
  #Prise4   = [ 14, 15, 18]
  #White    = [  4, 17]

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
    GPIO.setup(senseur.pin, GPIO.IN)
    senseur.getDhtValues()
    dic[senseur.label] = senseur
    # print "Humidity    : ",senseur.label, dic[senseur.label].toSnmpSetHum()
    # print "Temperature : ",senseur.label, dic[senseur.label].toSnmpSetTemp()

  fuel = Fuel()
  fuel.readFuelData()

  edf=teleinfoEJP()

  snmpValuesToSet = []
  
  for senseur in allSenseurs:
    if senseur.isValid():
       snmpValuesToSet.append(senseur.toSnmpSetHum())
       snmpValuesToSet.append(senseur.toSnmpSetTemp())

  snmpValuesToSet.append(fuel.toSnmpBurningTime())
  snmpValuesToSet.append(fuel.toSnmpFuelBurnt())
  snmpValuesToSet.append(fuel.toSnmpFuelRemaining())

  for teleinfoLabel in allTeleinfoLabel:
    if teleinfoLabel.isValid():
      snmpValuesToSet.append(teleinfoLabel.toSnmpSet())
  
  # print ("snmpValuesToSet %s" %(snmpValuesToSet) )

  cmdGen = cmdgen.CommandGenerator()
  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget((ipHostSnmp, 161)),
    *snmpValuesToSet
    #dic['Ext'].toSnmpSetHum(),
    #dic['Ext'].toSnmpSetTemp(),
    #dic['Cuisine'].toSnmpSetHum(),
    #dic['Cuisine'].toSnmpSetTemp(),
    #dic['ThermoOld'].toSnmpSetHum(),
    #dic['ThermoOld'].toSnmpSetTemp(),
    #dic['ThermoNew'].toSnmpSetHum(),
    #dic['ThermoNew'].toSnmpSetTemp(),
    #dic['SdbNew'].toSnmpSetHum(),
    #dic['SdbNew'].toSnmpSetTemp(),
    #dic['Rasp'].toSnmpSetHum(),
    #dic['Rasp'].toSnmpSetTemp(),
    #fuel.toSnmpBurningTime(),
    #fuel.toSnmpFuelBurnt(),
    #fuel.toSnmpFuelRemaining(),
    #edf.etiquettes['EJPHN'].toSnmp(),
    #edf.etiquettes['EJPHPM'].toSnmp(),
    #edf.etiquettes['IINST1'].toSnmp(),
    #edf.etiquettes['IINST2'].toSnmp(),
    #edf.etiquettes['IINST3'].toSnmp(),
    #edf.etiquettes['ISOUSC'].toSnmp(),
    #edf.etiquettes['PAPP'].toSnmp(),
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

