#! /usr/bin/env python
import os, sys, re



#========== Programme principal =============
if __name__ == "__main__":

    print "starting script"

    fich2 = os.popen( 'ls *.mov').read().split()

    for l2 in fich2:
       print "converting ",l2.split(".mov")[0],".mov to ", l2.split(".mov")[0],".flv"
       os.system( 'avconv -i %s.mov -ar 44100 -b 20000k %s.flv'%(l2.split(".mov")[0],l2.split(".mov")[0]))

    print "script ended"

