#define DEBUG 1
#define EDF
#define SNMP

/**
* Agentuino SNMP Agent Library Prototyping...
*
* Copyright 2010 Eric C. Gionet <lavco_eg@hotmail.com>
*
*/
#include <Streaming.h>         // Include the Streaming library
#include <Ethernet.h>          // Include the Ethernet library
#include <SPI.h>
#include <MemoryFree.h>
#include <Agentuino.h> 
#include <Flash.h>
#include <SoftwareSerial.h>
//
#define DEBUG 1
//

//int dht22XXX    = 0; 
//int dht22YYY    = 1; 
int dht22OldPin = 2; 
int EDFRxPin    = 3;
int ETHERNET_RESERVED_PIN1 = 4;
int EDFTxPin    = 5;
//int relayPin    = 5; 
//int resetPin    = 6; 
int dht22NewPin = 7;
int dht22ExtPin = 8; 
int flowPin     = 9; 
int ETHERNET_RESERVED_PIN2 = 10;
int ETHERNET_RESERVED_PIN3 = 11;
int ETHERNET_RESERVED_PIN4 = 12;

#ifdef EDF
#include <edf.h>
SoftwareSerial edfSerial(EDFRxPin, EDFTxPin);
Teleinfos teleinfos;
#endif

static byte mac[] = { 0x90, 0xA2, 0xDA, 0x0E, 0x0C, 0x4A };
static byte ip[] = { 192, 168, 1, 99 };
static byte gateway[] = { 192, 168, 1, 254 };
static byte subnet[] = { 255, 255, 255, 0 };
static byte leroux_dns[] = { 192, 168, 1, 254 };

static char sysDescr[] PROGMEM      = "1.3.6.1.2.1.1.1.0";  // read-only  (DisplayString)
static char const oidEDFIndexNormal[] PROGMEM = "1.3.6.1.4.1.36582.20";
static char const oidEDFIndexPointe[] PROGMEM = "1.3.6.1.4.1.36582.21";

static char locDescr[]              = "Agentuino, a light-weight SNMP Agent.";  // read-only (static)

uint32_t prevMillis = millis();
char oid[SNMP_MAX_OID_LEN];
SNMP_API_STAT_CODES api_status;
SNMP_ERR_CODES status;

#ifdef SNMP
void pduReceived()
{
  SNMP_PDU pdu;
  //
  #ifdef DEBUG
    Serial << F("UDP Packet Received Start..") << F(" RAM:") << freeMemory() << endl;
  #endif
  //
  api_status = Agentuino.requestPdu(&pdu);
  //
  if ( pdu.type == SNMP_PDU_GET || pdu.type == SNMP_PDU_GET_NEXT || pdu.type == SNMP_PDU_SET
    && pdu.error == SNMP_ERR_NO_ERROR && api_status == SNMP_API_STAT_SUCCESS ) {
    //
    pdu.OID.toString(oid);
    //
    //Serial << "OID: " << oid << endl;
    //
    if ( strcmp_P(oid, sysDescr ) == 0 ) {
      // handle sysDescr (set/get) requests
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } else {
        // response packet from get-request - locDescr
        status = pdu.VALUE.encode(SNMP_SYNTAX_OCTETS, locDescr);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
      //
      #ifdef DEBUG
        Serial << F("sysDescr...") << locDescr << F(" ") << pdu.VALUE.size << endl;
      #endif
    } else if (strcmp_P(oid, oidEDFIndexNormal ) == 0) {
      Serial << "oidEDFIndexNormal" << endl;
      if ( pdu.type == SNMP_PDU_SET ) {
          // response packet from set-request - object is read-only
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
      } else {
#ifdef EDF
        Serial << "getTeleinfo begin" << endl;
        int ok  = teleinfos.read(edfSerial, Serial);
        Serial << ok  << endl;
        if (!ok)  { 
//          Serial << "getTeleinfo timedout" << endl;
          status = SNMP_ERR_READ_ONLY;
        } else {
          Serial << teleinfos.EJPHN << endl;
          status = pdu.VALUE.encode(SNMP_SYNTAX_COUNTER, teleinfos.EJPHN);
        }
        pdu.error = status;
#endif
#ifndef EDF
        pdu.error = SNMP_ERR_READ_ONLY;
#endif
        pdu.type = SNMP_PDU_RESPONSE;
      }
    }  else {      // oid does not exist
      //
      // response packet - object not found
      pdu.type = SNMP_PDU_RESPONSE;
      pdu.error = SNMP_ERR_NO_SUCH_NAME;
    }
    //
    Agentuino.responsePdu(&pdu);
  }
  //
  Agentuino.freePdu(&pdu);
  //
  //Serial << "UDP Packet Received End.." << " RAM:" << freeMemory() << endl;
}
#endif

void setup()
{
  Serial.begin(1200);
#ifdef EDF
  edfSerial.begin(1200);
#endif 
  Ethernet.begin(mac, ip, leroux_dns, gateway, subnet);
  //
#ifdef SNMP
  api_status = Agentuino.begin();
  //
  if ( api_status == SNMP_API_STAT_SUCCESS ) {
    //
    Agentuino.onPduReceive(pduReceived);
    //
    delay(10);
    //
    Serial << F("SNMP Agent Initalized...") << endl;
    //
    return;
  }
  //
  delay(10);
  //
  Serial << F("SNMP Agent Initalization Problem...") << status << endl;
#endif
}

void loop()
{
  // listen/handle for incoming SNMP requests
  #ifdef SNMP
  Agentuino.listen();
  #endif
  #ifndef SNMP
  Serial << "getTeleinfos begin " << endl;
  int ok  = teleinfos.read(edfSerial, Serial);
  if (!ok)  { 
    Serial << "getTeleinfo timedout" << endl;
  } else {
    Serial << "getTeleinfo complete in " << ok << endl;
    Serial << teleinfos.EJPHN << endl;
  }
  #endif

}
