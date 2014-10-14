#!/usr/bin/python
import time
import pcapy
import impacket.ImpactDecoder as Decoders
import impacket.ImpactPacket as Packets
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

ipHostSnmp      = "192.168.0.110"
ipSqueezCenter  = "192.168.0.103"
ipSqueezChambre = "192.168.0.5"
ipSqueezSalon   = "192.168.0.6"
ipSqueezSdb     = "192.168.0.7"
ipSqueezCuisine = "192.168.0.8"
oidAmpliSalonState   = "1.3.6.1.4.1.43689.1.1.1.0"
oidAmpliSdbState     = "1.3.6.1.4.1.43689.1.1.2.0"
oidAmpliCuisineState = "1.3.6.1.4.1.43689.1.1.3.0"
oidAmpliChambreState = "1.3.6.1.4.1.43689.1.1.4.0"

def printlog(datelog,text):
  fileToBeWriten = "/home/dimi/prog/log/audio_packet_check_log.txt"
  fichierWrite = open(fileToBeWriten,'a')
  fichierWrite.write(datelog)
  fichierWrite.write(text)
  fichierWrite.write('\n')
  fichierWrite.close()  

def set_Value(Oid,ipHostSnmp,value):
  errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
      cmdgen.CommunityData('private',mpModel=0),
      cmdgen.UdpTransportTarget((ipHostSnmp, 161)),
      (Oid, rfc1902.Integer(value)))
  printlog(time.asctime(),'set oid %s from %s to %s value \n'%(Oid,ipHostSnmp,value))

  # Check for errors and print out results
  if errorIndication:
    printlog(time.asctime(),'get oid %s from %s errorIndication : %s \n'%(Oid,ipHostSnmp,errorIndication))
  else:
    if errorStatus:
      printlog(time.asctime(),'get oid %s from %s errorStatus : %s at %s \n'%(Oid,ipHostSnmp,errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
    else:
      for name, val in varBinds:
        #printlog('get oid %s from %s : %s = %s'%(Oid,ipHostSnmp,name.prettyPrint(), val.prettyPrint()))
        return val

def main():
  
  lastTime = 0
  audioMaxDelay = 300
  audioCurrentDelay = 0
  deltaTime = 2
  audioChambrePower = 0
  audioCuisinePower = 0
  audioSalonPower   = 0
  audioSdbPower     = 0

  lastPacketCuisine = int(time.time()) - audioMaxDelay
  lastPacketChambre = int(time.time()) - audioMaxDelay
  lastPacketSalon   = int(time.time()) - audioMaxDelay
  lastPacketSdb     = int(time.time()) - audioMaxDelay

  print 'Opening eth0'

  cap = pcapy.open_live('eth0', 5000, 1, 1000)
  cap.setfilter('src host 192.168.0.103 and port 9000')
  eth_decoder = Decoders.EthDecoder()
  ip_decoder = Decoders.IPDecoder()

  while (True):
    try:
      (header, payload) = cap.next()
    except:
      continue

    ethernet = eth_decoder.decode(payload)
    if ethernet.get_ether_type() == Packets.IP.ethertype:
      ip = ip_decoder.decode(payload[ethernet.get_header_size():])
      ip_src = ip.get_ip_src()
      ip_dst = ip.get_ip_dst()
      if (header.getlen() > 100):
        if (ip_src == ipSqueezCenter and ip_dst == ipSqueezCuisine):
          lastPacketCuisine = int(time.time())
        if (ip_src == ipSqueezCenter and ip_dst == ipSqueezChambre):
          lastPacketChambre = int(time.time())
        if (ip_src == ipSqueezCenter and ip_dst == ipSqueezSalon):
          lastPacketSalon = int(time.time())
        if (ip_src == ipSqueezCenter and ip_dst == ipSqueezSdb):
          lastPacketSdb = int(time.time())

	if ((int(time.time()) - lastTime) > deltaTime):
	# audioCurrentDelay indicate the time since the last packet received
            audioCurrentDelay = max((int(time.time()) - lastPacketChambre), audioCurrentDelay)  
            audioCurrentDelay = max((int(time.time()) - lastPacketCuisine), audioCurrentDelay)  
            audioCurrentDelay = max((int(time.time()) - lastPacketSalon)  , audioCurrentDelay) 
            audioCurrentDelay = max((int(time.time()) - lastPacketSdb)    , audioCurrentDelay) 

            lastAudioChambrePower = audioChambrePower
            lastAudioCuisinePower = audioCuisinePower
            lastAudioSalonPower   = audioSalonPower
            lastAudioSdbPower     = audioSdbPower

            audioChambrePower = ((int(time.time()) - lastPacketChambre) < audioMaxDelay)
            audioCuisinePower = ((int(time.time()) - lastPacketCuisine) < audioMaxDelay)
            audioSalonPower   = ((int(time.time()) - lastPacketSalon)   < audioMaxDelay)
            audioSdbPower     = ((int(time.time()) - lastPacketSdb)     < audioMaxDelay)
	
	    if lastAudioCuisinePower != audioCuisinePower:
                set_Value(oidAmpliCuisineState,ipHostSnmp,audioCuisinePower)
	    if lastAudioChambrePower != audioChambrePower:
                set_Value(oidAmpliChambreState,ipHostSnmp,audioChambrePower)
	    if lastAudioSalonPower != audioSalonPower:
                set_Value(oidAmpliSalonState,ipHostSnmp,audioSalonPower)
	    if lastAudioSdbPower != audioSdbPower:
                set_Value(oidAmpliSdbState,ipHostSnmp,audioSdbPower)
		
            lastTime = int(time.time())
	
if __name__ == "__main__":
  time.sleep(30)
  main()
