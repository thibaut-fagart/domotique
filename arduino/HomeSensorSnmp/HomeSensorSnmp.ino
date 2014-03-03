#include <DHT.h>
#include <Streaming.h> 
#include <Ethernet.h>
#include <SPI.h>
#include <MemoryFree.h>
#include <Agentuino.h> 
#include <Flash.h>
#include <TimerOne.h>
#include <snmp_utils.h>


static byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0xEE, 0x82 };
static byte ip[] = { 192, 168, 0, 70 };
static byte gateway[] = { 192, 168, 0, 254 };
static byte subnet[] = { 255, 255, 255, 0 };
static byte home_dns[] = { 192, 168, 0, 254 };

#define DHTTYPE DHT22 // DHT 22 (AM2302)

int dhtSalonPin   = 31;  // DHT22 Salon
int dhtPCPin      = 33;  // DHT22 Palcard PC
int dhtSdBPin     = 43;  // DHT22 Salle de Bain
int dhtExtPin     = 45;  // DHT22 Exterieur

DHT dht_Salon(dhtSalonPin, DHTTYPE);
DHT dht_PC(dhtPCPin, DHTTYPE);
DHT dht_SdB(dhtSdBPin, DHTTYPE);
DHT dht_Ext(dhtExtPin, DHTTYPE);

int VMCPin        = 46;  // VMC Power
int FiveVPin      = 48;  // 5V cmd

int portePin      = 28;  // Switch porte

int couloir1Pin = 36;  // Ventilo couloir 1
int couloir2Pin = 38;  // Ventilo couloir 2
int SdB1Pin     = 32;  // Ventilo Salle de bain 1
int SdB2Pin     = 34;  // Ventilo Salle de bain 2


int couloirPWMPin = 11;  // Ventilo couloir PWM
int SdBPWMPin     = 12;  // Ventilo Salle de bain PWM

int ThermoPin       = 40; // Relay Thermostat
int TwelveVPinSpOne = 42;  // 12V cmd
int TwelveVPinSpTwo = 44;  // 12V cmd

int AudioCuisinePin = 26; // Power Ampli Cuisine
int AudioSdBPin     = 28; // Power Ampli Salle de bain
int AudioChambrePin = 30; // Power Ampli Chambre
int AudioSalonPin   = 35; // Power Ampli Salon

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
static char const oidTempSalon[]  PROGMEM = "1.3.6.1.4.1.36582.1";  // read-only  (Integer)
static char const oidHumidSalon[] PROGMEM = "1.3.6.1.4.1.36582.2";  // read-only  (Integer)
static char const oidTempPC[]     PROGMEM = "1.3.6.1.4.1.36582.3";  // read-only  (Integer)
static char const oidHumidPC[]    PROGMEM = "1.3.6.1.4.1.36582.4";  // read-only  (Integer)
static char const oidTempSdB[]    PROGMEM = "1.3.6.1.4.1.36582.5";  // read-only  (Integer)
static char const oidHumidSdB[]   PROGMEM = "1.3.6.1.4.1.36582.6";  // read-only  (Integer)
static char const oidTempExt[]    PROGMEM = "1.3.6.1.4.1.36582.7";  // read-only  (Integer)
static char const oidHumidExt[]   PROGMEM = "1.3.6.1.4.1.36582.8";  // read-only  (Integer)
//
static char const oidVentiloCouloir1State[]   PROGMEM = "1.3.6.1.4.1.36582.10";  // read-write  (Integer)
static char const oidVentiloCouloir2State[]   PROGMEM = "1.3.6.1.4.1.36582.11";  // read-write  (Integer)
static char const oidVentiloCouloirSpeed[]    PROGMEM = "1.3.6.1.4.1.36582.12";  // read-write  (Integer)
static char const oidVentiloSdB1State[]       PROGMEM = "1.3.6.1.4.1.36582.15";  // read-write  (Integer)
static char const oidVentiloSdB2State[]       PROGMEM = "1.3.6.1.4.1.36582.16";  // read-write  (Integer)
static char const oidVentiloSdBSpeed[]        PROGMEM = "1.3.6.1.4.1.36582.17";  // read-write  (Integer)
//
static char const oidPorteState[]        PROGMEM = "1.3.6.1.4.1.36582.20";  // read-only  (Integer)
static char const oidThermostatState[]   PROGMEM = "1.3.6.1.4.1.36582.21";  // read-write  (Integer)
//
static char const oidAmpliSalonState[]   PROGMEM = "1.3.6.1.4.1.36582.30";  // read-write  (Integer)
static char const oidAmpliSdBState[]     PROGMEM = "1.3.6.1.4.1.36582.31";  // read-write  (Integer)
static char const oidAmpliCuisineState[] PROGMEM = "1.3.6.1.4.1.36582.32";  // read-write  (Integer)
static char const oidAmpliChambreState[] PROGMEM = "1.3.6.1.4.1.36582.33";  // read-write  (Integer)
//
static char const oidVMCState[]          PROGMEM = "1.3.6.1.4.1.36582.40";  // read-write  (Integer)
//
static char const oidTempExtEte[]        PROGMEM = "1.3.6.1.4.1.36582.50";  // read-write  (Integer)
static char const oidVMCMan[]            PROGMEM = "1.3.6.1.4.1.36582.51";  // read-write  (Integer)
static char const oidAudioMan[]          PROGMEM = "1.3.6.1.4.1.36582.52";  // read-write  (Integer)
//
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

