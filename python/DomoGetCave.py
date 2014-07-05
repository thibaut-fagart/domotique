#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import httplib

def get_dth22Ethernet(Host,Port):
    httpServ= httplib.HTTPConnection(Host, Port )
    httpServ.request("GET", "/index.html")
    reponse = httpServ.getresponse().read()
    httpServ.close()
    return reponse

#========== Programme principal =============
if __name__ == '__main__':

  caveHost = '192.168.0.60'
  cavePort = '999'

  print get_dth22Ethernet(caveHost,cavePort)
