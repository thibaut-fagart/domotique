#include "edf.h"
#include <Streaming.h> 

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


void getTeleinfo(SoftwareSerial& cptSerial, Print& debug) {
  //debug .print( ">>getTeleinfo") << endl;
  debug.print(">>getTeleinfo\n");
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

    debug .print( "Trame ["); debug.print (Trame); debug .print( "]\n");
  
    lireTrame(Trame,debug);	

    // on vérifie si on a une trame complète ou non
    for (i=0; i<11; i++) {
      trameComplete+=check[i];
    }
    debug .print( "Nb lignes valides :"); debug .print(trameComplete); debug .print("\n");
    if (trameComplete < 11) trameComplete=0; // on a pas les 11 valeurs, il faut lire la trame suivante
    else trameComplete = 1;
  }
    debug .print( "<<getTeleinfo\n") ;

}

/*------------------------------------------------------------------------------*/
/* Test checksum d'un message (Return 1 si checkum ok)				*/
/*------------------------------------------------------------------------------*/
int checksum_ok(char *etiquette, char *valeur, char checksum, Print& debug) 
{
    debug .print( ">>checksum_ok\n") ; 

	unsigned char sum = 32 ;		// Somme des codes ASCII du message + un espace
	int i ;
 
	for (i=0; i < strlen(etiquette); i++) sum = sum + etiquette[i] ;
	for (i=0; i < strlen(valeur); i++) sum = sum + valeur[i] ;
	sum = (sum & 63) + 32 ;
	debug .print (etiquette) ; debug.print( " ") ; debug.print(valeur); debug .print (" ") ; debug .print (checksum) ; debug .print("\n");
	debug .print( "Sum = "); debug .print (sum) ; debug .print( "\n");
	debug .print( "Cheksum = "); debug .print(int(checksum));debug .print( "\n");
	if ( sum == checksum) return 1 ;	// Return 1 si checkum ok.
	return 0 ;
    debug .print( "<<checksum_ok") ;debug .print("\n");
}

void lireTrame(char *trame, Print& debug){
    debug .print( ">>lireTrame") ; debug .print("\n");
    int i;
    int j=0;
    for (i=0; i < strlen(trame); i++){
      if (trame[i] != 0x0D) { // Tant qu'on est pas au CR, c'est qu'on est sur une ligne du groupe
          Ligne[j++]=trame[i];
      }
      else { //On vient de finir de lire une ligne, on la décode (récupération de l'etiquette + valeur + controle checksum
          decodeLigne(Ligne,debug);
          memset(Ligne,'\0',32); // on vide la ligne pour la lecture suivante
          j=0;
      }

   }
   debug .print( "<< lireTrame") ; debug .print("\n");

}

int decodeLigne(char *ligne, Print& debug){ 
  //Checksum='\0';
    debug .print( ">>decodeLigne") ; debug .print("\n");
  
   int debutValeur; 
  int debutChecksum;
  // Décomposer en fonction pour lire l'étiquette etc ...  
  debutValeur=lireEtiquette(ligne,debug);
  debutChecksum=lireValeur(ligne, debutValeur,debug);
  lireChecksum(ligne,debutValeur + debutChecksum -1,debug);

  if (checksum_ok(Etiquette, Donnee, Checksum[0], debug)){ // si la ligne est correcte (checksum ok) on affecte la valeur à l'étiquette
    return affecteEtiquette(Etiquette,Donnee,debug);
  } 
  else return 0;
    debug .print( "<<decodeLigne") ; debug .print("\n");

}


