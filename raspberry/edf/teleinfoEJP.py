#!/usr/bin/env python
# -*- coding:utf-8 -*-

import serial
import datetime
import time
from pysnmp.proto import rfc1902


class Etiquette:
    def __init__(self, oid, label):
        self.label = label
        self.value = None
        self.oid = oid
    def toSnmp(self):
        return None

class EtiquetteInt (Etiquette):
    def fromTrame(self, str):
        self.value = int(str)
    def toSnmp(self):
        print ("tosnmpEdf %s : %s" % (self.label, self.value))
        return (self.oid, rfc1902.Integer(self.value))

class EtiquetteStr (Etiquette):
    def fromTrame(self, str):
        self.value = str
    def toSnmp(self):
        print ("tosnmpEdf %s : %s" % (self.label, self.value))
        return (self.oid, rfc1902.Integer(self.value))

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
        self.etiquettes = {}
        self.etiquettes['ISOUSC'] = EtiquetteInt(Edf.oidEdfIsousc,'ISOUSC' )
        self.etiquettes['IINST1'] = EtiquetteInt(Edf.oidEdfIinst1, 'IINST1')
        self.etiquettes['IINST2'] = EtiquetteInt(Edf.oidEdfIinst2, 'IINST2')
        self.etiquettes['IINST3'] = EtiquetteInt(Edf.oidEdfIinst3, 'IINST3')
        self.etiquettes['PAPP'] = EtiquetteInt(Edf.oidEdfPapp, 'PAPP')
        self.etiquettes['EJPHN'] = EtiquetteInt(Edf.oidEdfIsousc, 'EJPHN')
        self.etiquettes['EJPHPM'] = EtiquetteInt(Edf.oidEdfIsousc, 'EJPHPM')

    def saveStats(self, filepath):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        edfFileData =filepath
        fileReadWrite = open(edfFileData, 'w')
        fileReadWrite.write(st)
        for etiquetteLabel in self.etiquettes:
            etiquette = self.etiquettes[etiquetteLabel]
            fileReadWrite.write(etiquette.label + ' : '+ etiquette.value)
        fileReadWrite.close()

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=1200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS)


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
    #print trames

    tramesValides = dict([
        [trame[0], trame[1]]
        for trame in trames
        if (len(trame) == 3) and (checksum(trame[0], trame[1]) == trame[2])
    ])

    return tramesValides


def teleinfoEJP():
    ser.flushInput()
    tramesOk = LireTeleinfo()
    edf = Edf()
    for etiquette in tramesOk:
        if etiquette in edf.etiquettes:
            edf.etiquettes[etiquette].value= int(tramesOk[etiquette])
        # else:
            #print "etiquette non supportee"
    ser.close()
    return edf


if __name__ == "__main__":
    edf = teleinfoEJP()
    edf.saveStats("edf.log")
