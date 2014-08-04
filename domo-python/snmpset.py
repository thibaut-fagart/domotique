#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

cmdGen = cmdgen.CommandGenerator()

############### manage 

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public', mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    '1.3.6.1.4.1.36582.31'
)
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
            print('curent %s = %s' % (name.prettyPrint(), val.prettyPrint()))


if val == 1:
  setval = 0
else:
  setval = 1

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    ('1.3.6.1.4.1.36582.31', rfc1902.Integer(setval)),
)

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
            print('set %s = %s' % (name.prettyPrint(), val.prettyPrint()))

############### manage 

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public', mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    '1.3.6.1.4.1.36582.32'
)
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
            print('curent %s = %s' % (name.prettyPrint(), val.prettyPrint()))


if val == 1:
  setval = 0
else:
  setval = 1

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    ('1.3.6.1.4.1.36582.32', rfc1902.Integer(setval)),
)

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
            print('set %s = %s' % (name.prettyPrint(), val.prettyPrint()))

############### manage 

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public', mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    '1.3.6.1.4.1.36582.33'
)
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
            print('curent %s = %s' % (name.prettyPrint(), val.prettyPrint()))


if val == 1:
  setval = 0
else:
  setval = 1

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    ('1.3.6.1.4.1.36582.33', rfc1902.Integer(setval)),
)

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
            print('set %s = %s' % (name.prettyPrint(), val.prettyPrint()))
