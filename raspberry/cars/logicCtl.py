#!/usr/bin/env python

import time, random
import threading

class logicCtl(threading.Thread): 
    def __init__(self, shared): 
        threading.Thread.__init__(self) 
        self.shared = shared
        self.distAvoid = 200
        self.hysteresisOpenField = 50
        self.neutralESC = self.shared.get('neutralESC')
        self._stopevent = threading.Event( )
        self.filterP = filterP(self.shared.get('capMag'))		
	  
    def run(self): 
        while not self._stopevent.isSet(): 
            if self.shared.get('modeDrive') == 'avoid':
                for intruder in [0, 45, 135, 180, 225, 315]:
                    if self.shared.get('Srf02-%s'%intruder) < self.distAvoid: 
		        if self.shared.get('Srf02-%s'%intruder+180) > self.distAvoid:
			    self.goDir('slow',intruder+180)
			else:
			    self.goDir('stop',intruder+180)
	            else:
			self.goDir('stop',intruder+180)

            if self.shared.get('modeDrive') == 'alone':
	        direction = self.shared.get('capMag')
                for openField in [0, 45, 135, 180, 225, 315]:
                    if self.shared.get('Srf02-%s'%direction) < (int(self.shared.get('Srf02-%s'%openField)) - self.hysteresisOpenField):
                        direction = openField
                if self.shared.get('Srf02-%s'%direction) > self.distAvoid: 
		    self.goDir('slow',direction)
		else:
		    self.goDir('stop',direction)
					
            if self.shared.get('modeDrive') == 'random':
		direction = random.randint(0, 360)
		if self.shared.get('Srf02-%s'%direction) > self.distAvoid: 
		    self.goDir('slow',direction)
		else:
		    self.goDir('stop',direction)

    def goDir(self,typeCtl,direction): 
	headingCars = self.shared.get('capMag')
	headingWheel = direction - headingCars
	self.shared.set('headingWheel',self.filterP.filt(self.from360to180(headingWheel)))
	if typeCtl == 'stop':
	    self.shared.set('rpm',self.neutralESC)
	else:
	    if typeCtl == 'slow':
	        self.shared.set('rpm',self.neutralESC+6)
		
    def from360to180(self,value):
        if value > 180:
            return value - 360
	elif value < -180:
            return value + 360
	else:
            return value
		
    def stop(self): 
        self._stopevent.set( ) 
		
class filterP(): 
    def __init__(self,value): 
        self.value = value
	self.valueOld = value
		
    def filt(self,value):
    	valueFiltered = self.valueOld + (value - self.valueOld)/self.filterGain
	self.valueOld = valueFiltered
	return valueFiltered
