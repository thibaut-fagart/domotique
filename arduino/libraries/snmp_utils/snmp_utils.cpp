#include "snmp_utils.h"

/**
 * if pdu type is GET, writes currentValue into the pdu's value.
 * if pdu type is SET AND readonly == TRUE, read the incoming value and stores it in currentValue.
 */
void handleStringOID (SNMP_PDU* pdu, char* currentValue, boolean readonly) {
	if ( pdu->type == SNMP_PDU_SET  ) {
		if (readonly) {
			// response p	acket from set-request - object is read-only
			pdu->type = SNMP_PDU_RESPONSE;
			pdu->error = SNMP_ERR_READ_ONLY;
		} else {
			pdu->type = SNMP_PDU_RESPONSE;
			pdu->error = pdu->VALUE.decode(currentValue, strlen(currentValue));
		}
	} else {
		// response packet from get-request
		pdu->type = SNMP_PDU_RESPONSE;
		pdu->error = pdu->VALUE.encode(SNMP_SYNTAX_OCTETS, currentValue);
	}
}

void handleIntOID(SNMP_PDU* pdu, int* currentValue, boolean readonly) {
      if ( pdu->type == SNMP_PDU_SET ) {
        if (readonly) {
          // response packet from set-request - object is read-only
          pdu->type = SNMP_PDU_RESPONSE;
          pdu->error = SNMP_ERR_READ_ONLY;
        } else {
          pdu->type = SNMP_PDU_RESPONSE;
          pdu->error = pdu->VALUE.decode(currentValue);
        }
      } else {
        pdu->type = SNMP_PDU_RESPONSE;
        pdu->error =  pdu->VALUE.encode(SNMP_SYNTAX_INT, *currentValue);
      }
}

void handleReadInt(SNMP_PDU* pdu, int value) {
    handleIntOID(pdu,&value,TRUE);
}

/**
 * reads the current temperature from the provided dht and stores it in the pdu
 */ 
void handleReadTemperature(SNMP_PDU* pdu, DHT* dht) {
        int localValue = (int)(10 * (dht-> readTemperature(false)));
	handleIntOID(pdu, &localValue, TRUE);
}

/**
 * reads the current humidity from the provided dht and stores it in the pdu
 */ 
void handleReadHumidity(SNMP_PDU* pdu, DHT* dht) {
        int localValue = (int)(10 * (dht-> readHumidity()));
	handleIntOID(pdu, &localValue, TRUE);
}