int lireEtiquette(char *ligne, Print& debug){
      debug .print( ">>lireEtiquette") ; debug .print("\n");

    int i;
    int j=0;
    memset(Etiquette,'\0',9);
    for (i=1; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Etiquette[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
	//  debug.print("Etiquette : ");
        //  debug.println(Etiquette);
          return j+2; // on est sur le dernier caractère de l'etiquette, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }

   }
      debug .print( "<<lireEtiquette") ;debug .print("\n");
}


int lireValeur(char *ligne, int offset, Print& debug){
	debug .print( ">>lireValeur") ;debug .print("\n");
    int i;
    int j=0;
    memset(Donnee,'\0',13);
    for (i=offset; i < strlen(ligne); i++){ 
      if (ligne[i] != 0x20) { // Tant qu'on est pas au SP, c'est qu'on est sur l'étiquette
          Donnee[j++]=ligne[i];
      }
      else { //On vient de finir de lire une etiquette
	//  debug.print("Valeur : ");
        //  debug.println(Donnee);
          return j+2; // on est sur le dernier caractère de la valeur, il faut passer l'espace aussi (donc +2) pour arriver à la valeur
      }

	}
	debug .print( "<<lireValeur") ; debug .print("\n");

}


void lireChecksum(char *ligne, int offset, Print& debug){
	debug .print( ">>lireChecksum") ; debug .print("\n");
	int i;
	int j=0;
	memset(Checksum,'\0',32);
	for (i=offset; i < strlen(ligne); i++){ 
		Checksum[j++]=ligne[i];
		//  debug.print("Chekcsum : ");
		// 	debug.println(Checksum);
	}

	debug .print( "<< lireChecksum") ; debug .print("\n");
}




int affecteEtiquette(char *etiquette, char *valeur, Print& debug){
      debug .print( ">>affecteEtiquette") ; debug .print("\n");
   debug.print("valeur="); debug.print(valeur) ;debug .print("\n");

 if(strcmp(etiquette,"ADCO") == 0) { 
   memset(ADCO,'\0',12); memcpy(ADCO, valeur,strlen(valeur)); check[1]=1; 
   debug.print("ADCO="); debug.print(ADCO); debug .print("\n");
 }
 else
 if(strcmp(etiquette,"HCHC") == 0) { HCHC = atol(valeur); check[2]=1;
   debug.print("HCHC="); debug.print(HCHC); debug .print("\n");
 }
 else
 if(strcmp(etiquette,"HCHP") == 0) { HCHP = atol(valeur); check[3]=1;
   debug.print("HCHP="); debug.print( HCHP ); debug .print("\n");
 }
 else
 if(strcmp(etiquette,"HHPHC") == 0) { 
   memset(HHPHC,'\0',2); strcpy(HHPHC, valeur); check[4]=1;
   debug.print("HHPHC="); debug.print(HHPHC) ; debug .print("\n");
 }
 else
 if(strcmp(etiquette,"PTEC") == 0) { memset(PTEC,'\0',4); memcpy(PTEC, valeur,strlen(valeur)); check[5]=1;
   debug.print("PTEC="); debug.print(PTEC); debug .print("\n");
 }
 else
 if(strcmp(Etiquette,"IINST") == 0) { IINST = atoi(valeur); check[6]=1;
   debug.print( "IINST="); debug.print(IINST); debug .print("\n");
 }
 else
 if(strcmp(Etiquette,"PAPP") == 0) { PAPP = atol(valeur); check[7]=1;
   debug.print("PAPP="); debug.print(PAPP); debug .print("\n");
 }
 else
 if(strcmp(Etiquette,"IMAX") == 0) { IMAX = atol(valeur); check[8]=1;
   debug.print("IMAX="); debug.print(IMAX); debug .print("\n");
 }
 else
 if(strcmp(Etiquette,"OPTARIF") == 0) { memset(OPTARIF,'\0',4); memcpy(OPTARIF, valeur,strlen(valeur)); check[9]=1;
   debug.print("OPTARIF="); debug.print(OPTARIF); debug .print("\n");
 }
 else
 if(strcmp(Etiquette,"ISOUSC") == 0) { ISOUSC = atoi(valeur); check[10]=1;
   debug.print( "ISOUSC="); debug.print(ISOUSC); debug .print("\n");
 }
 else
 if(strcmp(Etiquette,"MOTDETAT") == 0) { memset(MOTDETAT,'\0',10); memcpy(MOTDETAT, valeur, strlen(valeur)); check[0]=1;
   debug.print("MOTDETAT="); debug.print(MOTDETAT); debug .print("\n");
 }
 else {
   debug .print( "unknown etiquette"); debug .print("\n");
 return 0;
 }

 return 1;
}
