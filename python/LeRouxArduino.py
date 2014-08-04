#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import time
import httplib

# LeRouxHost = '192.168.1.99'
LeRouxHost = '109.190.53.51'
LeRouxPort = '999'

def get_dth22Ethernet(Host,Port):
   httpServ= httplib.HTTPConnection(Host, Port )
   httpServ.request("GET", "/index.html")
   reponse = httpServ.getresponse().read().split(':End:')

   print reponse[0].split(':')
   print reponse[1].split(':')
   print reponse[2].split(':')

   httpServ.close()

def set_Ethernet(Host,Port,command):
   httpServ= httplib.HTTPConnection(Host, Port )
   httpServ.request(command, "")
   reponse = httpServ.getresponse().read()

   print reponse
   
   httpServ.close()
   
#========== Programme principal =============
if __name__ == '__main__':

   set_Ethernet(LeRouxHost,LeRouxPort,"START"+'1')

