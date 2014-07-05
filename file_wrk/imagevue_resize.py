#! /usr/bin/env python
import os, sys, re


#========== Programme principal =============
if __name__ == "__main__":

    print "starting script"

    fich1 = os.popen( 'ls').read().split()
    os.popen( 'mkdir _altimage')
    for l2 in fich1:
       try:
          if l2.split('.')[1] == 'jpg' or l2.split('.')[1] == 'JPG':
             os.popen( 'cp %s _altimage/' % l2 )
             print ("copy of %s in _altimage done" % (l2))
             os.popen( 'convert %s -resize 1024x1024 -quality 100  %s' % (l2,l2) )
             print ("converting %s in current folder done" % (l2))
       except:
          continue

    print "script ended"
