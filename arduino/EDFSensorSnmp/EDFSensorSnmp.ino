/*
reserved pins
 ethernet shield : 4 10 11 12 13
 
 */

#define DEBUG 0
#define EDF
//#define SNMP


#include <DHT.h>
#include <Streaming.h>         
#include <Ethernet.h>         
#include <SPI.h>
#include <MemoryFree.h>
#include <Flash.h>
#include <SoftwareSerial.h>
#include <Agentuino.h> 
#include <snmp_utils.h>

static byte mac[] = { 0x00, 0x06, 0x66, 0x50, 0xA4, 0x29 };
static byte ip[] = { 192, 168, 0, 75 };
static byte gateway[] = { 192, 168, 0, 254 };
static byte subnet[] = { 255, 255, 255, 0 };
static byte edf_dns[] = { 192, 168, 0, 254 };

#define DHTTYPE DHT22 // DHT 22 (AM2302)

int dhtEdfPin   = 4;  // DHT22 EDF
int EDFRxPin    = 9;
int EDFTxPin    = 8;

int ETHERNET_RESERVED_PIN2 = 10;
int ETHERNET_RESERVED_PIN3 = 11;
int ETHERNET_RESERVED_PIN4 = 12;

#ifdef EDF
#include <edf.h>
SoftwareSerial edfSerial(EDFRxPin, EDFTxPin);
Teleinfos teleinfos;
#endif

DHT dht_Edf(dhtEdfPin, DHTTYPE);

//
// tkmib - linux mib browser
//
// RFC1213-MIB OIDs
// .iso (.1)
// .iso.org (.1.3)
// .iso.org.dod (.1.3.6)
// .iso.org.dod.internet (.1.3.6.1)
// .iso.org.dod.internet.mgmt (.1.3.6.1.2)
// .iso.org.dod.internet.mgmt.mib-2 (.1.3.6.1.2.1)
// .iso.org.dod.internet.mgmt.mib-2.system (.1.3.6.1.2.1.1)
// .iso.org.dod.internet.mgmt.mib-2.system.sysDescr (.1.3.6.1.2.1.1.1)
static char const sysDescr[] PROGMEM      = "1.3.6.1.2.1.1.1.0";  // read-only  (DisplayString)
// .iso.org.dod.internet.mgmt.mib-2.system.sysObjectID (.1.3.6.1.2.1.1.2)
static char const sysObjectID[] PROGMEM   = "1.3.6.1.2.1.1.2.0";  // read-only  (ObjectIdentifier)
// .iso.org.dod.internet.mgmt.mib-2.system.sysUpTime (.1.3.6.1.2.1.1.3)
static char const sysUpTime[] PROGMEM     = "1.3.6.1.2.1.1.3.0";  // read-only  (TimeTicks)
// .iso.org.dod.internet.mgmt.mib-2.system.sysContact (.1.3.6.1.2.1.1.4)
static char const sysContact[] PROGMEM    = "1.3.6.1.2.1.1.4.0";  // read-write (DisplayString)
// .iso.org.dod.internet.mgmt.mib-2.system.sysName (.1.3.6.1.2.1.1.5)
static char const sysName[] PROGMEM       = "1.3.6.1.2.1.1.5.0";  // read-write (DisplayString)
// .iso.org.dod.internet.mgmt.mib-2.system.sysLocation (.1.3.6.1.2.1.1.6)
static char const sysLocation[] PROGMEM   = "1.3.6.1.2.1.1.6.0";  // read-write (DisplayString)
// .iso.org.dod.internet.mgmt.mib-2.system.sysServices (.1.3.6.1.2.1.1.7)
static char const sysServices[] PROGMEM   = "1.3.6.1.2.1.1.7.0";  // read-only  (Integer)
//
// Arduino defined OIDs
// .iso.org.dod.internet.private (.1.3.6.1.4)
// .iso.org.dod.internet.private.enterprises (.1.3.6.1.4.1)
// .iso.org.dod.internet.private.enterprises.arduino (.1.3.6.1.4.1.36582)
//
static char const oidTempEDF[]  PROGMEM = "1.3.6.1.4.1.36582.1";  // read-only  (Integer)
static char const oidHumidEDF[] PROGMEM = "1.3.6.1.4.1.36582.2";  // read-only  (Integer)
static char const oidEDFIndex[] PROGMEM = "1.3.6.1.4.1.36582.20";
static char const oidEDF_IInst[] PROGMEM = "1.3.6.1.4.1.36582.23";
static char const oidEDF_PApp[] PROGMEM = "1.3.6.1.4.1.36582.26";

// RFC1213 local values
static char locDescr[]              = "Agentuino, a light-weight SNMP Agent.";  // read-only (static)
static char locObjectID[]           = "1.3.6.1.3.2009.0";                       // read-only (static)
static uint32_t locUpTime           = 0;                                        // read-only (static)
static char locContact[20]          = "Fagart";                                 // should be stored/read from EEPROM - read/write (not done for simplicity)
static char locName[20]             = "Agentuino";                              // should be stored/read from EEPROM - read/write (not done for simplicity)
static char locLocation[20]         = "Paris France";                           // should be stored/read from EEPROM - read/write (not done for simplicity)
static int locServices              = 7;                                        // read-only (static)

uint32_t prevMillis = millis();
char oid[SNMP_MAX_OID_LEN];
SNMP_API_STAT_CODES api_status;
SNMP_ERR_CODES status;

