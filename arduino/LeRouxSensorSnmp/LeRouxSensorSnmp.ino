#include <DHT.h>
#include <Streaming.h>         // Include the Streaming library
#include <Ethernet.h>          // Include the Ethernet library
#include <SPI.h>
#include <MemoryFree.h>
#include <Agentuino.h> 
#include <Flash.h>
#include <SoftwareSerial.h>
#include <snmp_utils.h>

//
#define DEBUG
//


static byte mac[] = { 0x90, 0xA2, 0xDA, 0x0E, 0x0C, 0x4A };
// MAC de l'ancienne carte
//static byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0xEE, 0x82 };
static byte ip[] = { 192, 168, 1, 99 };
//static byte ip[] = { 192, 168, 1, 100 };
static byte gateway[] = { 192, 168, 1, 254 };
static byte subnet[] = { 255, 255, 255, 0 };
static byte leroux_dns[] = { 192, 168, 1, 254 };
#define DHTTYPE DHT22 // DHT 22 (AM2302)

int dht22XXX = 0; 
int dht22YYY = 1; 
int dht22OldPin = 2; 
int dht22NewPin = 7;
int dht22ExtPin = 8; 
DHT dht_exterieur(dht22ExtPin, DHTTYPE);
DHT dht_nouvelleMaison(dht22NewPin, DHTTYPE);
DHT dht_ancienneMaison(dht22OldPin, DHTTYPE);
int relayPin    = 5; 
int resetPin    = 6; 
int EDFPin      = 3;
int flowPin     = 9; 

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
static char const oidSwitchEDF[] PROGMEM   = "1.3.6.1.4.1.36582.20";  // read-write  (String)

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

/*****************************************
 * EDF 
 */
SoftwareSerial cptSerial(EDFPin, 1);
uint32_t prevEDFReadMillis = 0;
static char edfOnOff[20]             = "off";
static int edfOn =  strcmp("on",edfOnOff);
/***************** Teleinfo configuration part *******************/
char CaractereRecu ='\0';
char Checksum[32] = "";
char Ligne[32]="";
char Etiquette[9] = "";
char Donnee[13] = "";
char Trame[512] ="";
int i = 0;
int j = 0;

unsigned long Chrono = 0;
unsigned long LastChrono = 0;

char ADCO[12] ;      // Adresse du concentrateur de téléreport (numéro de série du compteur), 12 numériques + \0
long HCHC = 0;      // Index option Heures Creuses - Heures Creuses, 8 numériques, Wh
long HCHP = 0;      // Index option Heures Creuses - Heures Pleines, 8 numériques, Wh
char PTEC[4] ;      // Période Tarifaire en cours, 4 alphanumériques
char HHPHC[2] ; // Horaire Heures Pleines Heures Creuses, 1 alphanumérique (A, C, D, E ou Y selon programmation du compteur)
int IINST = 0;     // Monophasé - Intensité Instantanée, 3 numériques, A  (intensité efficace instantanée)
long PAPP = 0;      // Puissance apparente, 5 numérique, VA (arrondie à la dizaine la plus proche)
long IMAX = 0;      // Monophasé - Intensité maximale appelée, 3 numériques, A
char OPTARIF[4] ;    // Option tarifaire choisie, 4 alphanumériques (BASE => Option Base, HC.. => Option Heures Creuses, EJP. => Option EJP, BBRx => Option Tempo [x selon contacts auxiliaires])
char MOTDETAT[10] = "";  // Mot d'état du compteur, 10 alphanumériques
int ISOUSC = 0;    // Intensité souscrite, 2 numériques, A

int check[11];  // Checksum by etiquette
int trame_ok = 1; // global trame checksum flag
int finTrame=0;
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
//    Serial << F("UDP Packet Received Start..") << F(" RAM:") << freeMemory() << endl;
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
    } else if ( strcmp_P(oid, oidSwitchEDF ) == 0 ) {
      // start/stop listening to edf signals
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read/write
        status = pdu.VALUE.decode(edfOnOff, strlen(edfOnOff)); 
        edfOn = strcmp ("on", edfOnOff);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      #ifdef DEBUG
        Serial << F("edf switched ...") << (edfOn ? "on" : "off") << endl;
      #endif
      } else {
        // response packet from get-request - locName
        status = pdu.VALUE.encode(SNMP_SYNTAX_OCTETS, edfOnOff);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
      //
}  else {
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
  //Serial << "UDP Packet Received End.." << " RAM:" << freeMemory() << endl;
}

void resetEthernet() {
  digitalWrite(resetPin,LOW); // put reset pin to low ==> reset the ethernet shield
  delay(200);
  digitalWrite(resetPin,HIGH); // set it back to high
  delay(2000);
}

