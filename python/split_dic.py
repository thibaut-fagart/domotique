#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, re, glob
import pickle
import datetime

path = 'data_new'

fileList = glob.glob(os.path.join(path,"sensor*.dat"))
fileList.sort()

data = {}
for i in fileList:
  fichierRead = open(i,'rb')
  dataOld = pickle.load(fichierRead)
  fichierRead.close()
  data.update(dataOld)

for n in range(17):
  data_new = {}
  beg_time = (datetime.datetime(2013, 06, 02) + datetime.timedelta(days=7*n)).strftime("%Y-%m-%d-%H-%M-%S")
  end_time = (datetime.datetime(2013, 06, 02) + datetime.timedelta(days=7*n+7)).strftime("%Y-%m-%d-%H-%M-%S")
  
  for j in data:
    if (j > beg_time) and (j < end_time):
      data_new[j]=data[j]
  
  fileYear  = int(beg_time.split('-')[0])
  fileMonth = int(beg_time.split('-')[1])
  fileDay   = int(beg_time.split('-')[2])

  fileToBeCreat = 'Sensor_%i_%02i_%02i.dat'%(fileYear,fileMonth,fileDay)
  print fileToBeCreat
  fichierWrite = open(os.path.join(path,fileToBeCreat),'w+b')
  pickle.dump(data_new,fichierWrite)
  fichierWrite.close()
