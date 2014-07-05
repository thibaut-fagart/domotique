#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from readDht import readDht

dhtpin = int(4)
oidDht22SalonTemp = "1.3.6.1.4.1.43689.1.1.2.4.1.0"
oidDht22SalonHum = "1.3.6.1.4.1.43689.1.1.2.4.2.0"
ipHostSnmp        = "192.168.0.110"

if __name__ == "__main__":

  readDht(ipHostSnmp,oidDht22SalonTemp,oidDht22SalonHum,dhtpin)

