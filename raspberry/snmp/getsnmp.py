#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

def getSnmp(host,oid):
  cmdGen = cmdgen.CommandGenerator()

  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
      cmdgen.CommunityData('public', mpModel=0),
      cmdgen.UdpTransportTarget((host, 161)),
      oid
<<<<<<< HEAD
  )
=======
  )   
>>>>>>> dcaf78ac9ef7feb55fad2e8d646d024ee83885e6
  # Check for errors and print out results
  if errorIndication:
      print(errorIndication)
  else:
      if errorStatus:
          print('%s at %s' % (
              errorStatus.prettyPrint(),
              errorIndex and varBinds[int(errorIndex)-1] or '?'
              )
          )
      else:
          for name, val in varBinds:
              return name.prettyPrint(), val.prettyPrint()
<<<<<<< HEAD
=======

>>>>>>> dcaf78ac9ef7feb55fad2e8d646d024ee83885e6
