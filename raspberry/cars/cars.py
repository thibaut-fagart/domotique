#!/usr/bin/env python

import memcache
import RPi.GPIO as GPIO
import time
import math
import smbus
from motor import motor
from Adafruit_I2C import Adafruit_I2C
from pizypwm import *


def init(shared,mymotor):
  neutralESC = 35
  shared.set('neutralESC', neutralESC)
  shared.set('Turn', 0)
  shared.set('Random', 0)
  shared.set('Way', neutralESC)
  shared.set('accError',0)
  shared.set('srf02Error',0)
  shared.set('i2cSRF02Power',1)
  shared.set('i2cAccPower',0)

  mymotor.start()
  mymotor.setW(100)
  time.sleep(2)
  mymotor.setW(neutralESC)

  # Set Pin 11 as Output
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(11, GPIO.OUT)


def running(shared,mymotor):
  # Start PWM with 50Hz on Pin 11
  Servo = PiZyPwm(50, 11, GPIO.BOARD)

  if shared.get('Turn') == 1:
    side = 10
    increment = 20
    servoCtl(Servo,side,increment)
    shared.set('Turn', 0)

  if shared.get('Turn') == -1:
    side = 5
    increment = 20
    servoCtl(Servo,side,increment)
    shared.set('Turn', 0)

  speedValue = shared.get('Way')
  speedValue = max(speedValue,0)
  speedValue = min(speedValue,100)
  mymotor.setW(speedValue) 


def servoCtl(Servo,side,increment):
    # Generate PWM with 10% Dutycycle (2ms)
    Servo.start(side)
    for Counter in range(int(increment)):
            time.sleep(0.001)

    # PWM stop
    Servo.stop()
    GPIO.cleanup()


def i2csensor(shared):
  lsm = Adafruit_LSM303()

  if shared.get('i2cAccPower'):
    try:
      accResult, magResult = lsm.read()
    except:
      shared.set('accError',shared.get('accError')+1)
    time.sleep(0.1)
    shared.set('accX',accResult[0])
    shared.set('accY',accResult[1])
    shared.set('accZ',accResult[2])
    shared.set('capMag',magResult[3])

def i2csensor(shared):
  i2c = smbus.SMBus(1)
  adress = (0x71,0x72,0x73,0x75,0x76,0x77)
  mode    = 81      # centimetres

  if shared.get('i2cSRF02Power'):
    for srf02Adress in adress:
      try:
        i2c.write_byte_data(srf02Adress, 0, mode) # lance un "ping" en centimetre
        dst = i2c.read_word_data(srf02Adress, 2) / 255
        shared.set('%s'%hex(srf02Adress),dst)
      except:
        shared.set('srf02Error',shared.get('srf02Error')+1)
      time.sleep(0.1)


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
  mymotor = motor('m1', 24, simulation=False)
 
  while shared.get('RpiPower') != 0:
    shared.set('RpiPower', 0)
    time.sleep(1)

  init(shared,mymotor)

  while shared.get('RpiPower') == 0:
    running(shared,mymotor)
    i2csensor(shared)

