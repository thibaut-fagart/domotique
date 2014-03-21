#ifndef utils_divers_h
#define utils_divers_h

#include "Arduino.h"
#include "DHT.h"
#include "Agentuino.h"
#include "Streaming.h"

#define TRUE 1
#define FALSE 0

/**
 * if pdu type is GET, writes currentValue into the pdu's value.
 * if pdu type is SET AND readonly == TRUE, read the incoming value and stores it in currentValue.
 */
void handleStringOID (SNMP_PDU* pdu, char* currentValue, boolean readonly);
 
void handleIntOID(SNMP_PDU* pdu, int* value, boolean readonly);

void handleUInt32OID(SNMP_PDU* pdu, uint32_t &value, boolean readonly);    
void handleReadUInt32(SNMP_PDU* pdu, uint32_t value);
/**
 * reads the current temperature from the provided dht and stores it in the pdu
 */ 
void handleReadTemperature(SNMP_PDU* pdu, DHT* dht);

/**
 * reads the current humidity from the provided dht and stores it in the pdu
 */ 
void handleReadHumidity(SNMP_PDU* pdu, DHT* dht);

#endif
