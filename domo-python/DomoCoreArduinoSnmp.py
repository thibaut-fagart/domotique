#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, time, re
import sharemem
import DomoLogic
import DomoData
import httplib
import datetime
import serial
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

class DomoUtils:
  def printlog(self,text):
    fileToBeWriten = "/home/dimi/prog/DomoCoreLog.txt"
    fichierWrite = open(fileToBeWriten,'a')
    fichierWrite.write(text)
    fichierWrite.close()  


class DomoCore:

  def __init__(self):
    self.shm = sharemem.Globshm()

    self.Host = "192.168.0.70"
    self.oidTempSalon  = "1.3.6.1.4.1.36582.1"
    self.oidHumidSalon = "1.3.6.1.4.1.36582.2"
    self.oidTempPC     = "1.3.6.1.4.1.36582.3"
    self.oidHumidPC    = "1.3.6.1.4.1.36582.4"
    self.oidTempSdB    = "1.3.6.1.4.1.36582.5"
    self.oidHumidSdB   = "1.3.6.1.4.1.36582.6"
    self.oidTempExt    = "1.3.6.1.4.1.36582.7"
    self.oidHumidExt   = "1.3.6.1.4.1.36582.8"
    self.oidVentiloCouloir1State = "1.3.6.1.4.1.36582.10"
    self.oidVentiloCouloir2State = "1.3.6.1.4.1.36582.11"
    self.oidVentiloCouloirSpeed  = "1.3.6.1.4.1.36582.12"
    self.oidVentiloSdB1State     = "1.3.6.1.4.1.36582.15"
    self.oidVentiloSdB2State     = "1.3.6.1.4.1.36582.16"
    self.oidVentiloSdBSpeed      = "1.3.6.1.4.1.36582.17"
    self.oidPorteState        = "1.3.6.1.4.1.36582.20"
    self.oidThermostatState   = "1.3.6.1.4.1.36582.21"
    self.oidAmpliSalonState   = "1.3.6.1.4.1.36582.30"
    self.oidAmpliSdBState     = "1.3.6.1.4.1.36582.31"
    self.oidAmpliCuisineState = "1.3.6.1.4.1.36582.32"
    self.oidAmpliChambreState = "1.3.6.1.4.1.36582.33"
    self.oidVMCState          = "1.3.6.1.4.1.36582.40"

    self.shm.tempExtEte = 15.
    self.shm.tempExt = 20.
    self.shm.tempCave = 14.
    self.shm.tempPC = 30.
    self.shm.humSdb = 40.
    self.shm.humSalon = 40.
    self.shm.humCave = 70.
    self.shm.forceChaudiere = 0
    self.shm.presenceCave = 0
    self.shm.audioMan = 0
    self.shm.VMCMan = 0
    self.shm.audioMaxDelay = 240
    self.shm.audioCurrentDelay = 0
    self.shm.connectState = 1
    self.shm.timeValOld = 0

    self.shm.audioSalonPower = 1      
    self.shm.audioChambrePower = 0   
    self.shm.audioCuisinePower = 0  
    self.shm.audioSdbPower = 0      
    self.shm.VMCPower = 1           
    self.speedOld = {}
    self.shm.ventiloSdbPower = 0    
    self.speedOld["Ventilo-SdB"] = 800
    self.shm.ventiloCouloirPower = 0
    self.speedOld["Ventilo-Couloir"] = 800
    self.shm.forceChaudiere = 0     
    self.shm.porteFermee = 0        
    self.di2 = 0
    self.di3 = 0
    self.di4 = 0
    self.di5 = 0

    self.memo = 0
    self.PreviousForceChaudiere = 0

    self.deltaTimeSensorFast     =  datetime.timedelta(seconds=15)
    self.deltaTimeSensorSnmp     =  datetime.timedelta(seconds=30)
    self.deltaTimeStore          =  datetime.timedelta(minutes=5)
    self.deltaTimeWrite          =  datetime.timedelta(hours=2)
    self.deltaTimeFile           =  datetime.timedelta(days=7)
    self.memoNowSensorSerial     =  datetime.datetime.now()
    self.memoNowSensorEthernet   =  datetime.datetime.now()
    self.memoNowStore            =  datetime.datetime.now()
    self.memoNowWrite            =  datetime.datetime.now()
    self.data = {}
    self.filePath = "/home/dimi/prog/data"
    self.firstFileReading = True
    self.caveHost = '192.168.0.60'
    self.cavePort = '999'

    self.refresh()

  def refresh(self):
    while (self.shm.connectState == 1):
         now = datetime.datetime.now()
         if (now - self.memoNowSensorSerial > self.deltaTimeSensorFast):
            self.memoNowSensorSerial = now

            self.logic()

            self.set_ArduinoValue(self.oidVMCState,self.Host,self.shm.VMCPower)
            self.set_ArduinoValue(self.oidVentiloSdB1State,self.Host,self.shm.ventiloSdbPower)
            self.set_ArduinoValue(self.oidVentiloSdB2State,self.Host,self.shm.ventiloSdbPower)
            self.set_ArduinoValue(self.oidVentiloCouloir1State,self.Host,self.shm.ventiloCouloirPower)
            self.set_ArduinoValue(self.oidVentiloCouloir2State,self.Host,self.shm.ventiloCouloirPower)

            self.shm.ventiloSdbSpeed = self.set_ArduinoValue(self.oidVentiloSdBSpeed,self.Host,self.shm.ventiloSdbReq)
            self.shm.ventiloCouloirSpeed = self.set_ArduinoValue(self.oidVentiloCouloirSpeed,self.Host,self.shm.ventiloCouloirReq)

            self.set_ArduinoValue(self.oidAmpliCuisineState,self.Host,self.shm.audioCuisinePower)
            self.set_ArduinoValue(self.oidAmpliSdBState,self.Host,self.shm.audioSdbPower)
            self.set_ArduinoValue(self.oidAmpliChambreState,self.Host,self.shm.audioChambrePower)

            self.set_ArduinoValue(self.oidThermostatState,self.Host,self.shm.forceChaudiere)
            self.shm.porteFermee = self.get_ArduinoValue(self.oidPorteState,self.Host)


         if (now - self.memoNowSensorEthernet > self.deltaTimeSensorSnmp):
            self.memoNowSensorEthernet = now
            try:
               self.get_dth22Ethernet(self.caveHost,self.cavePort)
            except:
               self.shm.tempCave = 999.9
               self.shm.humCave = 999.9
               self.shm.presenceCave = 0

            self.shm.tempPC    = float(self.get_ArduinoValue(self.oidTempPC,self.Host))/10.
            self.shm.humPC     = float(self.get_ArduinoValue(self.oidHumidPC,self.Host))/10.
            self.shm.tempSdb   = float(self.get_ArduinoValue(self.oidTempSdB,self.Host))/10.
            self.shm.humSdb    = float(self.get_ArduinoValue(self.oidHumidSdB,self.Host))/10.
            self.shm.tempSalon = float(self.get_ArduinoValue(self.oidTempSalon,self.Host))/10.
            self.shm.humSalon  = float(self.get_ArduinoValue(self.oidHumidSalon,self.Host))/10.
            self.shm.tempExt   = float(self.get_ArduinoValue(self.oidTempExt,self.Host))/10.
            self.shm.humExt    = float(self.get_ArduinoValue(self.oidHumidExt,self.Host))/10.

            DomoData.write_file(self, self.filePath)


  def logic(self):
    DomoLogic.logic_VMC(self)
    DomoLogic.logic_Music(self)
    self.PreviousForceChaudiere = DomoLogic.logic_thermostat(self,self.PreviousForceChaudiere)

    self.shm.audioCurrentDelay = max((int(time.time()) - self.shm.lastPacketChambre), self.shm.audioCurrentDelay)  
    self.shm.audioCurrentDelay = max((int(time.time()) - self.shm.lastPacketCuisine), self.shm.audioCurrentDelay)  
    self.shm.audioCurrentDelay = max((int(time.time()) - self.shm.lastPacketSdb), self.shm.audioCurrentDelay)  

  def get_dth22Ethernet(self,Host,Port):
    httpServ= httplib.HTTPConnection(Host, Port )
    httpServ.request("GET", "/index.html")
    reponse = httpServ.getresponse().read().split(':End:')

    for rep in reponse:
       if (rep.split(':')[0] == 'DHT'):
          self.shm.tempCave = float(rep.split(':')[2])
          self.shm.humCave = float(rep.split(':')[4])
       if (rep.split(':')[0] == 'Error'):
          self.shm.tempCave = 999.9
          self.shm.humCave = 999.9
       if (rep.split(':')[0] == 'PIR'):
          self.shm.presenceCave = int(rep.split(':')[2])

    httpServ.close()

  def get_ArduinoValue(self,Oid,Host):
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
          cmdgen.CommunityData('public',mpModel=0),
          cmdgen.UdpTransportTarget((Host, 161)),
          Oid )
    # Check for errors and print out results
    if errorIndication:
       DomoUtils().printlog('get oid %s from %s errorIndication : %s'%(Oid,Host,errorIndication))
    else:
        if errorStatus:
            DomoUtils().printlog('get oid %s from %s errorStatus : %s at %s'%(Oid,Host,errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
        else:
            for name, val in varBinds:
                # DomoUtils().printlog('get oid %s from %s : %s = %s'%(Oid,Host,name.prettyPrint(), val.prettyPrint())
                return val

  def set_ArduinoValue(self,Oid,Host,value):
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
          cmdgen.CommunityData('private',mpModel=0),
          cmdgen.UdpTransportTarget((Host, 161)),
          (Oid, rfc1902.Integer(value)))

    # Check for errors and print out results
    if errorIndication:
       DomoUtils().printlog('get oid %s from %s errorIndication : %s'%(Oid,Host,errorIndication))
    else:
        if errorStatus:
            DomoUtils().printlog('get oid %s from %s errorStatus : %s at %s'%(Oid,Host,errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
        else:
            for name, val in varBinds:
                # DomoUtils().printlog('get oid %s from %s : %s = %s'%(Oid,Host,name.prettyPrint(), val.prettyPrint())
                return val
  
#========== Programme principal =============
if __name__ == '__main__':

  DomoCore()
