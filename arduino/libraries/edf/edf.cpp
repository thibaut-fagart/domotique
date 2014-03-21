#include "edf.h"

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

int check[11];  // Checksum by etiquette
int trame_ok = 1; // global trame checksum flag
int finTrame=0;


void getTeleinfo(SoftwareSerial& cptSerial, Teleinfos& teleinfos, Print& debug) {
	#ifdef DEBUG
		debug << ">>getTeleinfo" << endl;
	#endif
	/* vider les infos de la dernière trame lue */
	memset(Ligne,'\0',32); 
	memset(Trame,'\0',512);
	int trameComplete=0;
	
	teleinfos.reset();
	while (!trameComplete){
		while(CaractereRecu != 0x02) {
		// boucle jusqu'a "Start Text 002" début de la trame
			if (cptSerial.available()) {
				CaractereRecu = cptSerial.read() & 0x7F;
			}
		}

		i=0; 
		while(CaractereRecu != 0x03) { 
			// Tant qu'on est pas arrivé à "EndText 003" Fin de trame ou que la trame est incomplète
			if (cptSerial.available()) {
				CaractereRecu = cptSerial.read() & 0x7F;
				Trame[i++]=CaractereRecu;
			}	
		}
		finTrame = i;
		Trame[i++]='\0';

		#ifdef DEBUG
			debug << "Trame [" << Trame <<  "]" << endl;
		#endif

		lireTrame(Trame, teleinfos, debug);	

		// on vérifie si on a une trame complète ou non
		trameComplete = teleinfos.isTrameComplete(debug);
	}
	#ifdef DEBUG
		debug <<  "<<getTeleinfo" << endl;
	#endif

}

/*------------------------------------------------------------------------------*/
/* Test checksum d'un message (Return 1 si checkum ok)				*/
/*------------------------------------------------------------------------------*/
int checksum_ok(char *etiquette, char *valeur, char checksum, Print& debug) {
	unsigned char sum = 32 ;		// Somme des codes ASCII du message + un espace
	int i ;
 
	for (i=0; i < strlen(etiquette); i++) sum = sum + etiquette[i] ;
	for (i=0; i < strlen(valeur); i++) sum = sum + valeur[i] ;
	sum = (sum & 63) + 32 ;
	if ( sum == checksum) return 1 ;	// Return 1 si checkum ok.
	return 0 ;
}

void lireTrame(char *trame, Teleinfos& teleinfos, Print& debug){
	int i;
	int j=0;
	for (i=0; i < strlen(trame); i++){
		if (trame[i] != 0x0D) { // Tant qu'on est pas au CR, c'est qu'on est sur une ligne du groupe
			Ligne[j++]=trame[i];
		} else { //On vient de finir de lire une ligne, on la décode (récupération de l'etiquette + valeur + controle checksum
			decodeLigne(Ligne,teleinfos, debug);
			memset(Ligne,'\0',32); // on vide la ligne pour la lecture suivante
			j=0;
		}
	}
}

int decodeLigne(char *ligne, Teleinfos& teleinfos, Print& debug){ 
	int debutValeur; 
	int debutChecksum;
	// Décomposer en fonction pour lire l'étiquette etc ...  
	debutValeur=lireEtiquette(ligne,debug);
	debutChecksum=lireValeur(ligne, debutValeur,debug);
	lireChecksum(ligne,debutValeur + debutChecksum -1,debug);

	if (checksum_ok(Etiquette, Donnee, Checksum[0], debug)){ // si la ligne est correcte (checksum ok) on affecte la valeur à l'étiquette
		return teleinfos.set(Etiquette,Donnee,debug);
	} else {
		return 0;
	}
}

int lireEtiquette(char *ligne, Print& debug){
    int i;
    int j=0;
    memset(Etiquette,'\0',9);
    for (i=1; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Etiquette[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
          return j+2; // on est sur le dernier caractère de l'etiquette, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }

   }
}


int lireValeur(char *ligne, int offset, Print& debug){
    int i;
    int j=0;
    memset(Donnee,'\0',13);
    for (i=offset; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Donnee[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
          return j+2; // on est sur le dernier caractère de la valeur, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }
	}
}


void lireChecksum(char *ligne, int offset, Print& debug){
	int i;
	int j=0;
	memset(Checksum,'\0',32);
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

void Teleinfos::setVariable (char* variable, char* valeur, int variableLength, byte idx) {
	memset(variable,'\0',variableLength); memcpy(variable, valeur,strlen(valeur));
	etiquettesLues |= (1L << idx); 
}
int Teleinfos::set(char *etiquette, char *valeur, Print& debug) {
	long etiquettesLuesBefore = etiquettesLues; 
	#ifdef DEBUG
		debug << " set " << etiquette << " = " << valeur << endl;
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
	} else if(strcmp(etiquette,"PEJP") == 0) { 
		PEJP = atoi( valeur); 
		etiquettesLues |= (1L << PEJP_idx); 
	} else if(strcmp(etiquette,"PTEC") == 0) { 
		setVariable (PTEC, valeur, 5, PTEC_idx);
	} else if(strcmp(etiquette,"IINST1") == 0) { 
		IINST1 = atoi(valeur); 
		etiquettesLues |= (1L << IINST1_idx); 
	} else if(strcmp(etiquette,"IINST2") == 0) { 
		IINST2 = atoi(valeur); 
		etiquettesLues |= (1L << IINST2_idx); 
	} else if(strcmp(etiquette,"IINST3") == 0) { 
		IINST3 = atoi(valeur); 
		etiquettesLues |= (1L << IINST3_idx); 
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
			debug <<  " unknown etiquette " <<  etiquette << endl;
		#endif
	}
	#ifdef DEBUG
		debug << etiquette << " : " << valeur << "(" << etiquettesLuesBefore << " -> "<<etiquettesLues << ")" << endl;
	#endif

	return etiquettesLues != etiquettesLuesBefore;
}
	
int Teleinfos::isTrameComplete(Print& debug) {
	// 0 si non, 1 si oui
	if (strstr(OPTARIF, "EJP") !=NULL) {
		#ifdef DEBUG 
			debug << "OPTARIF reconnue " << endl;
		#endif
		return (maskEJPComplet & etiquettesLues) == maskEJPComplet;
	} else {
		#ifdef DEBUG 
			debug << "OPTARIF inconnue [" <<OPTARIF <<"]"<< endl;
		#endif
		return 0;
	}
}
