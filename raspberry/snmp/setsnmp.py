#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

def setSnmp(host,oid,value):
  cmdGen = cmdgen.CommandGenerator()

  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
      cmdgen.CommunityData('private', mpModel=0),
      cmdgen.UdpTransportTarget((host, 161)),
      (oid, rfc1902.Integer(value)),
  )

  # Check for errors and print out results
  if errorIndication:
      print(errorIndication)
      return False
  else:
      if errorStatus:
          print('%s at %s' % (
              errorStatus.prettyPrint(),
              errorIndex and varBinds[int(errorIndex)-1] or '?'
              )
          )
          return False
      else:
          for name, val in varBinds:
              return True

