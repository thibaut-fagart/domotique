#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, time, re
import sharemem
import DomoLogic
import DomoData
import httplib
import datetime
import serial

class DomoUtils:
  def printlog(self,text):
    fileToBeWriten = "/home/dimi/prog/DomoCoreLog.txt"
    fichierWrite = open(fileToBeWriten,'a')
    fichierWrite.write(text)
    fichierWrite.close()  


class DomoCore:

  def __init__(self):
    self.shm = sharemem.Globshm()
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
    self.shm.connectState = 0
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

    self.deltaTimeSensorSerial   =  datetime.timedelta(seconds=5)
    self.deltaTimeSensorEthernet =  datetime.timedelta(seconds=30)
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

    try:
       self.arduino=serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.1)
       DomoUtils().printlog('Arduino serial link started on ACM0 \n')
       self.shm.connectState = 2
    except IOError:
       self.shm.connectState = 3
       DomoUtils().printlog('Arduino serial link Not started on ACM0 \n')
 
    self.refresh()

  def refresh(self):
    while (self.shm.connectState != 3):
      if (self.shm.connectState == 2):
         now = datetime.datetime.now()
         if (now - self.memoNowSensorSerial > self.deltaTimeSensorSerial):
            self.memoNowSensorSerial = now

            self.logic()

            self.set_diArduino('VMC',self.shm.VMCPower)
            self.set_diArduino('Ventilo-SdB1',self.shm.ventiloSdbPower)
            self.set_diArduino('Ventilo-SdB2',self.shm.ventiloSdbPower)
            try:
              self.shm.ventiloSdbSpeed = self.set_PWMArduino('Ventilo-SdB',self.shm.ventiloSdbReq)
            except:
              DomoUtils().printlog('PWM Sdb setting error \n')
              self.shm.ventiloSdbSpeed = 9999

            #self.shm.rpmSdb = self.get_valueArduino('Ventilo-SdB-Speed')

            self.set_diArduino('Ventilo-Couloir1',self.shm.ventiloCouloirPower)
            self.set_diArduino('Ventilo-Couloir2',self.shm.ventiloCouloirPower)
            try:
              self.shm.ventiloCouloirSpeed = self.set_PWMArduino('Ventilo-Couloir',self.shm.ventiloCouloirReq)
            except:
              DomoUtils().printlog('PWM couloir setting error \n')
              self.shm.ventiloSdbSpeed = 9999

            #self.shm.rpmCouloir = self.get_valueArduino('Ventilo-Couloir-Speed')

            self.set_diArduino('Audio-Cuisine',self.shm.audioCuisinePower)
            self.set_diArduino('Audio-SdB',self.shm.audioSdbPower)
            self.set_diArduino('Audio-Chambre',self.shm.audioChambrePower)
            self.set_diArduino('Thermostat',self.shm.forceChaudiere)

            error, self.shm.tempPC,    self.shm.humPC    = self.get_dth22Arduino('PC')
            error, self.shm.tempSdb,   self.shm.humSdb   = self.get_dth22Arduino('SdB')
            error, self.shm.tempSalon, self.shm.humSalon = self.get_dth22Arduino('Salon')
            error, self.shm.tempExt,   self.shm.humExt   = self.get_dth22Arduino('Ext')
            self.shm.porteFermee = self.get_switchArduino('Porte')

         if (now - self.memoNowSensorEthernet > self.deltaTimeSensorEthernet):
            self.memoNowSensorEthernet = now
            try:
               self.get_dth22Ethernet(self.caveHost,self.cavePort)
            except:
               self.shm.tempCave = 999.9
               self.shm.humCave = 999.9
               self.shm.presenceCave = 0

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

  def set_PWMArduino(self,actuator,value):
    if value > self.speedOld[actuator]:
      self.arduino.write(actuator+'++')
      time.sleep(0.01)
      self.speedOld[actuator] = int(self.arduino.readline().split(':')[-1])
    if value < self.speedOld[actuator]:
      self.arduino.write(actuator+'--')
      time.sleep(0.01)
      self.speedOld[actuator] = int(self.arduino.readline().split(':')[-1])

    return self.speedOld[actuator]
  
  def set_diArduino(self,actuator,state):
    if state:
    	self.arduino.write(actuator+'-ON')
    else:
    	self.arduino.write(actuator+'-OFF')
    time.sleep(0.01)
  
  def get_AnalogArduino(self,sensor):
    self.arduino.write(sensor)
    time.sleep(0.01)
    return self.arduino.readline()

  def get_valueArduino(self,sensor):
    self.arduino.write(sensor)
    time.sleep(0.2)
    return int(self.arduino.readline().split(':')[-1])

  def get_switchArduino(self,sensor):
    self.arduino.write(sensor)
    time.sleep(0.01)
    return self.arduino.readline() == "CLOSED"

  def get_dth22Arduino(self,sensor):
    try:
      self.arduino.write(sensor)
      time.sleep(0.01)
      s = self.arduino.readline()
    except:
      errlog = sensor + ' dth22Arduino write failure (Serial link probably) \n'
      DomoUtils().printlog(errlog)
    try:
        sSplit = s.split(':')
	tempSensor = float(sSplit[1])
	humSensor  = float(sSplit[0])
	error = 'Ok'
    except:
	if (sSplit[0] == 'Error'):
           error = 'Error number = %s'%sSplit[0]
           errlog = sensor + ' : ' + sSplit[0] + ' : ' + sSplit[1] + ' : ' + error + '\n'
           DomoUtils().printlog(errlog)
        else:
           sBis = self.arduino.readline()
           error = 'message = %s'%sSplit[0]
           errlog = sensor + ' : ' + error + '\n'
           DomoUtils().printlog(errlog)
	tempSensor = 999.9
	humSensor  = 999.9


    return error,tempSensor,humSensor
  
#========== Programme principal =============
if __name__ == '__main__':

  DomoCore()
