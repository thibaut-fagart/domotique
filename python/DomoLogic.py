#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, time, re

def logic_Music(self):
  if (self.shm.audioMan == False):
    self.shm.audioChambrePower = ((int(time.time()) - self.shm.lastPacketChambre) < self.shm.audioMaxDelay)
    self.shm.audioCuisinePower = ((int(time.time()) - self.shm.lastPacketCuisine) < self.shm.audioMaxDelay)
    self.shm.audioSdbPower = ((int(time.time()) - self.shm.lastPacketSdb) < self.shm.audioMaxDelay)

def logic_thermostat(self,PreviousForceChaudiere):
  if (self.shm.forceChaudiere == 1) and (PreviousForceChaudiere == 1):
    self.shm.forceChaudiere = 0
  return self.shm.forceChaudiere

def logic_VMC(self):
    if self.shm.VMCMan == False:
        if (self.shm.tempExt > self.shm.tempExtEte + 0.5):
            self.shm.VMCPower = 1
            self.shm.ventiloSdbPower = 0
            self.shm.ventiloCouloirPower = 0
        else:
            if (self.shm.humSdb > self.shm.humSalon + 20.):
                self.shm.VMCPower = 1
                self.shm.ventiloSdbPower = 0
                self.shm.ventiloCouloirPower = 0
            if ((self.shm.humSdb < self.shm.humSalon + 10.) and (self.shm.tempExt < self.shm.tempExtEte - 0.5)):
                self.shm.VMCPower = 0
                self.shm.ventiloSdbPower = 1
                self.shm.ventiloCouloirPower = 1

#========== Programme principal =============
if __name__ == '__main__':

  logic_VMC()
