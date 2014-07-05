#include <DHT.h>
#include <Streaming.h> 
#include <Ethernet.h>
#include <SPI.h>
#include <MemoryFree.h>
#include <Agentuino.h> 
#include <Flash.h>
#include <snmp_utils.h>


static byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x56, 0xB3 };
static byte ip[] = { 192, 168, 0, 71 };
static byte gateway[] = { 192, 168, 0, 254 };
static byte subnet[] = { 255, 255, 255, 0 };
static byte cave_dns[] = { 192, 168, 0, 254 };

#define DHTTYPE DHT22 // DHT 22 (AM2302)

int dhtCavePin   = 5;  // DHT22 EDF
int pirPin=3; 

DHT dht_Cave(dhtCavePin, DHTTYPE);

char inData[30]; // Allocate some space for the string
char inChar=-1; // Where to store the character read
byte index = 0; // Index into array; where to store the character

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
static char const oidTempCave[]  PROGMEM = "1.3.6.1.4.1.36582.1";  // read-only  (Integer)
static char const oidHumidCave[] PROGMEM = "1.3.6.1.4.1.36582.2";  // read-only  (Integer)
static char const oidPresCave[]  PROGMEM = "1.3.6.1.4.1.36582.3";  // read-only  (Integer)
static char const oidAbsCave[]   PROGMEM = "1.3.6.1.4.1.36582.4";  // read-only  (Integer)
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

float tempCave = 0, humCave = 0;
int pir_moving = 0, pir_nobody = 0;

uint32_t timeSecond = 0;

void pduReceived()
{
  SNMP_PDU pdu;
  
  api_status = Agentuino.requestPdu(&pdu);
  
  if ( pdu.type == SNMP_PDU_GET || pdu.type == SNMP_PDU_GET_NEXT || pdu.type == SNMP_PDU_SET
    && pdu.error == SNMP_ERR_NO_ERROR && api_status == SNMP_API_STAT_SUCCESS ) {
    
    pdu.OID.toString(oid);
 
    if ( strcmp_P(oid, sysDescr ) == 0 ) {
		handleStringOID (&pdu, locDescr, TRUE);
    } else if ( strcmp_P(oid, sysUpTime ) == 0 ) {
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
    } else if ( strcmp_P(oid, sysName ) == 0 ) {
	handleStringOID (&pdu, locName, FALSE);
    } else if ( strcmp_P(oid, sysContact ) == 0 ) {
	handleStringOID (&pdu, locContact, FALSE);
    } else if ( strcmp_P(oid, sysLocation ) == 0 ) {
	handleStringOID (&pdu, locLocation, FALSE);
    } else if ( strcmp_P(oid, sysServices) == 0 ) {
        handleIntOID(&pdu, &locServices, TRUE);
		
    } else if (strcmp_P(oid, oidTempCave ) == 0) {
	handleReadTemperature(&pdu, &dht_Cave);
    } else if (strcmp_P(oid, oidHumidCave ) == 0) {
	handleReadHumidity(&pdu, &dht_Cave);
    } else if (strcmp_P(oid, oidPresCave ) == 0) {
	handleIntOID(&pdu, &pir_moving, TRUE);
    } else if (strcmp_P(oid, oidAbsCave ) == 0) {
	handleIntOID(&pdu, &pir_nobody, TRUE);
		
    }  else {
      // oid does not exist
      //
      // response packet - object not found
      pdu.type = SNMP_PDU_RESPONSE;
      pdu.error = SNMP_ERR_NO_SUCH_NAME;
    }

    Agentuino.responsePdu(&pdu);
  }

  Agentuino.freePdu(&pdu);
}

int pir_delay=300; 
int decompte=0;
  
void setup() {
  pinMode(pirPin, INPUT);
  dht_Cave.begin();
  delay(1000); 
  //
  Ethernet.begin(mac, ip, gateway, subnet);
  delay(1000); // donne le temps à la carte Ethernet de s'initialiser
  //
  api_status = Agentuino.begin();
  //
  if ( api_status == SNMP_API_STAT_SUCCESS ) {
    //
    Agentuino.onPduReceive(pduReceived);
    delay(10);
    return;
  }
  delay(10);
}

void loop() 
{
  // listen/handle for incoming SNMP requests
  Agentuino.listen();
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
    timeSecond += 1;

    int pirVal = digitalRead(pirPin);
    
    if(pirVal == LOW)
    {
      if (decompte!=pir_delay)
      {
        pir_moving = true;
        decompte=pir_delay;
      }  
      else
      {
        pir_moving = false;
      }  
    } 
    else
    {
    // plus personne, on commence à décompter
      if(decompte > 0 )
      {
        decompte--;
        pir_nobody = false;
      }
      else if (decompte == 0)
      {
        pir_nobody = true;
        decompte=-1;
      }
    }
  }  
}
