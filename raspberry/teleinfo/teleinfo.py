#!/usr/bin/env python
# -*- coding:utf-8 -*-

import serial
from setsnmp import setSnmp
from getsnmp import getSnmp

oidEdfAdco    = "1.3.6.1.4.1.43689.1.3.1.1.0"
oidEdfOptarif = "1.3.6.1.4.1.43689.1.3.1.2.0"
oidEdfIsousc  = "1.3.6.1.4.1.43689.1.3.1.3.0"
oidEdfBase    = "1.3.6.1.4.1.43689.1.3.1.4.0"
oidEdfPtec    = "1.3.6.1.4.1.43689.1.3.1.5.0"
oidEdfIinst   = "1.3.6.1.4.1.43689.1.3.1.6.0"
oidEdfImax    = "1.3.6.1.4.1.43689.1.3.1.7.0"
oidEdfPapp    = "1.3.6.1.4.1.43689.1.3.1.8.0"
ipHostSnmp    = "192.168.0.211"

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
                        
                tramesValides = dict([
                        [trame[0],trame[1]]
                        for trame in trames
                        if (len(trame) == 3) and (checksum(trame[0],trame[1]) == trame[2])
                        ])
                        
                return tramesValides

if __name__ == "__main__":

  ser.flushInput()
  tramesOk = LireTeleinfo()
  trouve = False
  for etiquette in tramesOk:
	  if etiquette ==  'ADCO':
                  result = setSnmp(ipHostSnmp,oidEdfAdco,int(0))
                  #result = setSnmp(ipHostSnmp,oidEdfAdco,int(tramesOk[etiquette]))
	  if etiquette ==  'OPTARIF':
                  result = setSnmp(ipHostSnmp,oidEdfOptarif,int(0))
                  #result = setSnmp(ipHostSnmp,oidEdfOptarif,int(tramesOk[etiquette]))
	  if etiquette ==  'ISOUSC':
        	  result = setSnmp(ipHostSnmp,oidEdfIsousc,int(tramesOk[etiquette]))
	  if etiquette ==  'BASE':
        	  result = setSnmp(ipHostSnmp,oidEdfBase,int(tramesOk[etiquette]))
	  if etiquette ==  'PTEC':
        	  result = setSnmp(ipHostSnmp,oidEdfPtec,int(0))
        	  #result = setSnmp(ipHostSnmp,oidEdfPtec,int(tramesOk[etiquette]))
    	  if etiquette == 'IINST':
        	  result = setSnmp(ipHostSnmp,oidEdfIinst,int(tramesOk[etiquette]))
	  if etiquette ==  'IMAX':
        	  result = setSnmp(ipHostSnmp,oidEdfImax,int(tramesOk[etiquette]))
	  if etiquette ==  'PAPP':
        	  result = setSnmp(ipHostSnmp,oidEdfPapp,int(tramesOk[etiquette]))
  ser.close()
