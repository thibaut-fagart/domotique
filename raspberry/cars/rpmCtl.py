#!/usr/bin/env python

import time
import threading
from motor import motor

class rpmCtl(threading.Thread): 
    def __init__(self, shared): 
        threading.Thread.__init__(self) 
        self.shared = shared
        self.minESC = 0
        self.neutralESC = 35
        self.maxESC = 100
        self.shared.set('neutralESC', self.neutralESC)
        self.shared.set('rpm', self.neutralESC)

        # Set Pin 24 as ESC
        self.servoPin = 24
        self.mymotor = motor('m1', self.servoPin, simulation=False)
        self.mymotor.start()
        self.mymotor.setW(self.maxESC)
        time.sleep(2)
        self.mymotor.setW(self.neutralESC)
        self.oldspeedValue = self.neutralESC
        self._stopevent = threading.Event( ) 
	  
    def run(self): 
        while not self._stopevent.isSet(): 
            speedValue = self.shared.get('rpm')
            speedValue = max(speedValue,self.minESC)
            speedValue = min(speedValue,self.maxESC)
            if speedValue != self.oldspeedValue:
                self.mymotor.setW(speedValue) 
                self.oldspeedValue = speedValue
                self._stopevent.wait(0.01) 
		  
    def stop(self): 
        self._stopevent.set( ) 
  