// Définition du timeout compteur de vitesse ventilateur
#define PULSE_TIMEOUT 200000
 
// Définition des etats interne
int VMCState          = 1;
int AudioSdBState     = 0;
int AudioSalonState   = 0;
int AudioChambreState = 0;
int AudioCuisineState = 0;
int ThermoState       = 0;
int SdB1State         = 0;
int SdB2State         = 0;
int SdBPWMSpeed       = 800;  
int couloir1State     = 0;
int couloir2State     = 0;
int couloirPWMSpeed   = 800;  
int tempExtEte        = 15; 
int VMCMan            = 0;
int AudioMan          = 1;
int porteState        = 0;

float tempSdB = 0, humSdB = 0;
float tempPC = 0, humPC = 0;
float tempSalon = 0, humSalon = 0;
float tempExt = 0, humExt = 0;

uint32_t timeSecond = 0;
uint32_t lastTimeSecondVMC    = 0;
uint32_t lastTimeSecondAudio  = 0;
uint32_t lastTimeSecondThermo = 0;


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
	  
    } else if ( strcmp_P(oid, oidPorteState) == 0 ) {
        handleIntOID(&pdu, &porteState, TRUE);
    } else if (strcmp_P(oid, oidTempExtEte ) == 0) {
        handleIntOID(&pdu, &tempExtEte, FALSE);
    } else if (strcmp_P(oid, oidVMCMan ) == 0) {
        handleIntOID(&pdu, &VMCMan, FALSE);
    } else if (strcmp_P(oid, oidAudioMan ) == 0) {
        handleIntOID(&pdu, &AudioMan, FALSE);
		
    } else if (strcmp_P(oid, oidTempSdB ) == 0) {
	handleReadTemperature(&pdu, &dht_SdB);
    } else if (strcmp_P(oid, oidHumidSdB ) == 0) {
	handleReadHumidity(&pdu, &dht_SdB);
		
    } else if (strcmp_P(oid, oidTempSalon ) == 0) {
	handleReadTemperature(&pdu, &dht_Salon);
    } else if (strcmp_P(oid, oidHumidSalon ) == 0) {
	handleReadHumidity(&pdu, &dht_Salon);
		
    } else if (strcmp_P(oid, oidTempPC ) == 0) {
	handleReadTemperature(&pdu, &dht_PC);
    } else if (strcmp_P(oid, oidHumidPC ) == 0) {
	handleReadHumidity(&pdu, &dht_PC);
		
    } else if (strcmp_P(oid, oidTempExt ) == 0) {
	handleReadTemperature(&pdu, &dht_Ext);
    } else if (strcmp_P(oid, oidHumidExt ) == 0) {
	handleReadHumidity(&pdu, &dht_Ext);

    } else if (strcmp_P(oid, oidVMCState ) == 0) {
        handleIntOID(&pdu, &VMCState, FALSE);
    } else if (strcmp_P(oid, oidThermostatState ) == 0) {
        handleIntOID(&pdu, &ThermoState, FALSE);
		
    } else if (strcmp_P(oid, oidAmpliSalonState ) == 0) {
        handleIntOID(&pdu, &AudioSalonState, FALSE);
    } else if (strcmp_P(oid, oidAmpliSdBState ) == 0) {
        handleIntOID(&pdu, &AudioSdBState, FALSE);
    } else if (strcmp_P(oid, oidAmpliChambreState ) == 0) {
        handleIntOID(&pdu, &AudioChambreState, FALSE);
    } else if (strcmp_P(oid, oidAmpliCuisineState ) == 0) {
        handleIntOID(&pdu, &AudioCuisineState, FALSE);

    } else if (strcmp_P(oid, oidVentiloSdB1State ) == 0) {
        handleIntOID(&pdu, &SdB1State, FALSE);
    } else if (strcmp_P(oid, oidVentiloSdB2State ) == 0) {
        handleIntOID(&pdu, &SdB2State, FALSE);
    } else if (strcmp_P(oid, oidVentiloCouloir1State ) == 0) {
        handleIntOID(&pdu, &couloir1State, FALSE);
    } else if (strcmp_P(oid, oidVentiloCouloir2State ) == 0) {
        handleIntOID(&pdu, &couloir2State, FALSE);

    } else if (strcmp_P(oid, oidVentiloCouloirSpeed ) == 0) {
        handleIntOID(&pdu, &couloirPWMSpeed, FALSE);
    } else if (strcmp_P(oid, oidVentiloSdBSpeed ) == 0) {
        handleIntOID(&pdu, &SdBPWMSpeed, FALSE);

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

void setup()
{
  pinMode(VMCPin,          OUTPUT);  
  pinMode(couloir1Pin,     OUTPUT);  
  pinMode(couloir2Pin,     OUTPUT);  
  pinMode(SdB1Pin,         OUTPUT);  
  pinMode(SdB2Pin,         OUTPUT);  
  pinMode(AudioCuisinePin, OUTPUT);
  pinMode(AudioSdBPin,     OUTPUT);
  pinMode(AudioChambrePin, OUTPUT);
  pinMode(ThermoPin,       OUTPUT);
  
  dht_SdB.begin();
  dht_Salon.begin();
  dht_PC.begin();
  dht_Ext.begin();

  digitalWrite(VMCPin,HIGH);
  digitalWrite(portePin,LOW);
  
  Timer1.initialize(40000);
  Timer1.pwm(couloirPWMPin, couloirPWMSpeed);
  Timer1.pwm(SdBPWMPin, SdBPWMSpeed);

  Serial.begin(9600);

  delay(1000); 
  //
  Ethernet.begin(mac, ip, gateway, subnet);
  //Ethernet.begin(mac, ip, home_dns, gateway, subnet);
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
  }
  
  if ( (timeSecond - lastTimeSecondVMC) > 30 ) {
    lastTimeSecondVMC = timeSecond;
    LogicVMC();
  }
  if ( (timeSecond - lastTimeSecondAudio) > 5 ) {
    lastTimeSecondAudio = timeSecond;
    LogicAudio();
  }
  if ( (timeSecond - lastTimeSecondThermo) > 5 ) {
    lastTimeSecondThermo = timeSecond;
    LogicThermostat();	
  } 
}  

