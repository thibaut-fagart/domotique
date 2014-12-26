#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
import Raspberry_Pi_Driver as driver
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from readDHT import readDHT
import serial
from teleinfoEJP import Edf

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

class Edf :
    oidEdfAdco    = "1.3.6.1.4.1.43689.1.4.1.0"
    oidEdfOptarif = "1.3.6.1.4.1.43689.1.4.2.0"
    oidEdfIsousc  = "1.3.6.1.4.1.43689.1.4.3.0"
    oidEdfEjphn   = "1.3.6.1.4.1.43689.1.4.9.0"
    oidEdfEjphpm  = "1.3.6.1.4.1.43689.1.4.10.0"
    oidEdfPtec    = "1.3.6.1.4.1.43689.1.4.5.0"
    oidEdfIinst1  = "1.3.6.1.4.1.43689.1.4.11.0"
    oidEdfIinst2  = "1.3.6.1.4.1.43689.1.4.12.0"
    oidEdfIinst3  = "1.3.6.1.4.1.43689.1.4.13.0"
    oidEdfImax1   = "1.3.6.1.4.1.43689.1.4.14.0"
    oidEdfImax2   = "1.3.6.1.4.1.43689.1.4.15.0"
    oidEdfImax3   = "1.3.6.1.4.1.43689.1.4.16.0"
    oidEdfPmax    = "1.3.6.1.4.1.43689.1.4.17.0"
    oidEdfPapp    = "1.3.6.1.4.1.43689.1.4.8.0"

    def readTeleinfo(self):
      ser.flushInput()
      tramesOk = LireTeleinfo()
      ser.close()
      #print tramesOk
      for etiquette in tramesOk:
          #if etiquette ==  'ADCO':
                      #result = setSnmp(ipHostSnmp,oidEdfAdco,int(tramesOk[etiquette]))
          #if etiquette ==  'OPTARIF':
                      #result = setSnmp(ipHostSnmp,oidEdfOptarif,int(tramesOk[etiquette]))
          if etiquette ==  'ISOUSC':
              self.ISOUSC = tramesOk[etiquette]
                      #print 'ISOUSC ',tramesOk[etiquette]
          if etiquette ==  'EJPHN':
              self.EJPHN = tramesOk[etiquette]
                      #print 'EJPHN ',tramesOk[etiquette]
          if etiquette ==  'EJPHPM':
              self.EJPHPM = tramesOk[etiquette]
                      #print 'EJPHPM ',tramesOk[etiquette]
          #if etiquette ==  'PTEC':
                  #result = setSnmp(ipHostSnmp,oidEdfPtec,int(tramesOk[etiquette]))
          if etiquette == 'IINST1':
              self.IINST1 = tramesOk[etiquette]
                  #print 'IINST1 ',tramesOk[etiquette]
          if etiquette == 'IINST2':
              self.IINST2=tramesOk[etiquette]
                  #print 'IINST2 ',tramesOk[etiquette]
          if etiquette == 'IINST3':
              self.IINST3 = tramesOk[etiquette]
                  #print 'IINST3 ',tramesOk[etiquette]
          #if etiquette ==  'IMAX1':
                  #result = setSnmp(ipHostSnmp,oidEdfImax1,int(tramesOk[etiquette]))
          #if etiquette ==  'IMAX2':
                  #result = setSnmp(ipHostSnmp,oidEdfImax2,int(tramesOk[etiquette]))
          #if etiquette ==  'IMAX3':
                  #result = setSnmp(ipHostSnmp,oidEdfImax3,int(tramesOk[etiquette]))
          #if etiquette ==  'PMAX':
                  #result = setSnmp(ipHostSnmp,oidEdfPmax,int(tramesOk[etiquette]))
          if etiquette ==  'PAPP':
              self.PAPP = tramesOk[etiquette]
                      #print 'PAPP ',tramesOk[etiquette]
    def toSnmpIsousc(self):
        return (self.oidEdfIsousc, int(self.ISOUSC))
    def toSnmpEjpHpm(self):
        return (self.oidEdfEjphpm, int(self.EJPHPM))
    def toSnmpEjpHn(self):
        return (self.oidEdfEjphn, int(self.EJPHN))
    def toSnmpIInst1(self):
        return (self.oidEdfIinst1, int(self.IINST1))
    def toSnmpIInst2(self):
        return (self.oidEdfIinst2, int(self.IINST2))
    def toSnmpIInst3(self):
        return (self.oidEdfIinst3, int(self.IINST3))
    def toSnmpPApp(self):
        return (self.oidEdfPapp, int(self.PAPP))


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

class Fuel :
  oidFuelBurningTime  = "1.3.6.1.4.1.43689.1.5.1.0"
  oidFuelBurnt        = "1.3.6.1.4.1.43689.1.5.2.0"
  oidFuelRemaining    = "1.3.6.1.4.1.43689.1.5.3.0"
  def readFuelData(self):
    fuelFileData = RaspberryPath + "/leroux/fuelFileData.log"
    fileReadWrite = open(fuelFileData, 'r')
    fuelData = fileReadWrite.read().split()
    self.burningTime = float(fuelData[0])
    self.fuelBurnt = float(fuelData[1])
    self.fuelRemaining = float(fuelData[2])
    fileReadWrite.close()
  def toSnmpBurningTime(self):
    return (self.oidFuelBurningTime, int(self.burningTime))
  def toSnmpFuelBurnt(self):
    return (self.oidFuelBurnt, int(self.oidFuelBurnt))
  def toSnmpFuelRemaining(self):
    return (self.oidFuelRemaining, int(self.oidFuelRemaining))

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
  edf = Edf()
  edf.readTeleinfo()
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
    edf.toSnmpEjpHn(),
    edf.toSnmpEjpHpm(),
    edf.toSnmpIInst1(),
    edf.toSnmpIInst2(),
    edf.toSnmpIInst3(),
    edf.toSnmpIsousc(),
    edf.toSnmpPApp()
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

