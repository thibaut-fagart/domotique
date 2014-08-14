#! /usr/bin/env python
import os, sys, re


#========== Programme principal =============
if __name__ == "__main__":

  print "starting script"

  rep = os.popen( 'ls ').read().split()
  for l1 in rep:
    i = 0
    repname = l1.split('-',1)[-1]
    fich = os.popen( 'ls %s' % l1 ).read().split()
    for l2 in fich:
      if (l2.split('.')[-1] == 'jpg' or l2.split('.')[-1] == 'JPG'):
        os.popen( 'mv %s/%s %s/%s-%04i.jpg' % (l1,l2,l1,repname,i))
        i = i+1

  print "script ended"
