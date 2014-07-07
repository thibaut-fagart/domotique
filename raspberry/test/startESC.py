#!/usr/bin/env python

import memcache
import RPi.GPIO as GPIO
import time
import math
from motor import motor


if __name__ == '__main__':
  shared = memcache.Client(['127.0.0.1:11211'], debug=0)
  mymotor = motor('m1', 24, simulation=False)
 
  mymotor.start()
  mymotor.setW(100)
  time.sleep(2)
  mymotor.setW(35)


  while True:
    time.sleep(2)
    speedValue = (35)
    speedValue = max(speedValue,0)
    speedValue = min(speedValue,100)
    mymotor.setW(speedValue)

