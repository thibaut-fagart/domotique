#!/usr/bin/env python

import os, time

def printlog(text):
  fileToBeWriten = "/home/dimi/prog/ftpScript/ftpLog.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()

def readlog():
  fileLog = "/home/dimi/prog/ftpScript/ftpLog.txt"
  fichierRead = open(fuelFileData,'r')
  logLine = fichierRead.read()
  fileReadWrite.close()
  return logLine

if __name__ == "__main__":
  ftpState = os.popen('/usr/sbin/pure-ftpwho -s')
  while 1:
    loggedFtp = ftpState.readline()
    if not loggedFtp: 
      break
    else:
      loggedFtp = loggedFtp.split('|')
      userFtp     = loggedFtp[1]
      timeDwnld   = loggedFtp[2]
      actionFtp   = loggedFtp[3]
      fileFtp     = loggedFtp[4]
      ipFtp       = loggedFtp[5]
      destFtp     = loggedFtp[6]
      portFtp     = loggedFtp[7]
      currentSize = loggedFtp[8]
      totalSize   = loggedFtp[9]
      percentFtp  = loggedFtp[10]
      speedFtp    = loggedFtp[11].split()[0]

      printlog(time.asctime())
      printlog('%s %s %s from %s at speed %s K/s : %s percent done'%(userFtp, actionFtp, fileFtp, ipFtp, speedFtp, percentFtp))
 
