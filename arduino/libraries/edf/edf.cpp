#include "edf.h"
//#define DEBUG
#define DEBUGLIGNE

/***************** Teleinfo configuration part *******************/
Teleinfos::Teleinfos(){
	reset();
}

/*
Structure d'une ligne de la trame
La composition d'un groupe d'information est la suivante :
• un caractère "Line Feed" LF (00A h) indiquant le début du groupe.
• le champ étiquette dont la longueur est inférieure ou égale à huit caractères,
• un caractère "SPace" SP (020 h) séparateur du champ étiquette et du champ donnée,
• le champ donnée dont la longueur est variable,
• un caractère "SPace" SP (020 h) séparateur du champ donnée et du champ contrôle,
• le champ contrôle se composant d'un caractère contenant la "checksum" dont le calcul est
donné ci-dessous en remarque,
• un caractère "Carriage Return" CR (00D h) indiquant la fin du groupe d'information.
*/
#define ERROR 0
#define EDF_TIMEOUT 5000
#define SERIAL_BUFFER_OVERFLOW 50
#define VALID_FOR 60000
int Teleinfos::read(SoftwareSerial &cptSerial, Print &debug) {
	#ifdef DEBUG
		debug << F(">>getTeleinfo") << endl;
	#endif
	uint32_t startMillis = millis();
	if ((lastRefresh !=0) && (startMillis - lastRefresh < VALID_FOR)) {
		return 1;
	}
	cptSerial.begin(1200);
	/* vider les infos de la dernière trame lue */
	memset(Ligne,'\0',sizeof(Ligne)); 
	int trameComplete=0;
	
	reset();
	while (!trameComplete) {
		while(CaractereRecu != 0x02) {
			if (millis()-startMillis > EDF_TIMEOUT) {
				cptSerial.end();
				return ERROR;
			}
		// boucle jusqu'a "Start Text 002" début de la trame
			if (cptSerial.available()) {
				CaractereRecu = cptSerial.read() & 0x7F;
			}
		}

		while (CaractereRecu != 0x03) {
			i=0; 
			while(CaractereRecu != 0x03 && CaractereRecu != 0x0D /* fin de ligne */) { 
				if (millis()-startMillis > EDF_TIMEOUT) {
					cptSerial.end();
					return ERROR;
				}
				// Tant qu'on est pas arrivé à "EndText 003" Fin de trame ou que la trame est incomplète
				int available = cptSerial.available();
				#ifdef DEBUG
				if (available > SERIAL_BUFFER_OVERFLOW) {
					debug << "O " << available << endl;
				}
				#endif
				if (available) {
					CaractereRecu = cptSerial.read() & 0x7F;
					Ligne[i++]=CaractereRecu;
				}	
			}
			if (i > 0) { 
				Ligne[i++] = '\0';
				#ifdef DEBUGLIGNE
				debug << Ligne << endl;
				#endif
				decodeLigne(Ligne, debug);
				memset(Ligne,'\0',sizeof(Ligne)); // on vide la ligne pour la lecture suivante
				if (CaractereRecu ==  0x0D) {
					CaractereRecu = '\0';
				}
			}
		}

		// on vérifie si on a une trame complète ou non
		trameComplete = isTrameComplete(debug);
		#ifdef DEBUG
		debug << F("complete ? ") << trameComplete << endl;
		#endif
	}
	#ifdef DEBUG
		debug <<  F("<<getTeleinfo") << endl;
	#endif
	cptSerial.end();
	lastRefresh = millis(); 
	return millis() - startMillis;
}
/*void Teleinfos::lireTrame(char *trame, Print& debug) {
	int i;
	int j=0;
	for (i=0; i < strlen(trame); i++){
		if (trame[i] != 0x0D) { // Tant qu'on est pas au CR, c'est qu'on est sur une ligne du groupe
			Ligne[j++]=trame[i];
		} else { //On vient de finir de lire une ligne, on la décode (récupération de l'etiquette + valeur + controle checksum
			decodeLigne(Ligne, debug);
			memset(Ligne,'\0',32); // on vide la ligne pour la lecture suivante
			j=0;
		}
	}
}
*/
int Teleinfos::decodeLigne(char *ligne, Print& debug) { 
	int debutValeur; 
	int debutChecksum;
	// Décomposer en fonction pour lire l'étiquette etc ...  
	debutValeur=lireEtiquette(ligne,debug);
	debutChecksum=lireValeur(ligne, debutValeur,debug);
	lireChecksum(ligne,debutValeur + debutChecksum -1,debug);

	if (checksum_ok(Etiquette, Donnee, Checksum[0], debug)){ // si la ligne est correcte (checksum ok) on affecte la valeur à l'étiquette
		return set(Etiquette,Donnee,debug);
	} else {
		return 0;
	}
}

