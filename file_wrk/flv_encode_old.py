#! /usr/bin/env python
import os, sys, re


#========== Programme principal =============
if __name__ == "__main__":

    print "starting script"

    try:
       os.system( 'mkdir flv' )
       print "flv created"
    except:
       print "flv already created"

    fich1 = os.popen( 'ls IMG_*.MOV').read().split()

    for l2 in fich1:
       fich_int = l2.split('IMG_')[1]
       fich_main = fich_int.split('.MOV')[0]
       os.system( 'mv IMG_%s.MOV mov_%s.mov' % (fich_main, fich_main) )

    fich2 = os.popen( 'ls *.mov').read().split()

    for l2 in fich2:
       convert = 1
       try:
          if convert:
            test = l2.split('rs')[1]
            fich_main = l2.split('rs')[0]
            print "converting ",fich_main,".mov to ",fich_main,".flv"
            #os.system('touch flv/%s.flv'%fich_main)
            os.system( 'ffmpeg -i %srs.mov -f flv -s 640*480 -sameq -vf transpose=1 flv/%s.flv' % (fich_main, fich_main) )
            convert = 0
       except:
          buff = 1
       try:
          if convert:
            test = l2.split('is')[1]
            fich_main = l2.split('is')[0]
            print "converting ",fich_main,".mov to ",fich_main,".flv"
            #os.system('touch flv/%s.flv'%fich_main)
            os.system( 'ffmpeg -i %sis.mov -f flv -s 640*480 -sameq -vf transpose=2 flv/%s.flv' % (fich_main, fich_main) )
            convert = 0
       except:
          buff = 1
       try:
          if convert:
            test = l2.split('s')[1]
            fich_main = l2.split('s')[0]
            print "converting ",fich_main,".mov to ",fich_main,".flv"
            #os.system('touch flv/%s.flv'%fich_main)
            os.system( 'ffmpeg -i %ss.mov -f flv -s 640*480 -sameq flv/%s.flv' % (fich_main, fich_main) )
            convert = 0
       except:
          buff = 1
       try:
          if convert:
            test = l2.split('r')[1]
            fich_main = l2.split('r')[0]
            print "converting ",fich_main,".mov to ",fich_main,".flv"
            #os.system('touch flv/%s.flv'%fich_main)
            #os.system( 'ffmpeg -i %sr.mov -f flv -s 640*360 -sameq -vf transpose=1 flv/%s.flv' % (fich_main, fich_main) )
            os.system( 'ffmpeg -i %sr.mov -f flv -s 960*540 -sameq -vf transpose=1 flv/%s.flv' % (fich_main, fich_main) )
            convert = 0
       except:
          buff = 1
       try:
          if convert:
            test = l2.split('l')[1]
            fich_main = l2.split('l')[0]
            print "converting ",fich_main,".mov to ",fich_main,".flv"
            #os.system('touch flv/%s.flv'%fich_main)
            #os.system( 'ffmpeg -i %sl.mov -f flv -s 640*360 -sameq -vf transpose=3 flv/%s.flv' % (fich_main, fich_main) )
            os.system( 'ffmpeg -i %sl.mov -f flv -s 960*540 -sameq -vf transpose=3 flv/%s.flv' % (fich_main, fich_main) )
            convert = 0
       except:
          buff = 1
       try:
          if convert:
            test = l2.split('i')[1]
            fich_main = l2.split('i')[0]
            print "converting ",fich_main,".mov to ",fich_main,".flv"
            #os.system('touch flv/%s.flv'%fich_main)
            #os.system( 'ffmpeg -i %si.mov -f flv -s 640*360 -sameq -vf vflip flv/%s.flv' % (fich_main, fich_main) )
            os.system( 'ffmpeg -i %si.mov -f flv -s 960*540 -sameq -vf vflip flv/%s.flv' % (fich_main, fich_main) )
            convert = 0
       except:
          if convert:
            fich_main = l2.split('.')[0]
            print "converting ",fich_main,".mp4 to ",fich_main,".flv"
            #os.system('touch flv/%s.flv'%fich_main)
            #os.system( 'ffmpeg -i %s.mov -f flv -s 640*360 -sameq flv/%s.flv' % (fich_main, fich_main) )
            os.system( 'ffmpeg -i %s.mov -f flv -s 960*540 -sameq flv/%s.flv' % (fich_main, fich_main) )
            convert = 0


    print "script ended"