void setup()
{
  pinMode(relayPin,    OUTPUT);
  pinMode(resetPin,    OUTPUT);
  pinMode(flowPin,     INPUT);
  pinMode(EDFPin,      INPUT);
  // fil rose = flow (pin 7)
  // fil orange = edf (pin 9)
  // gris = 5v
  // marron = masse
  // blanc
  Serial.begin(9600);
  cptSerial.begin(1200);
    // manually reset the ethernet shield before using it
  resetEthernet();
  delay(1000); 
  dht_exterieur.begin();
  dht_nouvelleMaison.begin();
  dht_ancienneMaison.begin();


  Ethernet.begin(mac, ip, leroux_dns, gateway, subnet);
  delay(1000); // donne le temps à la carte Ethernet de s'initialiser
  //
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
}
void getTeleinfo() {
  Serial << F(">>getTeleinfo") << endl;
  /* vider les infos de la dernière trame lue */
  memset(Ligne,'\0',32); 
  memset(Trame,'\0',512);
  int trameComplete=0;

  memset(ADCO,'\0',12);
  HCHC = 0;
  HCHP = 0;
  memset(PTEC,'\0',4);
  memset(HHPHC,'\0',2);
  IINST = 0;
  PAPP = 0;
  IMAX = 0;
  memset(OPTARIF,'\0',4);
  memset(MOTDETAT,'\0',10);
  ISOUSC = 0;


  while (!trameComplete){
    while(CaractereRecu != 0x02) // boucle jusqu'a "Start Text 002" début de la trame
    {
       if (cptSerial.available()) {
         CaractereRecu = cptSerial.read() & 0x7F;
       }
    }

    i=0; 
    while(CaractereRecu != 0x03) // || !trame_ok ) // Tant qu'on est pas arrivé à "EndText 003" Fin de trame ou que la trame est incomplète
    { 
      if (cptSerial.available()) {
          CaractereRecu = cptSerial.read() & 0x7F;
  	  Trame[i++]=CaractereRecu;
      }	
    }
    finTrame = i;
    Trame[i++]='\0';

    Serial << F("Trame [")<< (Trame) << F("]")<< endl;
  
    lireTrame(Trame);	

    // on vérifie si on a une trame complète ou non
    for (i=0; i<11; i++) {
      trameComplete+=check[i];
    }
    Serial << F("Nb lignes valides :") <<(trameComplete) << endl;
    if (trameComplete < 11) trameComplete=0; // on a pas les 11 valeurs, il faut lire la trame suivante
    else trameComplete = 1;
  }
    Serial << F("<<getTeleinfo") << endl;

}

/*------------------------------------------------------------------------------*/
/* Test checksum d'un message (Return 1 si checkum ok)				*/
/*------------------------------------------------------------------------------*/
int checksum_ok(char *etiquette, char *valeur, char checksum) 
{
    Serial << F(">>checksum_ok") << endl;

	unsigned char sum = 32 ;		// Somme des codes ASCII du message + un espace
	int i ;
 
	for (i=0; i < strlen(etiquette); i++) sum = sum + etiquette[i] ;
	for (i=0; i < strlen(valeur); i++) sum = sum + valeur[i] ;
	sum = (sum & 63) + 32 ;
        Serial << (etiquette) << F(" ") << (valeur) << (" ") << (checksum) << endl;
	Serial << F("Sum = ")<< (sum) << endl;
	Serial << F("Cheksum = ") << (int(checksum))<< endl;
	if ( sum == checksum) return 1 ;	// Return 1 si checkum ok.
	return 0 ;
    Serial << F("<<checksum_ok") << endl;
}

void lireTrame(char *trame){
    Serial << F(">>lireTrame") << endl;
    int i;
    int j=0;
    for (i=0; i < strlen(trame); i++){
      if (trame[i] != 0x0D) { // Tant qu'on est pas au CR, c'est qu'on est sur une ligne du groupe
          Ligne[j++]=trame[i];
      }
      else { //On vient de finir de lire une ligne, on la décode (récupération de l'etiquette + valeur + controle checksum
          decodeLigne(Ligne);
          memset(Ligne,'\0',32); // on vide la ligne pour la lecture suivante
          j=0;
      }

   }
   Serial << F("<< lireTrame") << endl;

}

int decodeLigne(char *ligne){ 
  //Checksum='\0';
    Serial << F(">>decodeLigne") << endl;
  
   int debutValeur; 
  int debutChecksum;
  // Décomposer en fonction pour lire l'étiquette etc ...  
  debutValeur=lireEtiquette(ligne);
  debutChecksum=lireValeur(ligne, debutValeur);
  lireChecksum(ligne,debutValeur + debutChecksum -1);

  if (checksum_ok(Etiquette, Donnee, Checksum[0])){ // si la ligne est correcte (checksum ok) on affecte la valeur à l'étiquette
    return affecteEtiquette(Etiquette,Donnee);
  } 
  else return 0;
    Serial << F("<<decodeLigne") << endl;

}


