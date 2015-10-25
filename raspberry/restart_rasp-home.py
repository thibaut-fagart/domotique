#!/usr/bin/env python

import paramiko,time

ref_ip = '192.168.0.4'
ref_user = 'root'
ref_pass = 'akiko.104'

def printlog(text):
  fileToBeWriten = "/home/dimi/prog/raspberry/rasp-home_reboot.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
  ssh.connect(ref_ip, username=ref_user, password=ref_pass)
  #print "ssh up"
except:
  printlog(time.asctime())
  printlog('----------------------------')
  printlog('ssh rasp-home down (or exsi?), trying to reboot rasp-home')
  # ask raspberry to reboot
  #print "ssh down"

if ssh:
  ssh.close()
  #print "ssh closed"
