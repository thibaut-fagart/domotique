#!/usr/bin/python 
from IOPi import IOPI
import time,sys

bus1 = IOPI(0x20)
bus2 = IOPI(0x21)

bus1.setPortDirection(0, 0x00)
bus1.setPortDirection(1, 0x00)
bus2.setPortDirection(0, 0x00)
bus2.setPortDirection(1, 0x00)

bus1.writePin(2, 0)
bus1.writePin(4, 0)
bus1.writePin(6, 0)
bus1.writePin(8, 0)

bus1.writePin(1, int(sys.argv[1]))  # cuisine
bus1.writePin(3, int(sys.argv[1]))  # chambre
bus1.writePin(5, 1)  # vmc
bus1.writePin(7, int(sys.argv[1]))  # sdb
