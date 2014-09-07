#!/usr/bin/env python

from pysphere import VIServer
import paramiko,time

exsi_ip = '192.168.0.4'
exsi_user = 'root'
exsi_pass = 'akiko.104'

www_ip = '192.168.0.103'
www_user = 'dimi'
www_pass = 'akiko.103'

def printlog(text):
  fileToBeWriten = "/home/dimi/prog/exsi/exsi_reboot.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()

server = VIServer()
server.connect(exsi_ip, exsi_user, exsi_pass)

vms = server.get_registered_vms()

vm = server.get_vm_by_path(vms[0])

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
  ssh.connect(www_ip, username=www_user, password=www_pass)
except:
  printlog(time.asctime())
  printlog('----------------------------')
  printlog('ssh down, trying to reboot www vm')
  vm.power_off()
  vm.power_on()
  printlog(vm.get_property('name',from_cache=False))
  printlog(vm.get_status())


server.disconnect()

if ssh:
  ssh.close()
