#!/usr/bin/env python
# -*- coding:utf-8 -*-

import serial
from setsnmp import setSnmp
from getsnmp import getSnmp
from pysnmp.proto import rfc1902

class Edf:
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
    
    def __init__(self):
      self.Isousc =None
      self.Ejphn  =None
      self.Ejphpm =None
      self.Ptec   =None
      self.Iinst1 =None
      self.Iinst2 =None
      self.Iinst3 =None
      self.Imax1  =None
      self.Imax2  =None
      self.Imax3  =None
      self.Pmax   =None
      self.Papp   =None

    def toSnmpIsousc(self):
        return (self.oidEdfIsousc, rfc1902.Integer(self.Isousc))

    def toSnmpEjpHpm(self):
        return (self.oidEdfEjphpm, rfc1902.Integer(self.Ejphpm))

    def toSnmpEjpHn(self):
        return (self.oidEdfEjphn, rfc1902.Integer(self.Ejphn))

    def toSnmpIInst1(self):
        return (self.oidEdfIinst1, rfc1902.Integer(self.Iinst1))

    def toSnmpIInst2(self):
        return (self.oidEdfIinst2, rfc1902.Integer(self.Iinst2))

    def toSnmpIInst3(self):
        return (self.oidEdfIinst3, rfc1902.Integer(self.Iinst3))

    def toSnmpPApp(self):
        return (self.oidEdfPapp, rfc1902.Integer(self.Papp))


ipHostSnmp    = "192.168.0.199"

ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate=1200,
	parity=serial.PARITY_EVEN,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.SEVENBITS )


def checksum (etiquette, valeur):
                sum = 32
                for c in etiquette: sum = sum + ord(c)
                for c in valeur:        sum = sum + ord(c)
                sum = (sum & 63) + 32
                return chr(sum)


def LireTeleinfo ():
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
                print trames
                        
                tramesValides = dict([
                        [trame[0],trame[1]]
                        for trame in trames
                        if (len(trame) == 3) and (checksum(trame[0],trame[1]) == trame[2])
                        ])
                        
                return tramesValides

def teleinfoEJP():
  ser.flushInput()
  tramesOk = LireTeleinfo()
  #print tramesOk
  edf = Edf()
  for etiquette in tramesOk:
	  #if etiquette ==  'ADCO':
                  #result = setSnmp(ipHostSnmp,oidEdfAdco,int(tramesOk[etiquette]))
	  #if etiquette ==  'OPTARIF':
                  #result = setSnmp(ipHostSnmp,oidEdfOptarif,int(tramesOk[etiquette]))
	  if etiquette ==  'ISOUSC':
        	  edf.Isousc = int (tramesOk[etiquette])
                  #print 'ISOUSC ',tramesOk[etiquette]
	  if etiquette ==  'EJPHN':
        	  edf.Ejphn = int (tramesOk[etiquette])
                  #print 'EJPHN ',tramesOk[etiquette]
	  if etiquette ==  'EJPHPM':
        	  edf.Ejphpm = int (tramesOk[etiquette])
                  #print 'EJPHPM ',tramesOk[etiquette]
	  #if etiquette ==  'PTEC':
        	  #result = setSnmp(ipHostSnmp,oidEdfPtec,int(tramesOk[etiquette]))
    	  if etiquette == 'IINST1':
        	  edf.Iinst1 = int(tramesOk[etiquette])
                  #print 'IINST1 ',tramesOk[etiquette]
    	  if etiquette == 'IINST2':
        	  edf.Iinst2 = int(tramesOk[etiquette])
                  #print 'IINST2 ',tramesOk[etiquette]
    	  if etiquette == 'IINST3':
        	  edf.Iinst3 = int(tramesOk[etiquette])
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
        	  edf.Papp = int(tramesOk[etiquette])
                  #print 'PAPP ',tramesOk[etiquette]
  ser.close()
  return edf


if __name__ == "__main__":
  teleinfoEJP()
