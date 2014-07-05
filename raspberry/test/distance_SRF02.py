#!/usr/bin/python

import smbus, time
i2c = smbus.SMBus(1)

adress = (0x71,0x72,0x73,0x75,0x76,0x77)
mode    = 81      # centimetres

while True:
  for i in adress:
    try:
      i2c.write_byte_data(i, 0, mode) # lance un "ping" en centimetre
      dst = i2c.read_word_data(i, 2) / 255 
      res = 'cm'
      print '%s : '%hex(i),dst,' ',res
    except:
      print '%s : '%hex(i),' None'
    time.sleep(0.1)
