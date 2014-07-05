#! /usr/bin/env python
import os, sys, re


#========== Programme principal =============
if __name__ == "__main__":

  print "starting script"
  i = 0

  rep = os.popen( 'ls').read().split()
  for l1 in rep:
    i = i+1
    os.popen( 'mv %s negatif_%03i.jpg' % (l1,i) )
    print 'move %s negatif_%03i.jpg' % (l1,i)

  print "script ended"
