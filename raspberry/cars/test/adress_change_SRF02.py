#!/usr/bin/python

import smbus

bus = smbus.SMBus(1)

currentDeviceAddress = 0x70
commandRegister = 0x00
changeCommand1 = 0xA0
changeCommand2 = 0xAA
changeCommand3 = 0xA5
changeAddressTo = 0xEE

bus.write_byte_data(currentDeviceAddress, commandRegister, changeCommand1)
bus.write_byte_data(currentDeviceAddress, commandRegister, changeCommand2)
bus.write_byte_data(currentDeviceAddress, commandRegister, changeCommand3)
bus.write_byte_data(currentDeviceAddress, commandRegister, changeAddressTo)
