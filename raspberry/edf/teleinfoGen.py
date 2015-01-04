#!/usr/bin/env python
# -*- coding:utf-8 -*-

import serial
import datetime
import time
from pysnmp.proto import rfc1902

RaspberryPath = "/home/prog/raspberry"

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=1200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS)

class TeleinfoLabel :
  def __init__(self, aLabel, anOid):
    self.label =  aLabel
    self.oid =  anOid
  def toSnmpSet(self):
    return (self.oid, rfc1902.Integer(self.value))
  def isValid(self):
    if (None == self.value):
      return False
      printlog(time.asctime(),'read label teleinfo %s error With value : %s'%(self.label,self.value))
    else:
      return True

class Edf:
  def __init__(self):
    listTeleinfoLabel = [
    #TeleinfoLabel('ADCO'   , "1.3.6.1.4.1.43689.1.4.1.0"),
    #TeleinfoLabel('OPTARIF', "1.3.6.1.4.1.43689.1.4.2.0"),
    TeleinfoLabel('ISOUSC' , "1.3.6.1.4.1.43689.1.4.3.0"),
    TeleinfoLabel('EJPHN'  , "1.3.6.1.4.1.43689.1.4.9.0"),
    TeleinfoLabel('EJPHPM' , "1.3.6.1.4.1.43689.1.4.10.0"),
    #TeleinfoLabel('PTEC'   , "1.3.6.1.4.1.43689.1.4.5.0"),
    TeleinfoLabel('IINST1' , "1.3.6.1.4.1.43689.1.4.11.0"),
    TeleinfoLabel('IINST2' , "1.3.6.1.4.1.43689.1.4.12.0"),
    TeleinfoLabel('IINST3' , "1.3.6.1.4.1.43689.1.4.13.0"),
    TeleinfoLabel('IMAX1'  , "1.3.6.1.4.1.43689.1.4.14.0"),
    TeleinfoLabel('IMAX2'  , "1.3.6.1.4.1.43689.1.4.15.0"),
    TeleinfoLabel('IMAX3'  , "1.3.6.1.4.1.43689.1.4.16.0"),
    TeleinfoLabel('PMAX'   , "1.3.6.1.4.1.43689.1.4.17.0"),
    TeleinfoLabel('PAPP'   , "1.3.6.1.4.1.43689.1.4.8.0"),
    ]

    self.allTeleinfoLabel = {} 
    for teleinfoLabel in listTeleinfoLabel :
      self.allTeleinfoLabel[teleinfoLabel.label] = teleinfoLabel


def checksum(etiquette, valeur):
    sum = 32
    for c in etiquette: sum = sum + ord(c)
    for c in valeur: sum = sum + ord(c)
    sum = (sum & 63) + 32
    return chr(sum)


def LireTeleinfo():
    # Attendre le debut du message
    while ser.read(1) != chr(2): pass

    message = ""
    fin = False

    while not fin:
      char = ser.read(1)
      if char != chr(2):
        message = message + char
      else:
        fin = True

    trames = [
      trame.split(" ")
      for trame in message.strip("\r\n\x03").split("\r\n")
    ]
    # print trames

    tramesValides = dict([
      [trame[0], trame[1]]
      for trame in trames
      if (len(trame) == 3) and (checksum(trame[0], trame[1]) == trame[2])
    ])

    return tramesValides


def teleinfo():
    ser.flushInput()
    tramesOk = LireTeleinfo()
    edf = Edf()
    for etiquette in tramesOk:
      if etiquette in edf.allTeleinfoLabel:
        edf.allTeleinfoLabel[etiquette].value = int(tramesOk[etiquette])
        # print edf.allTeleinfoLabel[etiquette].label, ' = ', int(tramesOk[etiquette])
      # else:
        # print etiquette, " : etiquette non supportee"
    ser.close()
    return edf


if __name__ == "__main__":
  edf = teleinfo()
