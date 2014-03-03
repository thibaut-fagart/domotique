#! /usr/bin/env python
import os, sys, re
import shutil

fich1=os.popen('ls').read().split('\n')
for l1 in fich1:
    l1elem=l1.split('-')
    if l1elem[2] == 'Cd2':
      l2=str(int(l1elem[0])+34)+'-Piste-Cd2-'+l1elem[0]+'.mp3'
      shutil.copyfile(l1,l2)
