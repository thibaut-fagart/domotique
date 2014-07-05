
#ifndef FUEL_H
#define FUEL_H
#include <EEPROM.h>

/****************************************
 * Fuel management
 */

static char const oidBurningTime[] PROGMEM   = "1.3.6.1.4.1.36582.10";  // read-only  (counter)
static char const oidBurntFuel[] PROGMEM   = "1.3.6.1.4.1.36582.11";  // read-only  (SNMP_SYNTAX_COUNTER64)
static char const oidRemainingFuel[] PROGMEM   = "1.3.6.1.4.1.36582.12";  // read-only  (gauge)

const uint32_t FUEL_TANK_CAPACITY = 2000;
const float fuel_flow_l_per_hour = 4.6f;
const int seconds_per_hour = 3600;

// cumulated burning time (seconds), updated in real time by the main loop
uint32_t burningTime_s = 0;
// intermediate time counter for precision
uint32_t burningTime_ms = 0;
// fuel supposed to be remaining in the fuel tank
uint32_t remainingFuel_l = FUEL_TANK_CAPACITY;
uint32_t EEPROM_REMAINING_FUEL_OFFSET = 0;
uint32_t EEPROM_BURNT_FUEL_OFFSET = EEPROM_REMAINING_FUEL_OFFSET +4;
uint64_t burningTime_sOnLastSave;
#define DELTA_BURNT_L_BEFORE_SAVE  1

void toBytes(uint32_t i, byte bytes[4]) {
  uint32_t t = i;
  bytes[3] = (t & 255);
  t = t >> 8;
  bytes[2] = (t & 255);
  t = t >> 8;
  bytes[1] = (t & 255);
  t = t >> 8;
  bytes[0] = (t & 255);
}

uint32_t fromBytes(byte bytes[4]) {
  uint32_t _255 = 255;
  uint32_t ret = _255 & bytes[3] ;
  ret |= (_255 & bytes[2]) << 8;
  ret |=(_255 & bytes[1]) << 16;
  ret |=(_255 & bytes[0]) << 24;
  return ret;
}

void storeInEEPROM (uint32_t offset, uint32_t value) {
	byte bytes[4];
	toBytes(value,  bytes);
	for (int i =0; i< 4; i++) {
		EEPROM.write(offset+i,bytes[i]);
	}
	#ifdef DEBUG
	Serial << "storeInEEPROM [" << offset << " ] = " << value << endl;
	#endif
}
uint32_t readFromEEPROM (uint32_t offset) {
	byte bytes[4];
	for (int i =0; i< 4; i++) {
		bytes[i] = EEPROM.read(offset+i);
	}
	uint32_t value = fromBytes(bytes);
	#ifdef DEBUG
	Serial << "readFromEEPROM  [" << offset << " ]= " << value << endl;
	#endif
	return value;
	
}

// EEPROM values are initially all 255
int isSet(uint32_t value) {
	byte bytes[4];
	toBytes(value, bytes);
	for (int i =0; i< 4; i++) {
		if (bytes[i] != 255) {
			return 1==1;
		}
	}
	return 1 != 1;
}

void initFuelFromEEPROM() {
	uint32_t stored =  readFromEEPROM(EEPROM_REMAINING_FUEL_OFFSET);
	if (isSet(stored)) {
		Serial << "stored " << stored << endl;
		remainingFuel_l = stored;
		Serial << "init remainingFuel_l " << remainingFuel_l << endl;
	}
	
	stored = readFromEEPROM(EEPROM_BURNT_FUEL_OFFSET);
	if (isSet(stored)) {
		burningTime_s = (((uint64_t)stored ) *3600 )/fuel_flow_l_per_hour;
		Serial << "init burningTime_s " << burningTime_s << endl ;
	}
	
}

int handleFuelOIDs(SNMP_PDU &pdu, char oid[SNMP_MAX_OID_LEN]) {
	SNMP_ERR_CODES status;
    if (strcmp_P(oid, oidBurningTime ) == 0) {
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-write
        uint32_t newBurningTime = burningTime_s;
        status = pdu.VALUE.decode(&newBurningTime);
#ifdef DEBUG
        Serial << F("updating burningTime ") << burningTime_s << F(" to ") << newBurningTime << endl;
#endif
        burningTime_s = newBurningTime;
		storeInEEPROM(EEPROM_BURNT_FUEL_OFFSET, (uint32_t)(((uint64_t) burningTime_s ) *fuel_flow_l_per_hour)/ 3600);
		burningTime_sOnLastSave = burningTime_s;
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      } 
      else {
        status = pdu.VALUE.encode(SNMP_SYNTAX_COUNTER, burningTime_s);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
    } 
    else if (strcmp_P(oid, oidBurntFuel ) == 0) {
      if ( pdu.type == SNMP_PDU_SET ) {
        // response packet from set-request - object is read-only
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = SNMP_ERR_READ_ONLY;
      } 
      else {
        uint64_t usedFuel_ml =  (((uint64_t) burningTime_s ) *fuel_flow_l_per_hour)/ 3.6;
#ifdef DEBUG
        Serial << F(" consumed fuel since reset ") << (uint32_t)usedFuel_ml << endl;
#endif
		uint32_t burntSinceLastSave = ((burningTime_s - burningTime_sOnLastSave)* fuel_flow_l_per_hour *3600);
		if  (burntSinceLastSave > DELTA_BURNT_L_BEFORE_SAVE) {
			burningTime_sOnLastSave = burningTime_s;
			uint32_t burntToSave = (((uint64_t) burningTime_s ) *fuel_flow_l_per_hour)/ 3600;
			storeInEEPROM(EEPROM_BURNT_FUEL_OFFSET, burntToSave);
		}
        status = pdu.VALUE.encode(SNMP_SYNTAX_COUNTER64, usedFuel_ml);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }      
    } 
    else if (strcmp_P(oid, oidRemainingFuel ) == 0) {
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
		storeInEEPROM (EEPROM_REMAINING_FUEL_OFFSET, remainingFuel_l);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      } 
      else {
        uint64_t usedFuel_ml =  (((uint64_t) burningTime_s ) *fuel_flow_l_per_hour)/ 3.6;
        uint32_t temp_remainingFuel_l = remainingFuel_l - (usedFuel_ml/1000);
#ifdef DEBUG
        Serial << F(" remaining fuel since reset ") << temp_remainingFuel_l << F(", init fuel tank ")<<remainingFuel_l << endl;
#endif
        status = pdu.VALUE.encode(SNMP_SYNTAX_GAUGE, temp_remainingFuel_l);
        pdu.type = SNMP_PDU_RESPONSE;
        pdu.error = status;
      }
    } else  {
		return 0==1;
	}
	return 0==0;

}
void incrementBurningTimeIfBurning(int pin, uint32_t stepMs) {
    if (digitalRead(pin) ==1) {
      // currentlyBurning
      burningTime_ms +=stepMs;
      if (burningTime_ms > 1000) {
        burningTime_s +=1;
#ifdef DEBUG
        //        Serial << F("burning for ") << burningTime_s << endl;
#endif
        burningTime_ms -=1000;
      }
    }
}
#endif