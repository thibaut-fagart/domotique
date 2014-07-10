#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import threading
from pizypwm import PiZyPwm


class dirCtl(threading.Thread): 
    def __init__(self, shared): 
        threading.Thread.__init__(self) 
        self.shared = shared
        self.leftDir = 5
        self.rightDir = 10
        self.minServo = -45
        self.neutralServo = 0
        self.maxServo = 45
        self.shared.set('neutralServo', self.neutralServo)
        self.shared.set('headingWheel', self.neutralServo)
		
        # Set Pin 11 as Servo
        self.servoPin = 11
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servoPin, GPIO.OUT)		
        # Start PWM with 50Hz
        self.Servo = PiZyPwm(50, self.servoPin, GPIO.BOARD)
        self.oldDirValue = self.neutralServo
        self._stopevent = threading.Event( ) 
		
    def run(self): 
        while not self._stopevent.isSet(): 
            dirDeltaValue = self.shared.get('headingWheel') - self.oldDirValue
            dirDeltaValue = max(dirDeltaValue,self.minServo - self.oldDirValue)
            dirDeltaValue = min(dirDeltaValue,self.maxServo - self.oldDirValue)
            if dirDeltaValue > 0:
                Servo.start(self.leftDir)
                for Counter in range(int(abs(dirDeltaValue))):
                    time.sleep(0.001)
                Servo.stop()
                self.oldDirValue = self.oldDirValue + dirDeltaValue
            if dirDeltaValue < 0:
                Servo.start(self.rightDir)
                for Counter in range(int(abs(dirDeltaValue))):
                    time.sleep(0.001)
                Servo.stop()
                self.oldDirValue = self.oldDirValue + dirDeltaValue
            self._stopevent.wait(0.01) 
		  
    def stop(self): 
	GPIO.cleanup()
        self._stopevent.set( ) 

