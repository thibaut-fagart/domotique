#ifndef edf_h
#define edf_h

#include "Arduino.h"
#include <Flash.h>
#include <Streaming.h> 
#include <SoftwareSerial.h>

void getTeleinfo(SoftwareSerial& edfSerials, Print& serial) ;
void lireTrame(char *trame, Print& debug);
int decodeLigne(char *ligne, Print& debug);
int lireEtiquette(char *ligne, Print& debug);
int lireValeur(char *ligne, int offset, Print& debug);
void lireChecksum(char *ligne, int offset, Print& debug);
int affecteEtiquette(char *etiquette, char *valeur, Print& debug);

#endif