void pduReceived()
{
  SNMP_PDU pdu;
  //
#ifdef DEBUG
  Serial << F("UDP Packet Received Start..") << F(" RAM:") << freeMemory() << endl;
#endif
  //
  api_status = Agentuino.requestPdu(&pdu);

  Serial << F("api ") << api_status << F(" pdu.type") << pdu.type << endl;
  //
  if ( pdu.type == SNMP_PDU_GET || pdu.type == SNMP_PDU_GET_NEXT || pdu.type == SNMP_PDU_SET
    && pdu.error == SNMP_ERR_NO_ERROR && api_status == SNMP_API_STAT_SUCCESS ) {
    //
    pdu.OID.toString(oid);
    //
    //Serial << "OID: " << oid << endl;
    //
    if ( strcmp_P(oid, sysDescr ) == 0 ) {
      handleStringOID (&pdu, locDescr, TRUE);
      //
#ifdef DEBUG
      Serial << F("sysDescr...") << locDescr << F(" ") << pdu.VALUE.size << endl;
#endif
    } 
    else if ( strcmp_P(oid, sysUpTime ) == 0 ) {
      // handle sysName (set/get) requests
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } 
      else {
        // response packet from get-request - locUpTime
        status = pdu.VALUE.encode(SNMP_SYNTAX_TIME_TICKS, locUpTime);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
      //
#ifdef DEBUG
      Serial << F("sysUpTime...") << locUpTime << F(" ") << pdu.VALUE.size << endl;
#endif
    } 
    else if ( strcmp_P(oid, sysName ) == 0 ) {
      handleStringOID (&pdu, locName, FALSE);
#ifdef DEBUG
      Serial << F("sysName...") << locName << F(" ") << pdu.VALUE.size << endl;
#endif
    } 
    else if ( strcmp_P(oid, sysContact ) == 0 ) {
      handleStringOID (&pdu, locContact, FALSE);
#ifdef DEBUG
      Serial << F("sysContact...") << locContact << F(" ") << pdu.VALUE.size << endl;
#endif
    } 
    else if ( strcmp_P(oid, sysLocation ) == 0 ) {
      handleStringOID (&pdu, locLocation, FALSE);
#ifdef DEBUG
      Serial << F("sysLocation...") << locLocation << F(" ") << pdu.VALUE.size << endl;
#endif
    } 
    else if ( strcmp_P(oid, sysServices) == 0 ) {
      // handle sysServices (set/get) requests
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } 
      else {
        // response packet from get-request - locServices
        status = pdu.VALUE.encode(SNMP_SYNTAX_INT, locServices);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
      //
#ifdef DEBUG
      Serial << F("locServices...") << locServices << F(" ") << pdu.VALUE.size << endl;
#endif

    } 
    else if (strcmp_P(oid, oidTempEDF ) == 0) {
      handleReadTemperature(&pdu, &dht_Edf);
    } 
    else if (strcmp_P(oid, oidHumidEDF ) == 0) {
      handleReadHumidity(&pdu, &dht_Edf);
    } 
    #ifdef EDF
    else if (strcmp_P(oid, oidEDFIndex ) == 0) {
      int ok  = teleinfos.read(edfSerial, Serial);
      if (ok)  { 
        handleReadUInt32(&pdu, teleinfos.BASE);
      } 
      else {
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      }
    } 
    else if (strcmp_P(oid, oidEDF_PApp ) == 0) {
      int ok  = teleinfos.read(edfSerial, Serial);
      if (ok)  { 
        handleReadUInt32(&pdu, teleinfos.PAPP);
      } 
      else {
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      }
    } 
    else if (strcmp_P(oid, oidEDF_IInst ) == 0) {
      int ok  = teleinfos.read(edfSerial, Serial);
      if (ok)  { 
        handleReadUInt32(&pdu, teleinfos.IINST);
      } 
      else {
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      }
    } 
    #endif
    else {
      // oid does not exist
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
#ifdef DEBUG
  Serial << F("UDP Packet Received End..") << F(" RAM:") << freeMemory() << endl;
#endif
}

void setup()
{
  Serial.begin(9600);
  Serial << F("setup") << endl;
  delay(1000); 
  dht_Edf.begin();

  Serial << F("ethernet begin") << endl;
//  Ethernet.begin(mac, ip, edf_dns, gateway, subnet);
  delay(1000); // donne le temps à la carte Ethernet de s'initialiser
  //
#ifdef SNMP
  Serial << ("agentuino begin") << endl;

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
#ifdef SNMP
  // listen/handle for incoming SNMP requests
  Agentuino.listen();
#endif
  //
  // sysUpTime - The time (in hundredths of a second) since
  // the network management portion of the system was last
  // re-initialized.
  uint32_t currentMillis = millis();
  uint32_t lastStep = currentMillis - prevMillis;
  if ( lastStep > 1000 ) {
    // increment previous milliseconds
    prevMillis += 1000;
    //
    // increment up-time counter
    locUpTime += 100;
#ifndef SNMP
    Serial << "getTeleinfos begin " << endl;
    int ok  = teleinfos.read(edfSerial, Serial);
    if (!ok)  {
      Serial << "getTeleinfo timedout" << endl;
    } 
    else {
      Serial << "getTeleinfo complete in " << ok << endl;
    }
#endif
  }
}