int lireEtiquette(char *ligne){
      Serial << F(">>lireEtiquette") << endl;

    int i;
    int j=0;
    memset(Etiquette,'\0',9);
    for (i=1; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Etiquette[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
	//  Serial.print("Etiquette : ");
        //  Serial.println(Etiquette);
          return j+2; // on est sur le dernier caractère de l'etiquette, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }

   }
      Serial << F("<<lireEtiquette") << endl;
}


int lireValeur(char *ligne, int offset){
      Serial << F(">>lireValeur") << endl;
    int i;
    int j=0;
    memset(Donnee,'\0',13);
    for (i=offset; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Donnee[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
	//  Serial.print("Valeur : ");
        //  Serial.println(Donnee);
          return j+2; // on est sur le dernier caractère de la valeur, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }

   }
         Serial << F("<<lireValeur") << endl;

}


void lireChecksum(char *ligne, int offset){
      Serial << F(">>lireChecksum") << endl;
    int i;
    int j=0;
    memset(Checksum,'\0',32);
    for (i=offset; i < strlen(ligne); i++){ 
          Checksum[j++]=ligne[i];
	//  Serial.print("Chekcsum : ");
        //  Serial.println(Checksum);
      }
      
            Serial << F("<< lireChecksum") << endl;


}




int affecteEtiquette(char *etiquette, char *valeur){
      Serial << F(">>affecteEtiquette") << endl;
   Serial<<F("valeur=")<<(valeur) << endl;

 if(strcmp(etiquette,"ADCO") == 0) { 
   memset(ADCO,'\0',12); memcpy(ADCO, valeur,strlen(valeur)); check[1]=1; 
   Serial<<F("ADCO=")<<(ADCO)<<endl;
 }
 else
 if(strcmp(etiquette,"HCHC") == 0) { HCHC = atol(valeur); check[2]=1;
   Serial<<F("HCHC=")<<(HCHC)<<endl;
 }
 else
 if(strcmp(etiquette,"HCHP") == 0) { HCHP = atol(valeur); check[3]=1;
   Serial<<("HCHP=")<< HCHP << endl;
 }
 else
 if(strcmp(etiquette,"HHPHC") == 0) { 
   memset(HHPHC,'\0',2); strcpy(HHPHC, valeur); check[4]=1;
   Serial<<F("HHPHC=")<<(HHPHC)<<endl;
 }
 else
 if(strcmp(etiquette,"PTEC") == 0) { memset(PTEC,'\0',4); memcpy(PTEC, valeur,strlen(valeur)); check[5]=1;
   Serial<<F("PTEC=")<<(PTEC)<<endl;
 }
 else
 if(strcmp(Etiquette,"IINST") == 0) { IINST = atoi(valeur); check[6]=1;
   Serial<< F("IINST=")<< (IINST)<<endl;
 }
 else
 if(strcmp(Etiquette,"PAPP") == 0) { PAPP = atol(valeur); check[7]=1;
   Serial<<F("PAPP=")<<(PAPP)<<endl;
 }
 else
 if(strcmp(Etiquette,"IMAX") == 0) { IMAX = atol(valeur); check[8]=1;
   Serial<<F("IMAX=")<<(IMAX)<<endl;
 }
 else
 if(strcmp(Etiquette,"OPTARIF") == 0) { memset(OPTARIF,'\0',4); memcpy(OPTARIF, valeur,strlen(valeur)); check[9]=1;
   Serial<<F("OPTARIF=")<<(OPTARIF)<<endl;
 }
 else
 if(strcmp(Etiquette,"ISOUSC") == 0) { ISOUSC = atoi(valeur); check[10]=1;
   Serial<< F("ISOUSC=")<<(ISOUSC)<<endl;
 }
 else
 if(strcmp(Etiquette,"MOTDETAT") == 0) { memset(MOTDETAT,'\0',10); memcpy(MOTDETAT, valeur, strlen(valeur)); check[0]=1;
   Serial<<F("MOTDETAT=")<<(MOTDETAT)<<endl;
 }
 else {
   Serial << F("unknown etiquette")<<endl;
 return 0;
 }

 return 1;
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
  if (/*currentMillis > 10000  && currentMillis  > prevEDFReadMillis +30000*/ 0==0) { // une minute
   // getTeleinfo();
      if (cptSerial.available()) {
    uint32_t start = millis();
    Serial << F("debut lecture teleinfo") << endl;
        while (cptSerial.available())
          Serial.write(cptSerial.read() & 0x7F);
    Serial << F(" teleinfo lue en ") << (prevEDFReadMillis-start) << endl;
    prevEDFReadMillis = millis();
      }
  }
 
}
