/*
reserved pins
ethernet shield : 4 10 11 12 13

*/

#define DEBUG 1
#define EDF
#define SNMP


#include <DHT.h>
#include <Streaming.h>         // Include the Streaming library
#include <Ethernet.h>          // Include the Ethernet library
#include <SPI.h>
#include <MemoryFree.h>
#include <Agentuino.h> 
#include <Flash.h>
#include <SoftwareSerial.h>
#include <snmp_utils.h>


static byte mac[] = { 0x90, 0xA2, 0xDA, 0x0E, 0x0C, 0x4A };
static byte ip[] = { 192, 168, 1, 99 };
static byte gateway[] = { 192, 168, 1, 254 };
static byte subnet[] = { 255, 255, 255, 0 };
static byte leroux_dns[] = { 192, 168, 1, 254 };
#define DHTTYPE DHT22 // DHT 22 (AM2302)
/*
0-3 capteurs dht
4 viierge
5 relay
6 reset
7-9 capteurs

*/
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

DHT dht_exterieur(dht22ExtPin, DHTTYPE);
DHT dht_nouvelleMaison(dht22NewPin, DHTTYPE);
DHT dht_ancienneMaison(dht22OldPin, DHTTYPE);
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
static char const oidTempExt[] PROGMEM    = "1.3.6.1.4.1.36582.0";  // read-only  (Integer)
static char const oidHumidExt[] PROGMEM   = "1.3.6.1.4.1.36582.1";  // read-only  (Integer)
static char const oidTempOld[] PROGMEM    = "1.3.6.1.4.1.36582.2";  // read-only  (Integer)
static char const oidHumidOld[] PROGMEM   = "1.3.6.1.4.1.36582.3";  // read-only  (Integer)
static char const oidTempNew[] PROGMEM    = "1.3.6.1.4.1.36582.4";  // read-only  (Integer)
static char const oidHumidNew[] PROGMEM   = "1.3.6.1.4.1.36582.5";  // read-only  (Integer)
static char const oidBurningTime[] PROGMEM   = "1.3.6.1.4.1.36582.10";  // read-only  (counter)
static char const oidBurntFuel[] PROGMEM   = "1.3.6.1.4.1.36582.11";  // read-only  (SNMP_SYNTAX_COUNTER64)
static char const oidRemainingFuel[] PROGMEM   = "1.3.6.1.4.1.36582.12";  // read-only  (gauge)
static char const oidTest[] PROGMEM   = "1.3.6.1.4.1.36582.19";  // read-write  (Integer)
static char const oidEDFIndexNormal[] PROGMEM = "1.3.6.1.4.1.36582.20";
static char const oidEDFIndexPointe[] PROGMEM = "1.3.6.1.4.1.36582.21";
static char const oidEDFPreavisEJP[] PROGMEM = "1.3.6.1.4.1.36582.22";
static char const oidEDF_IInst1[] PROGMEM = "1.3.6.1.4.1.36582.23";
static char const oidEDF_IInst2[] PROGMEM = "1.3.6.1.4.1.36582.24";
static char const oidEDF_IInst3[] PROGMEM = "1.3.6.1.4.1.36582.25";
static char const oidEDF_PApp[] PROGMEM = "1.3.6.1.4.1.36582.25";
//
// RFC1213 local values
static char locDescr[]              = "Agentuino, a light-weight SNMP Agent.";  // read-only (static)
static char locObjectID[]           = "1.3.6.1.3.2009.0";                       // read-only (static)
static uint32_t locUpTime           = 0;                                        // read-only (static)
static char locContact[20]          = "Fagart";                            // should be stored/read from EEPROM - read/write (not done for simplicity)
static char locName[20]             = "Agentuino";                              // should be stored/read from EEPROM - read/write (not done for simplicity)
static char locLocation[20]         = "Le Roux France";                        // should be stored/read from EEPROM - read/write (not done for simplicity)
static int32_t locServices          = 7;                                        // read-only (static)


/****************************************
 * Fuel management
 */
const uint32_t FUEL_TANK_CAPACITY = 2000;
const float fuel_flow_l_per_hour = 4.6f;
const int seconds_per_hour = 3600;
// cumulated burning time (seconds), updated in real time by the main loop
uint32_t burningTime_s = 0;
// intermediate time counter for precision
uint32_t burningTime_ms = 0;
// fuel supposed to be remaining in the fuel tank
uint32_t remainingFuel_l = FUEL_TANK_CAPACITY;