void LogicVMC()
{
  if ( VMCMan == 0 ) {
        tempExt = dht_Ext.readTemperature(false);
        humSdB = dht_SdB.readHumidity();
	humSalon = dht_Salon.readHumidity();
		
	if ( tempExt > tempExtEte + 1) {
            digitalWrite(VMCPin,     HIGH);
            digitalWrite(couloir1Pin,LOW);
            digitalWrite(couloir2Pin,LOW);
            digitalWrite(SdB1Pin,    LOW);
            digitalWrite(SdB2Pin,    LOW);
        } else {
            if (humSdB > humSalon + 20.) {
		digitalWrite(VMCPin,     HIGH);
		digitalWrite(couloir1Pin,LOW);
		digitalWrite(couloir2Pin,LOW);
		digitalWrite(SdB1Pin,    LOW);
		digitalWrite(SdB2Pin,    LOW);
	    }
            if ((humSdB < humSalon + 10.) and (tempExt < tempExtEte)) {
		digitalWrite(VMCPin,     LOW);
		digitalWrite(couloir1Pin,HIGH);
		digitalWrite(couloir2Pin,HIGH);
		digitalWrite(SdB1Pin,    HIGH);
		digitalWrite(SdB2Pin,    HIGH);
            }    
        }
        pinGetState(&VMCState,      VMCPin);
        pinGetState(&couloir1State, couloir1Pin);
        pinGetState(&couloir2State, couloir2Pin);
        pinGetState(&SdB1State,     SdB1Pin);
        pinGetState(&SdB2State,     SdB2Pin);

  } else {
	pinSetState(VMCState,      VMCPin);
	pinSetState(couloir1State, couloir1Pin);
	pinSetState(couloir2State, couloir2Pin);
	pinSetState(SdB1State,     SdB1Pin);
	pinSetState(SdB2State,     SdB2Pin);
  }
}

void LogicAudio()
{
  if ( AudioMan == 0  && porteState == 1 ) {
		digitalWrite(AudioSalonPin,  LOW);
		digitalWrite(AudioChambrePin,LOW);
		digitalWrite(AudioSdBPin,    LOW);
		digitalWrite(AudioCuisinePin,LOW);

		pinGetState(&AudioSalonState,   AudioSalonPin);
		pinGetState(&AudioChambreState, AudioChambrePin);
		pinGetState(&AudioSdBState,     AudioSdBPin);
		pinGetState(&AudioCuisineState, AudioCuisinePin);
  } else {
		pinSetState(AudioSalonState,   AudioSalonPin);
		pinSetState(AudioChambreState, AudioChambrePin);
		pinSetState(AudioSdBState,     AudioSdBPin);
		pinSetState(AudioCuisineState, AudioCuisinePin);
  }
}

void LogicThermostat()
{
	int curentThermoState = digitalRead(ThermoPin);
	
	if (curentThermoState == 1) {
		pinSetState(0, ThermoPin);
	}
	
	if (ThermoState == 1 && curentThermoState == 0) {
		pinSetState(ThermoState, ThermoPin);
	} 

	pinGetState(&ThermoState, ThermoPin);
}

void LogicVentiloSpeed()
{
    Timer1.setPwmDuty(couloirPWMPin, couloirPWMSpeed);
    Timer1.setPwmDuty(SdBPWMPin, SdBPWMSpeed);
}

void pinSetState(int state, int pin)
{
	if (state == 1) {
		digitalWrite(pin,HIGH);
	} else {
		digitalWrite(pin,LOW);
	}
}

void pinGetState(int* state, int pin)
{
	*state = digitalRead(pin);
}
