#! /usr/bin/env python
import os, sys, re


#========== Programme principal =============
if __name__ == "__main__":

  text = '.jpg'

  print "starting script"

  rep = os.popen( 'ls').read().split()
  for l1 in rep:
    fich = l1.split(text)
    os.popen( 'mv %s %s.jpg' % (l1,fich[0]) )

  print "script ended"
