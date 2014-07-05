#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    cmdgen.CommunityData('private',mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    ('1.3.6.1.4.1.36582.15', rfc1902.Integer(1))
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
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    cmdgen.CommunityData('private',mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    ('1.3.6.1.4.1.36582.16', rfc1902.Integer(1))
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
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    cmdgen.CommunityData('private',mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    ('1.3.6.1.4.1.36582.40', rfc1902.Integer(0))
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
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

