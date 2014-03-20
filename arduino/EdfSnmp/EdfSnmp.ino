#include <Streaming.h>

#include <DHT.h>
#include <SoftwareSerial.h>
#include <edf.h>

int dht22EdfPin = 4; 
int EdfRxPin    = 9;
int EdfTxPin    = 8;

SoftwareSerial EdfSerial(EdfRxPin, EdfTxPin);

void setup() {
        Serial.begin(1200);     // opens serial port, sets data rate to 1200 bps
        EdfSerial.begin(1200);
}

void loop() {
  Teleinfos teleinfos;
  getTeleinfo(EdfSerial, teleinfos, Serial);
  Serial << "teleinfos {" <<teleinfos << "}" << endl;

}
