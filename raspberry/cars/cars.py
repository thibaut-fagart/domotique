#!/usr/bin/env python

import memcache
import time
from i2csensor import i2csensor
from rpmCtl import rpmCtl
from dirCtl import dirCtl
from logicCtl import logicCtl


if __name__ == '__main__':
  shared = memcache.Client(['127.0.0.1:11211'], debug=0)
 
 # Wait till memcache is started
  while shared.get('RpiPower') != 0:
    shared.set('RpiPower', 0)
    time.sleep(1)

# Start control of the different thread	
  carsTimer = 0
  carRpm = rpmCtl(shared) 
  carDir = dirCtl(shared) 
  carI2C = i2csensor(shared) 
  carLogic = logicCtl(shared) 
  
  carRpm.start() 
  carDir.start() 
  carI2C.start()
  carLogic.start()

  while shared.get('RpiPower') == 0:
    carsTimer += 1
    time.sleep(1)
	
  carRpm.stop()
  carDir.stop()
  carI2C.stop()
  carLogic.stop()

