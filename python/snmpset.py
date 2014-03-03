#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('private', mpModel=0),
    cmdgen.UdpTransportTarget(('192.168.0.70', 161)),
    #('1.3.6.1.4.1.36582.33', rfc1902.Integer(1)),
    ('1.3.6.1.4.1.36582.33', rfc1902.Integer(1)),
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
