#!/usr/bin/env python

import memcache
import RPi.GPIO as GPIO
import time
import math
import smbus
from motor import motor
from Adafruit_I2C import Adafruit_I2C
from pizypwm import PiZyPwm
#from pizypwm import *

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
  

class dirCtl(threading.Thread): 
    def __init__(self, shared): 
        threading.Thread.__init__(self) 
        self.shared = shared
	self.minServo = -45
	self.neutralServo = 0
	self.maxServo = 45
	self.shared.set('neutralServo', self.neutralServo)
        self.shared.set('heading', self.neutralServo)
		
	# Set Pin 11 as Servo
	self.servoPin = 11
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(self.servoPin, GPIO.OUT)		
	# Start PWM with 50Hz
        Servo = PiZyPwm(50, self.servoPin, GPIO.BOARD)
	self.oldDirValue = self.neutralServo
        self._stopevent = threading.Event( ) 
		
    def run(self): 
        while not self._stopevent.isSet(): 
            dirDeltaValue = self.shared.get('heading') - self.oldDirValue
            dirDeltaValue = max(dirDeltaValue,self.minServo - self.oldDirValue)
            dirDeltaValue = min(dirDeltaValue,self.maxServo - self.oldDirValue)
	    if dirDeltaValue != 0:
                servoCtl(Servo,dirDeltaValue)
                self.oldDirValue = self.oldDirValue + dirDeltaValue
            self._stopevent.wait(0.01) 
		  
    def servoCtl(Servo,increment):
	# Generate PWM with 10% Dutycycle (2ms)
	Servo.start(increment/abs(increment))
	for Counter in range(int(increment)):
            time.sleep(0.001)
	    # PWM stop
	    Servo.stop()
	    GPIO.cleanup()
		
    def stop(self): 
        self._stopevent.set( ) 
  
class i2csensor(threading.Thread): 
    def __init__(self, shared): 
        threading.Thread.__init__(self) 
        self.shared = shared
        self.shared.set('Random', 0)
        self.shared.set('accError',0)
        self.shared.set('i2cAccPower',0)
        self.shared.set('srf02Error',0)
        self.shared.set('i2cSRF02Power',1)
        self.lsm = Adafruit_LSM303()
	self.i2c = smbus.SMBus(1)
        self.adress = (0x71,0x72,0x73,0x75,0x76,0x77)
        self.mode   = 81      # centimetres
        self._stopevent = threading.Event( ) 
	  
    def run(self): 
        while not self._stopevent.isSet(): 
	    if shared.get('i2cAccPower'):
		try:
	            accResult, magResult = self.lsm.read()
		except:
		    self.shared.set('accError',self.shared.get('accError')+1)
		time.sleep(0.07)
		self.shared.set('accX',accResult[0])
		self.shared.set('accY',accResult[1])
		self.shared.set('accZ',accResult[2])
		self.shared.set('capMag',magResult[3])

	    if shared.get('i2cSRF02Power'):
		for srf02Adress in adress:
		    try:
			self.i2c.write_byte_data(srf02Adress, 0, mode) # lance un "ping" en centimetre
			dst = self.i2c.read_word_data(srf02Adress, 2) / 255
			self.shared.set('%s'%hex(srf02Adress),dst)
		    except:
			self.shared.set('srf02Error',self.shared.get('srf02Error')+1)
		    time.sleep(0.07)
            self._stopevent.wait(0.01) 
		  
    def stop(self): 
        self._stopevent.set( ) 


class Adafruit_LSM303(Adafruit_I2C):

    # Minimal constants carried over from Arduino library
    LSM303_ADDRESS_ACCEL = (0x32 >> 1)  # 0011001x
    LSM303_ADDRESS_MAG   = (0x3C >> 1)  # 0011110x
                                             # Default    Type
    LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20 # 00000111   rw
    LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23 # 00000000   rw
    LSM303_REGISTER_ACCEL_OUT_X_L_A   = 0x28
    LSM303_REGISTER_MAG_CRB_REG_M     = 0x01
    LSM303_REGISTER_MAG_MR_REG_M      = 0x02
    LSM303_REGISTER_MAG_OUT_X_H_M     = 0x03

    # Gain settings for setMagGain()
    LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3
    LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9
    LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5
    LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0
    LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7
    LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6
    LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1

    def __init__(self, busnum=-1, debug=False, hires=False):

        # Accelerometer and magnetometer are at different I2C
        # addresses, so invoke a separate I2C instance for each
        self.accel = Adafruit_I2C(self.LSM303_ADDRESS_ACCEL, busnum, debug)
        self.mag   = Adafruit_I2C(self.LSM303_ADDRESS_MAG  , busnum, debug)

        # Enable the accelerometer
        self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x27)
        # Select hi-res (12-bit) or low-res (10-bit) output mode.
        # Low-res mode uses less power and sustains a higher update rate,
        # output is padded to compatible 12-bit units.
        if hires:
            self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A,
              0b00001000)
        else:
            self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0)

        # Enable the magnetometer
        self.mag.write8(self.LSM303_REGISTER_MAG_MR_REG_M, 0x00)


    # Interpret signed 12-bit acceleration component from list
    def accel12(self, list, idx):
        n = list[idx] | (list[idx+1] << 8) # Low, high bytes
        if n > 32767: n -= 65536           # 2's complement signed
        return n >> 4                      # 12-bit resolution


    # Interpret signed 16-bit magnetometer component from list
    def mag16(self, list, idx):
        n = (list[idx] << 8) | list[idx+1]   # High, low bytes
        return n if n < 32768 else n - 65536 # 2's complement signed

    def magHeading(self, mx, my):
        heading = math.atan2 (my,mx)

        # Correct negative values
        if (heading < 0):
          heading = heading + (2 * math.pi)

        # convert to degrees
        heading = heading * 180/math.pi

        return heading

    def read(self):
        # Read the accelerometer
        listAcc = self.accel.readList(
          self.LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
        resAcc = [self.accel12(listAcc, 0),
                  self.accel12(listAcc, 2),
                  self.accel12(listAcc, 4) ]

        # Read the magnetometer
        listMag = self.mag.readList(self.LSM303_REGISTER_MAG_OUT_X_H_M, 6)
        resMag = [self.mag16(listMag, 0),
                  self.mag16(listMag, 2),
                  self.mag16(listMag, 4),
                  self.magHeading(self.mag16(listMag, 0),self.mag16(listMag, 4))]

        return resAcc, resMag


    def setMagGain(gain=LSM303_MAGGAIN_1_3):
        self.mag.write8( LSM303_REGISTER_MAG_CRB_REG_M, gain)


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
  carRpm.start() 
  carDir.start() 
  carI2C.start()

  while shared.get('RpiPower') == 0:
    carsTimer += 1
    time.sleep(1)
	
  carRpm.stop()
  carDir.stop()
  carI2C.stop()