/*------------------------------------------------------------------------------*/
/* Test checksum d'un message (Return 1 si checkum ok)				*/
/*------------------------------------------------------------------------------*/
int Teleinfos::checksum_ok(char *etiquette, char *valeur, char checksum, Print& debug) {
	unsigned char sum = 32 ;		// Somme des codes ASCII du message + un espace
	int i ;
 
	for (i=0; i < strlen(etiquette); i++) sum = sum + etiquette[i] ;
	for (i=0; i < strlen(valeur); i++) sum = sum + valeur[i] ;
	sum = (sum & 63) + 32 ;
	if ( sum == checksum) return 1 ;	// Return 1 si checkum ok.
	return 0 ;
}


int Teleinfos::lireEtiquette(char *ligne, Print& debug){
    int i;
    int j=0;
    memset(Etiquette,'\0',sizeof(Etiquette));
    for (i=1; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Etiquette[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
          return j+2; // on est sur le dernier caractère de l'etiquette, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }
   }
}


int Teleinfos::lireValeur(char *ligne, int offset, Print& debug){
    int i;
    int j=0;
    memset(Donnee,'\0',sizeof(Donnee));
    for (i=offset; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Donnee[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
          return j+2; // on est sur le dernier caractère de la valeur, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }
	}
}


void Teleinfos::lireChecksum(char *ligne, int offset, Print& debug){
	int i;
	int j=0;
	memset(Checksum,'\0',sizeof(Checksum));
	for (i=offset; i < strlen(ligne); i++){ 
		Checksum[j++]=ligne[i];
	}
}

byte ADCO_idx = 0;
byte OPTARIF_idx = ADCO_idx + 1;
byte ISOUSC_idx = OPTARIF_idx + 1;
byte EJPHN_idx = ISOUSC_idx + 1;
byte EJPHPM_idx = EJPHN_idx + 1;
byte PEJP_idx = EJPHPM_idx + 1;
byte PTEC_idx = PEJP_idx + 1;
byte IINST1_idx = PTEC_idx + 1;
byte IINST2_idx = IINST1_idx + 1;
byte IINST3_idx = IINST2_idx + 1;
byte IMAX1_idx = IINST3_idx + 1;
byte IMAX2_idx = IMAX1_idx + 1;
byte IMAX3_idx = IMAX2_idx + 1;
byte PMAX_idx = IMAX3_idx + 1;
byte PAPP_idx = PMAX_idx + 1;
byte MOTDETAT_idx = PAPP_idx + 1;
byte PPOT_idx = MOTDETAT_idx + 1;
byte BASE_idx = PPOT_idx + 1;
byte IINST_idx = BASE_idx + 1;
byte ADPS_idx = IINST_idx + 1;
byte IMAX_idx = ADPS_idx + 1;

unsigned long maskEJPComplet = 
	(1 << ADCO_idx) 
	| (1 << EJPHN_idx)
	| (1 << EJPHPM_idx)
	| (1 << IINST1_idx)
	| (1 << IINST2_idx)
	| (1 << IINST3_idx)
	| (1 << IMAX1_idx)
	| (1 << IMAX2_idx)
	| (1 << IMAX3_idx)
	| (1 << PMAX_idx)
	| (1 << PAPP_idx);

unsigned long maskNormalComplet = 
	(1 << ADCO_idx) 
	| (1 << BASE_idx)
	| (1 << PTEC_idx)
	| (1 << IINST_idx)
	| (1 << IMAX_idx)
	| (1 << PAPP_idx);

void Teleinfos::setVariable (char * const variable, char const * const valeur, int variableLength, byte idx) {
	memset(variable,'\0',variableLength); memcpy(variable, valeur,strlen(valeur));
	etiquettesLues |= (1L << idx); 
}
int Teleinfos::set(char *etiquette, char *valeur, Print& debug) {
	long etiquettesLuesBefore = etiquettesLues; 
	#ifdef DEBUG
		//debug << " set " << etiquette << " = " << valeur << endl;
	#endif
	if(strcmp(etiquette,"ADCO") == 0) { 
		setVariable (ADCO, valeur, 13, ADCO_idx);
	} else if(strcmp(etiquette,"OPTARIF") == 0) { 
		setVariable (OPTARIF, valeur, 5, OPTARIF_idx);
	} else if(strcmp(etiquette,"ISOUSC") == 0) { 
		ISOUSC = atoi(valeur); 
		etiquettesLues |= (1L << ISOUSC_idx); 
	} else if(strcmp(etiquette,"EJPHN") == 0) { 
		EJPHN = atol(valeur);
		etiquettesLues |= (1L << EJPHN_idx);
	} else if(strcmp(etiquette,"EJPHPM") == 0) {
		EJPHPM = atol(valeur);
		etiquettesLues |= (1L << EJPHPM_idx);
	} else if(strcmp(etiquette,"BASE") == 0) { 
		BASE = atol(valeur);
		etiquettesLues |= (1L << BASE_idx);
	} else if(strcmp(etiquette,"PEJP") == 0) { 
		PEJP = atoi( valeur); 
		etiquettesLues |= (1L << PEJP_idx); 
	} else if(strcmp(etiquette,"PTEC") == 0) { 
		setVariable (PTEC, valeur, 5, PTEC_idx);
	} else if(strcmp(etiquette,"IINST") == 0) { 
		IINST = atoi(valeur); 
		etiquettesLues |= (1L << IINST_idx); 
	} else if(strcmp(etiquette,"IINST1") == 0) { 
		IINST1 = atoi(valeur); 
		etiquettesLues |= (1L << IINST1_idx); 
	} else if(strcmp(etiquette,"IINST2") == 0) { 
		IINST2 = atoi(valeur); 
		etiquettesLues |= (1L << IINST2_idx); 
	} else if(strcmp(etiquette,"IINST3") == 0) { 
		IINST3 = atoi(valeur); 
		etiquettesLues |= (1L << IINST3_idx); 
	} else if(strcmp(etiquette,"IMAX") == 0) { 
		IMAX = atol(valeur); 
		etiquettesLues |= (1L << IMAX_idx); 
	} else if(strcmp(etiquette,"IMAX1") == 0) { 
		IMAX1 = atol(valeur); 
		etiquettesLues |= (1L << IMAX1_idx); 
	} else if(strcmp(etiquette,"IMAX2") == 0) { 
		IMAX2 = atol(valeur); 
		etiquettesLues |= (1L << IMAX2_idx); 
	} else if(strcmp(etiquette,"IMAX3") == 0) { 
		IMAX3 = atol(valeur); 
		etiquettesLues |= (1L << IMAX3_idx); 
	} else if(strcmp(etiquette,"PMAX") == 0) { 
		PMAX = atol(valeur); 
		etiquettesLues |= (1L << PMAX_idx); 
	} else if(strcmp(etiquette,"PAPP") == 0) { 
		PAPP = atol(valeur); 
		etiquettesLues |= (1L << PAPP_idx); 
	} else if(strcmp(etiquette,"MOTDETAT") == 0) { 
		setVariable (MOTDETAT, valeur, 7, MOTDETAT_idx);
	} else if(strcmp(etiquette,"PPOT") == 0) { 
		setVariable (PPOT, valeur, 3, PPOT_idx);
	/*} else if(strcmp(etiquette,"HCHC") == 0) { 
		HCHC = atol(valeur); etiquettesLues ++; 
	} else if(strcmp(etiquette,"HCHP") == 0) { 
		HCHP = atol(valeur); etiquettesLues ++; 
	} else if(strcmp(etiquette,"HHPHC") == 0) { 
		memset(HHPHC,'\0',2); strcpy(HHPHC, valeur); etiquettesLues ++; 
	*/
	} else {
		#ifdef DEBUG
			debug <<  F(" unknown etiquette ") <<  etiquette << endl;
		#endif
	}
	#ifdef DEBUG
		//debug << etiquette << " : " << valeur << "(" << etiquettesLuesBefore << " -> "<<etiquettesLues << ")" << endl;
	#endif

	return etiquettesLues != etiquettesLuesBefore;
}
	
int Teleinfos::isTrameComplete(Print& debug) const {
	// 0 si non, 1 si oui
	if (strstr(OPTARIF, "EJP") !=NULL) {
		#ifdef DEBUG 
			//debug << "OPTARIF reconnue " << endl;
		#endif
		return (maskEJPComplet & etiquettesLues) == maskEJPComplet;
	}else if (strstr(OPTARIF, "BASE") !=NULL) {
		#ifdef DEBUG 
			//debug << "OPTARIF reconnue " << endl;
		#endif
		return (maskNormalComplet & etiquettesLues) == maskNormalComplet;
	} else {
		#ifdef DEBUG 
			debug << F("OPTARIF inconnue [") <<OPTARIF <<("]")<< endl;
		#endif
		return 0;
	}
}
