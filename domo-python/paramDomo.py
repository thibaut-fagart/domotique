#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sharemem

#========== Programme principal =============

if __name__ == '__main__':
  shm = sharemem.Globshm()

  print "PC    : %.1f"%shm.tempPC   , "°C : %.1f"%shm.humPC   , "%"
  print "Ext   : %.1f"%shm.tempExt  , "°C : %.1f"%shm.humExt  , "%"
  print "Salon : %.1f"%shm.tempSalon, "°C : %.1f"%shm.humSalon, "%"
  print "SdB   : %.1f"%shm.tempSdb  , "°C : %.1f"%shm.humSdb  , "%"
  print "Cave  : %.1f"%shm.tempCave , "°C : %.1f"%shm.humCave , "%"