/******************* END OF CONFIGURATION *******************/


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
    } else if ( strcmp_P(oid, sysUpTime ) == 0 ) {
      // handle sysName (set/get) requests
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } else {
        // response packet from get-request - locUpTime
        status = pdu.VALUE.encode(SNMP_SYNTAX_TIME_TICKS, locUpTime);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
      //
      #ifdef DEBUG
        Serial << F("sysUpTime...") << locUpTime << F(" ") << pdu.VALUE.size << endl;
      #endif
    } else if ( strcmp_P(oid, sysName ) == 0 ) {
		handleStringOID (&pdu, locName, FALSE);
      #ifdef DEBUG
        Serial << F("sysName...") << locName << F(" ") << pdu.VALUE.size << endl;
      #endif
    } else if ( strcmp_P(oid, sysContact ) == 0 ) {
		handleStringOID (&pdu, locContact, FALSE);
      #ifdef DEBUG
        Serial << F("sysContact...") << locContact << F(" ") << pdu.VALUE.size << endl;
      #endif
    } else if ( strcmp_P(oid, sysLocation ) == 0 ) {
		handleStringOID (&pdu, locLocation, FALSE);
      #ifdef DEBUG
        Serial << F("sysLocation...") << locLocation << F(" ") << pdu.VALUE.size << endl;
      #endif
    } else if ( strcmp_P(oid, sysServices) == 0 ) {
      // handle sysServices (set/get) requests
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } else {
        // response packet from get-request - locServices
        status = pdu.VALUE.encode(SNMP_SYNTAX_INT, locServices);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
      //
      #ifdef DEBUG
        Serial << F("locServices...") << locServices << F(" ") << pdu.VALUE.size << endl;
      #endif
      
    } else if (strcmp_P(oid, oidTempExt ) == 0) {
		handleReadTemperature(&pdu, &dht_exterieur);
    } else if (strcmp_P(oid, oidHumidExt ) == 0) {
		handleReadHumidity(&pdu, &dht_exterieur);
    } else if (strcmp_P(oid, oidTempOld ) == 0) {
		handleReadTemperature(&pdu, &dht_ancienneMaison);
    } else if (strcmp_P(oid, oidHumidOld ) == 0 ) {
		handleReadHumidity(&pdu, &dht_ancienneMaison);
    } else if (strcmp_P(oid, oidTempNew ) == 0 ) {
		handleReadTemperature(&pdu, &dht_nouvelleMaison);
    } else if (strcmp_P(oid, oidHumidNew ) == 0) {
		handleReadHumidity(&pdu, &dht_nouvelleMaison);
    } else if (strcmp_P(oid, oidBurningTime ) == 0) {
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-write
        uint32_t newBurningTime = burningTime_s;
        status = pdu.VALUE.decode(&newBurningTime);
        #ifdef DEBUG
        Serial << F("updating burningTime ") << burningTime_s << F(" to ") << newBurningTime << endl;
        #endif
        burningTime_s = newBurningTime;
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      } else {
        status = pdu.VALUE.encode(SNMP_SYNTAX_COUNTER, burningTime_s);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
    } else if (strcmp_P(oid, oidBurntFuel ) == 0) {
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } else {
        uint64_t usedFuel_ml =  (((uint64_t) burningTime_s ) *fuel_flow_l_per_hour)/ 3.6;
      #ifdef DEBUG
      Serial << F(" consumed fuel since reset ") << (uint32_t)usedFuel_ml << endl;
      #endif
        status = pdu.VALUE.encode(SNMP_SYNTAX_COUNTER64, usedFuel_ml);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }      
    } else if (strcmp_P(oid, oidRemainingFuel ) == 0) {
        // response packet from set-request - object is read-only
        #ifdef DEBUG
        Serial << F(" oidRemainingFuel , pduType=") << pdu.type  << endl;
        #endif
        if ( pdu.type == SNMP_PDU_SET ) {
          uint32_t newRemainingFuel = remainingFuel_l ;
          status = pdu.VALUE.decode(&newRemainingFuel);
          #ifdef DEBUG
          Serial << F(" init Fuel, previous remaining ") << remainingFuel_l 
                 << F(" new remaining ") << newRemainingFuel << endl;
          #endif
          remainingFuel_l = newRemainingFuel;
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = status;
        } else {
          uint64_t usedFuel_ml =  (((uint64_t) burningTime_s ) *fuel_flow_l_per_hour)/ 3.6;
          uint32_t temp_remainingFuel_l = remainingFuel_l - (usedFuel_ml/1000);
          #ifdef DEBUG
          Serial << F(" remaining fuel since reset ") << temp_remainingFuel_l << F(", init fuel tank ")<<remainingFuel_l << endl;
          #endif
          status = pdu.VALUE.encode(SNMP_SYNTAX_GAUGE, temp_remainingFuel_l);
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = status;
        }
/*    } else if (strcmp_P(oid, oidTest ) == 0) {
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } else {
      #ifdef DEBUG
      uint32_t i1 =0x00000000;
      uint32_t i2 =0xFFFFFFFF;
      Serial << F(" i1= ") << i1 << F(" , i2= ") << i2 << endl;
      Serial << F(" i1-1= ") << (i1-1) << F(" , i2+1= ") <<( i2 +1)<< endl;
      Serial << F(" i2+1 -i2= ") << (i2+1-i2) << endl;
      #endif
          status = pdu.VALUE.encode(SNMP_SYNTAX_GAUGE, (i2+1-i2));
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = status;
      }
*/
    } else if (strcmp_P(oid, oidEDFIndexNormal ) == 0) {
        int ok  = teleinfos.read(edfSerial, Serial);
        if (!ok)  { 
          handleReadUInt32(&pdu, teleinfos.EJPHN);
        } else {
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
        }
    } else if (strcmp_P(oid, oidEDFIndexPointe ) == 0) {
        int ok  = teleinfos.read(edfSerial, Serial);
        if (!ok)  { 
          handleReadUInt32(&pdu, teleinfos.EJPHPM);
        } else {
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
        }
    }      
  } else if (strcmp_P(oid, oidEDFPreavisEJP ) == 0) {
        int ok  = teleinfos.read(edfSerial, Serial);
        if (!ok)  { 
          handleReadInt(&pdu, teleinfos.PEJP);
        } else {
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
        }
  } else if (strcmp_P(oid, oidEDF_PApp ) == 0) {
        int ok  = teleinfos.read(edfSerial, Serial);
        if (!ok)  { 
          handleReadUInt32(&pdu, teleinfos.PAPP);
        } else {
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
        }
  } else if (strcmp_P(oid, oidEDF_IInst1 ) == 0) {
        int ok  = teleinfos.read(edfSerial, Serial);
        if (!ok)  { 
          handleReadInt(&pdu, teleinfos.IINST1);
        } else {
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
        }
  } else if (strcmp_P(oid, oidEDF_IInst2 ) == 0) {
        int ok  = teleinfos.read(edfSerial, Serial);
        if (!ok)  { 
          handleReadInt(&pdu, teleinfos.IINST2);
        } else {
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
        }
  } else if (strcmp_P(oid, oidEDF_IInst3 ) == 0) {
        int ok  = teleinfos.read(edfSerial, Serial);
        if (!ok)  { 
          handleReadInt(&pdu, teleinfos.IINST3);
        } else {
          pdu.type = SNMP_PDU_RESPONSE;
          pdu.error = SNMP_ERR_READ_ONLY;
        }
  } else {
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

/*void resetEthernet() {
  digitalWrite(resetPin,LOW); // put reset pin to low ==> reset the ethernet shield
  delay(200);
  digitalWrite(resetPin,HIGH); // set it back to high
  delay(2000);
}
*/
void setup()
{
  Serial.begin(9600);
  Serial << F("setup") << endl;
//  pinMode(relayPin,    OUTPUT);
//  pinMode(resetPin,    OUTPUT);
  pinMode(flowPin,     INPUT);
    // manually reset the ethernet shield before using it
//  resetEthernet();
  delay(1000); 
  dht_exterieur.begin();
  dht_nouvelleMaison.begin();
  dht_ancienneMaison.begin();

  Serial << F("ethernet begin") << endl;
  Ethernet.begin(mac, ip, leroux_dns, gateway, subnet);
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
    if (digitalRead(flowPin) ==1) {
      // currentlyBurning
      burningTime_ms +=lastStep;
      if (burningTime_ms > 1000) {
        burningTime_s +=1;
        #ifdef DEBUG
//        Serial << F("burning for ") << burningTime_s << endl;
        #endif
        burningTime_ms -=1000;
      }
    }
  }
 
}
