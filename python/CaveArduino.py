#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import time
import httplib

CaveHost = '192.168.0.60'
CavePort = '999'

def get_dth22Ethernet(Host,Port):
   httpServ= httplib.HTTPConnection(Host, Port )
   httpServ.request("GET", "/index.html")
   reponse = httpServ.getresponse().read().split(':End:')

   for rep in reponse:
       if (rep.split(':')[0] == 'DHT'):
          print 'temp = ', float(rep.split(':')[2])
          print 'hum = ', float(rep.split(':')[4])
       if (rep.split(':')[0] == 'Error'):
          print 'temp = 999.9'
          print 'hum = 999.9'
       if (rep.split(':')[0] == 'PIR'):
          print 'presence = ', int(rep.split(':')[2])

   httpServ.close()

#========== Programme principal =============
if __name__ == '__main__':

  get_dth22Ethernet(CaveHost,CavePort)

