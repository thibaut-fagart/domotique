#ifndef edf_h
#define edf_h

#include "Arduino.h"
#include <SoftwareSerial.h>
#include <Streaming.h>
#include <Flash.h>

/*
reference EDF : http://www.planete-domotique.com/notices/ERDF-NOI-CPT_O2E.pdf
Si l'intensité mesurée sur l'une quelconque des phases dépasse la valeur de réglage du disjoncteur, le cycle
d'émission des trames longues s'interrompt à la fin de l'émission du groupe d'information en cours. La liaison
de télé-information émet alors des cycles composés de 20 trames courtes et d'une trame longue tant que le
dépassement persiste et pendant 1 minute après sa disparition.


Trame courtes
int(3) ADIR1 , ADIR2, ADIR3 Avertissement de Dépassement d'intensité de réglage par phase (en amperes)
char[12] ADCO Adresse du compteur 
int(3) IINST1 , IINST2, IINST3 Adresse du compteur ADCO 12 Intensité Instantanée pour les 3 phases 1, 2 et 3


    Préavis EJP si option = EJP : PEJP ( 2 car.) 30mn avant période EJP, en minutes
    Avertissement de dépassement de puissance souscrite : ADPS ( 3 car. unité = ampères) (message émis uniquement en cas de dépassement effectif, dans ce cas il est immédiat)
    

*/

/*
rappels sur 'const'
see http://duramecho.com/ComputerInformation/WhyHowCppConst.html
    const int * Constant2 :  Constant2 is a variable pointer to a constant integer
	int const * Constant2 : same as above
	int * const Constant3 : Constant3 is constant pointer to a variable integer
    int const * const Constant4 : declares that Constant4 is constant pointer to a constant integer.
	Basically ‘const’ applies to whatever is on its immediate left (other than if there is nothing there in which case it applies to whatever is its immediate right)
	
	big_structure_type const &Parameter1 : const pointer
*/

struct Teleinfos {
	uint32_t lastRefresh;
	char CaractereRecu;
	char Checksum[2] ;
	char Ligne[32];
	char Etiquette[9] ;
	char Donnee[13] ;
//	char Trame[512] ;
	int i ;
	int j ;


	char ADCO[13]; // 041330071201 - N° d’identification du compteur : ADCO (12 caractères)
	char OPTARIF[5]; // EJP. " Option tarifaire (type d’abonnement) : OPTARIF (4 car.)
	int ISOUSC ; //30 9 Intensité souscrite : ISOUSC ( 2 car. unité = ampères)
	uint32_t BASE; // 002727095 E Index normales ( 9 car. unité = Wh)
	uint32_t EJPHN; // 002727095 E Index heures normales si option = EJP : EJP HN ( 9 car. unité = Wh)
	uint32_t EJPHPM; // 000100755 F Index heures de pointe mobile si option = EJP : EJP HPM ( 9 car. unité = Wh)
	uint32_t PEJP; // int (2) Préavis Début EJP (30 min avant) , en minutes
	char PTEC [5]; //HN.. ^ Période tarifaire en cours : PTEC ( 4 car.)
	uint32_t IINST; // 002 J Intensité instantanée : IINST ( 3 car. unité = ampères)
	uint32_t IINST1; // 002 J Intensité instantanée : IINST ( 3 car. unité = ampères)
	uint32_t IINST2; // 000 I Intensité instantanée : IINST ( 3 car. unité = ampères)
	uint32_t IINST3; // 001 K Intensité instantanée : IINST ( 3 car. unité = ampères)
	uint32_t IMAX; //014 5 Intensité maximale : IMAX ( 3 car. unité = ampères)
	uint32_t IMAX1; //014 5 Intensité maximale : IMAX ( 3 car. unité = ampères)
	uint32_t IMAX2; //018 : Intensité maximale : IMAX ( 3 car. unité = ampères)
	uint32_t IMAX3; // 042 8 Intensité maximale : IMAX ( 3 car. unité = ampères)
	uint32_t PMAX; // 14370 5 Puissance maximale triphasée atteinte (Watts)
	uint32_t PAPP; // 00690 0 Puissance apparente : PAPP ( 5 car. unité = Volt.ampères)
	char MOTDETAT[7];// 000000 B Mot d’état (autocontrôle) : MOTDETAT (6 car.)
	char PPOT[3]; // 00 # Présence des potentiels
	
	uint32_t etiquettesLues;
	
	Teleinfos();
	int read(SoftwareSerial &cptSerial, Print &debug);
	int set(char *etiquette, char *valeur, Print &debug) ;
	int isTrameComplete(Print &debug) const; 
	void setVariable (char * const variable, char const * const valeur, int variableLength, byte idx) ;
	int checksum_ok(char *etiquette, char *valeur, char checksum, Print& debug) ;
	void lireTrame(char *trame, Print& debug) ;
	int decodeLigne(char *ligne, Print& debug);
	int lireEtiquette(char *ligne, Print& debug);
	int lireValeur(char *ligne, int offset, Print& debug);
	void lireChecksum(char *ligne, int offset, Print& debug);
	int affecteEtiquette(char *etiquette, char *valeur, Print& debug);
	
	void reset() {
		memset(ADCO,'\0',13);
		memset(OPTARIF,'\0',5);
		ISOUSC = 0;
		BASE = 0L; 
		EJPHN = 0L; 
		EJPHPM=0L; 
		PEJP= 0;
		memset(PTEC ,'\0',5);
		IINST=0; 
		IINST1=0; 
		IINST2=0; 
		IINST3=0; 
		IMAX=0l;
		IMAX1=0l;
		IMAX2=0l; 
		IMAX3=0l; 
		PMAX=0l; 
		PAPP=0l; 
		memset(MOTDETAT,'\0',7);
		memset(PPOT,'\0',3 );
		
		etiquettesLues=0l;
	
	}
	void print(Print &debug) const {
		debug << "ADCO :" << ADCO << endl;
		debug << "OPTARIF :" << OPTARIF<< endl;
		debug << "ISOUSC :" << ISOUSC<< endl;
		debug << "BASE :" << BASE<< endl;
		debug << "EJPHN :" << EJPHN<< endl;
		debug << "EJPHPM :" << EJPHPM<< endl;
		debug << "PEJP :" << PEJP << endl;
		debug << "PTEC :" << PTEC << endl;
		debug << "IINST :" << IINST << endl;
		debug << "IINST1 :" << IINST1 << endl;
		debug << "IINST2 :" << IINST2 << endl;
		debug << "IINST3 :" << IINST3<< endl;
		debug << "IMAX :" << IMAX << endl;
		debug << "IMAX1 :" << IMAX1 << endl;
		debug << "IMAX2 :" << IMAX2 << endl;
		debug << "IMAX3 :" << IMAX3 << endl;
		debug << "PMAX :" << PMAX << endl;
		debug << "PAPP :" << PAPP << endl;
		debug << "MOTDETAT :" << MOTDETAT << endl;
		debug << "PPOT :" << PPOT<< endl;
	}
};

inline Print &operator <<(Print &obj, const Teleinfos &arg)
{ arg.print(obj); return obj; }



#endif