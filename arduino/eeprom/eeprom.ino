#include <Streaming.h>
#include <EEPROM.h>


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
}
uint32_t readFromEEPROM (uint32_t offset) {
	byte bytes[4];
	for (int i =0; i< 4; i++) {
		bytes[i] = EEPROM.read(offset+i);
	}
	return fromBytes(bytes);
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

uint32_t randomUint() {
  byte b;
  b = random(255);
  Serial << "random :  "<< b;
  uint32_t ret=b;
  b = random(255);
  Serial << " " << b;
  ret = (ret << 8) |  b;
  b = random(255);
  Serial << " " << b;
  ret = (ret << 8) |  b;
  b = random(255);
  Serial << " " << b;
  ret = (ret << 8) |  b;
Serial << endl;
return ret;
}

void setup() {
  Serial.begin(9600);
  Serial << "setup " << endl;
  delay(2000);
//  storeInEEPROM(0, 444);
  uint32_t i =  readFromEEPROM(0);
  Serial << "readFromEEPROM(0) " << i << " isSet ? " << isSet(i) << endl;
  Serial << "readFromEEPROM(4) " << readFromEEPROM(4) << " isSet ? " << isSet(i) << endl;
  byte bytes[4];
  toBytes(i, bytes);
  for (int j =0; j < 4; j++) {
    Serial << bytes[j] << " " ; 
  }
  Serial << endl;
}

int a = 0;
int value;
void loop()
{
  value = EEPROM.read(a);

  Serial << a << "\t" << value << endl;

  a = a + 1;

  if (a == 512)
    a = 0;

  delay(500);
}

/*
void loop()
{
  uint32_t   i = randomUint();
 
  byte bytes [4] ;
  toBytes(i, bytes);

  Serial << i << "=" ;
  for (int i =0 ; i <4; i++) {
   Serial << bytes[i] << "," ;
  }
  Serial << endl;
  uint32_t merged = (fromBytes(bytes));
  Serial << merged << " OK ? " << (merged - i) << endl;;
  delay (1000);
 }*/
