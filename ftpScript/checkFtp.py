#!/usr/bin/env python

import os, time
from setsnmp import setSnmp

ipHostSnmp   = "192.168.0.103"
user1        = "step"
oidUser1     = "1.3.6.1.4.1.43689.2.1.0"
user2        = "magritte"
oidUser2     = "1.3.6.1.4.1.43689.2.2.0"
user3        = "tom"
oidUser3     = "1.3.6.1.4.1.43689.2.3.0"
user4        = "thib"
oidUser4     = "1.3.6.1.4.1.43689.2.4.0"
user5        = "gregoire"
oidUser5     = "1.3.6.1.4.1.43689.2.5.0"

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

      if userFtp == user1:
        resultSetUser = setSnmp(ipHostSnmp,oidUser1,int(speedFtp))
      if userFtp == user2:
        resultSetUser = setSnmp(ipHostSnmp,oidUser2,int(speedFtp))
      if userFtp == user3:
        resultSetUser = setSnmp(ipHostSnmp,oidUser3,int(speedFtp))
      if userFtp == user4:
        resultSetUser = setSnmp(ipHostSnmp,oidUser4,int(speedFtp))
      if userFtp == user5:
        resultSetUser = setSnmp(ipHostSnmp,oidUser5,int(speedFtp))
 
