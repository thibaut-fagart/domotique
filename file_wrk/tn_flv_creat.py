#! /usr/bin/env python
import os, sys, re, sys


#========== Programme principal =============
if __name__ == "__main__":

    print "starting script \n"

    fich1 = os.popen( 'ls').read().split()
    if sys.argv[1] == 'create':
      for l2 in fich1:
        try:
          if l2.split('_')[0] == 'mov':
            num = l2.split('_')[1]
            os.popen('ffmpeg -y -ss 00:00:01.00 -t 1 -b 15000kb -i mov_%s -f mjpeg Screenshot-mov_%s.flv-1.png'%(num,num.split('.')[0]))
            print "creat Screenshot-mov_%s.flv-1.png" % num.split('.')[0] 
        except:
          continue
    if sys.argv[1] == 'modify':
      for l2 in fich1:
        try:
          if l2.split('_')[1] == 'mov':
            num = l2.split('_')[2]
            os.popen( 'rm tn_mov_%s' % num )
            print "rm tn_mov_%s" % num 
            os.popen( 'mv tn_Screenshot-mov_%s.flv-1.jpg tn_mov_%s' % (num.split('.')[0],num) )
            os.popen( 'rm Screenshot-mov_%s.flv-1.png' % (num.split('.')[0]) )
            print "mv tn_Screenshot-mov_%s.flv-1.jpg tn_mov_%s" % (num.split('.')[0],num)
            print "rm Screenshot-mov_%s.flv-1.jpg" % (num.split('.')[0])
        except:
          continue

    print "script ended \n"
