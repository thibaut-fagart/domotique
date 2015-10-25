#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,time
import RPi.GPIO as GPIO
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from readDHT import SenseurDHT

RaspberryPath = "/home/prog/raspberry"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ipHostSnmp  = "192.168.0.110"

def printlog(datelog,text):
  fileToBeWriten = RaspberryPath + "/home/LogHomeDht.log"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()   

if __name__ == "__main__":

  allSenseurs = [
    SenseurDHT('Ext'    , "1.3.6.1.4.1.43689.1.2.1.1.0" , "1.3.6.1.4.1.43689.1.2.1.2.0" , 27),
    SenseurDHT('Sdb'    , "1.3.6.1.4.1.43689.1.2.3.1.0" , "1.3.6.1.4.1.43689.1.2.3.2.0" ,  4),
    SenseurDHT('Salon'  , "1.3.6.1.4.1.43689.1.2.4.1.0" , "1.3.6.1.4.1.43689.1.2.4.2.0" , 17),
    #SenseurDHT('Cave'   , "1.3.6.1.4.1.43689.1.2.8.1.0" , "1.3.6.1.4.1.43689.1.2.8.2.0" , 11),
    SenseurDHT('Rasp'   , "1.3.6.1.4.1.43689.1.2.13.1.0", "1.3.6.1.4.1.43689.1.2.13.2.0",  9),
  ]
  dic = {}
  for senseur in allSenseurs :
    GPIO.setup(senseur.pin, GPIO.IN)
    senseur.getDhtValues()
    dic[senseur.label] = senseur
    # print "Humidity    : ",senseur.label, dic[senseur.label].toSnmpSetHum()
    # print "Temperature : ",senseur.label, dic[senseur.label].toSnmpSetTemp()

  cmdGen = cmdgen.CommandGenerator()
  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget((ipHostSnmp, 161)),
    dic['Ext'].toSnmpSetHum(),
    dic['Ext'].toSnmpSetTemp(),
    dic['Salon'].toSnmpSetHum(),
    dic['Salon'].toSnmpSetTemp(),
    dic['Sdb'].toSnmpSetHum(),
    dic['Sdb'].toSnmpSetTemp(),
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

