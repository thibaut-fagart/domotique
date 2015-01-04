#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from readDHT import Dht
from fuelSet import Fuel
from teleinfoGen import teleinfo as teleinfo

RaspberryPath = "/home/prog/raspberry"

ipHostSnmp            = "192.168.0.199"

if __name__ == "__main__":
  
  dht = Dht()

  fuel = Fuel()
  fuel.readFuelData()

  edf=teleinfo()

  snmpValuesToSet = []

  for senseur in dht.allSenseurs:
    if dht.allSenseurs[senseur].isValid():
       snmpValuesToSet.append(dht.allSenseurs[senseur].toSnmpSetHum())
       snmpValuesToSet.append(dht.allSenseurs[senseur].toSnmpSetTemp())

  snmpValuesToSet.append(fuel.toSnmpBurningTime())
  snmpValuesToSet.append(fuel.toSnmpFuelBurnt())
  snmpValuesToSet.append(fuel.toSnmpFuelRemaining())

  for teleinfoLabel in edf.allTeleinfoLabel:
    snmpValuesToSet.append(edf.allTeleinfoLabel[teleinfoLabel].toSnmpSet())
  
  # print ("snmpValuesToSet %s" %(snmpValuesToSet) )

  cmdGen = cmdgen.CommandGenerator()
  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget((ipHostSnmp, 161)),
    *snmpValuesToSet
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

