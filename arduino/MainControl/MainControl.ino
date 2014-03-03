#include "DHT22.h"
#include <SPI.h>
#include <TimerOne.h>

int dhtSalonPin   = 23;  // DHT22 Salon
int dhtPCPin      = 25;  // DHT22 Palcard PC
int dhtSdBPin     = 51;  // DHT22 Salle de Bain
int dhtExtPin     = 53;  // DHT22 Exterieur

int VMCPin        = 47;  // Switch porte
int FiveVPin      = 49;  // 5V cmd

int portePin      = 29;  // VMC Power

int couloirOutPin = 33;  // Ventilo couloir Out
int couloirInPin  = 35; // Ventilo couloir In
int SdBOutPin     = 37;  // Ventilo Salle de bain Out
int SdBInPin      = 39; // Ventilo Salle de bain In


int couloirPWMPin = 11;  // Ventilo couloir PWM
int SdBPWMPin     = 12;  // Ventilo Salle de bain PWM

int thermostatPin   = 41; // Relay Thermostat
int TwelveVPinSpOne = 43;  // 12V cmd
int TwelveVPinSpTwo = 45;  // 12V cmd

int AudioCuisinePin = 27; // Power Ampli Cuisine
int AudioSdBPin     = 29; // Power Ampli Salle de bain
int AudioChambrePin = 31; // Power Ampli Chambre
int AudioSalonPin   = 32; // Power Ampli Salon

int couloirSpeedPin =  9;  // Ventilo couloir Speed return
int SdBSpeedPin     = 10;  // Ventilo Salle de bain Speed return

int couloirSpeed  = 800;  // valeur PWM ventilo couloir
int SdBSpeed      = 800;  // valeur PWM ventilo Salle de Bain

char inData[30]; // Allocate some space for the string
char inChar=-1; // Where to store the character read
byte index = 0; // Index into array; where to store the character

float tempSdB = 0, humSdB = 0;
DHT22_Err_t resultSdB;
float tempPC = 0, humPC = 0;
DHT22_Err_t resultPC;
float tempSalon = 0, humSalon = 0;
DHT22_Err_t resultSalon;
float tempExt = 0, humExt = 0;
DHT22_Err_t resultExt;

// Définition du timeout compteur de vitesse ventilateur
#define PULSE_TIMEOUT 200000
 
// Variable contenant la vitesse du moteur
unsigned long rpmCouloir; 
unsigned long rpmSdB; 


void setup() {
  pinMode(dhtSdBPin,   INPUT);
  pinMode(portePin,    INPUT);
  pinMode(dhtPCPin,    INPUT);
  pinMode(dhtSalonPin, INPUT);
  pinMode(dhtExtPin,   INPUT);
  pinMode(VMCPin,        OUTPUT);  
  pinMode(couloirInPin,  OUTPUT);  
  pinMode(couloirOutPin, OUTPUT);  
  pinMode(SdBInPin,      OUTPUT);  
  pinMode(SdBOutPin,     OUTPUT);  
  pinMode(AudioCuisinePin, OUTPUT);
  pinMode(AudioSdBPin,     OUTPUT);
  pinMode(AudioChambrePin, OUTPUT);
  pinMode(thermostatPin,   OUTPUT);
  
  digitalWrite(VMCPin,HIGH);
  
  Timer1.initialize(40000);
  Timer1.pwm(couloirPWMPin, couloirSpeed);
  Timer1.pwm(SdBPWMPin, SdBSpeed);
  
  
  Serial.begin(9600);   
}

char serialString(char* This) {
    while (Serial.available() > 0) // Don't read unless
                                   // there you know there is data
    {
        if(index < 29) // One less than the size of the array
        {
            inChar = Serial.read(); // Read a character
            inData[index] = inChar; // Store it
            index++; // Increment where to write next
            inData[index] = '\0'; // Null terminate the string
        }
    }

    if (strcmp(inData,This)  == 0) {
        for (int i=0;i<29;i++) {
            inData[i]=0;
        }
        index=0;
        return(0);
    }
    else {
        return(1);
    }
}

void loop() {
  
  if (Serial.available() > 0) {
    
    if (serialString("Ventilo-Couloir-Speed")==0) {
     rpmCouloir = pulseIn(couloirSpeedPin, LOW, PULSE_TIMEOUT); 
     Serial.print("Ventilo Couloir Speed:");
     Serial.print(rpmCouloir, DEC);
    } 

    if (serialString("Ventilo-SdB-Speed")==0) {
      rpmSdB = pulseIn(SdBSpeedPin, LOW, PULSE_TIMEOUT); 
      Serial.print("Ventilo SdB Speed:");
      Serial.print(rpmSdB, DEC);
    } 

    if (serialString("Ventilo-Couloir++")==0) {
      if (couloirSpeed < 1000) {
        couloirSpeed = couloirSpeed + 10;
      }
      Timer1.setPwmDuty(couloirPWMPin, couloirSpeed);
      Serial.print("Ventilo Couloir Req:");
      Serial.print(couloirSpeed);
    } 
    if (serialString("Ventilo-Couloir--")==0) {
      if (couloirSpeed > 500) {
        couloirSpeed = couloirSpeed - 10;
      }
      Timer1.setPwmDuty(couloirPWMPin, couloirSpeed);
      Serial.print("Ventilo Couloir Req:");
      Serial.print(couloirSpeed);
    }

    if (serialString("Ventilo-SdB++")==0) {
      if (SdBSpeed < 1000) {
        SdBSpeed = SdBSpeed + 10;
      }
      Timer1.setPwmDuty(SdBPWMPin,SdBSpeed);
      Serial.print("Ventilo SdB Req:");
      Serial.print(SdBSpeed);
    } 
    if (serialString("Ventilo-SdB--")==0) {
      if (couloirSpeed > 500) {
        SdBSpeed = SdBSpeed - 10;
      }
      Timer1.setPwmDuty(SdBPWMPin,SdBSpeed);
      Serial.print("Ventilo SdB Req:");
      Serial.print(SdBSpeed);
    }
    
    if (serialString("Ventilo-Couloir1-ON")==0) {
      digitalWrite(couloirOutPin,HIGH);
    } 
    if (serialString("Ventilo-Couloir1-OFF")==0) {
      digitalWrite(couloirOutPin,LOW);
    }

    if (serialString("Ventilo-Couloir2-ON")==0) {
      digitalWrite(couloirInPin,HIGH);
    } 
    if (serialString("Ventilo-Couloir2-OFF")==0) {
      digitalWrite(couloirInPin,LOW);
    }
        
    if (serialString("Ventilo-SdB1-ON")==0) {
      digitalWrite(SdBOutPin,HIGH);
    } 
    if (serialString("Ventilo-SdB1-OFF")==0) {
      digitalWrite(SdBOutPin,LOW);
    }

    if (serialString("Ventilo-SdB2-ON")==0) {
      digitalWrite(SdBInPin,HIGH);
    } 
    if (serialString("Ventilo-SdB2-OFF")==0) {
      digitalWrite(SdBInPin,LOW);
    }
    
    if (serialString("Porte")==0) {
      if (digitalRead(portePin)==0) {
        Serial.print("OPEN");
      }
      else {
        Serial.print("CLOSED");
      }
    }
    
    if (serialString("Thermostat-ON")==0) {
      digitalWrite(thermostatPin,HIGH);
    } 
    if (serialString("Thermostat-OFF")==0) {
      digitalWrite(thermostatPin,LOW);
    }
        
    if (serialString("Audio-Salon-ON")==0) {
      digitalWrite(AudioSalonPin,HIGH);
    } 
    if (serialString("Audio-Salon-OFF")==0) {
      digitalWrite(AudioSalonPin,LOW);
    }
            
    if (serialString("Audio-Cuisine-ON")==0) {
      digitalWrite(AudioCuisinePin,HIGH);
    } 
    if (serialString("Audio-Cuisine-OFF")==0) {
      digitalWrite(AudioCuisinePin,LOW);
    }
    
    if (serialString("Audio-Chambre-ON")==0) {
      digitalWrite(AudioChambrePin,HIGH);
    } 
    if (serialString("Audio-Chambre-OFF")==0) {
      digitalWrite(AudioChambrePin,LOW);
    }
    
    if (serialString("Audio-SdB-ON")==0) {
      digitalWrite(AudioSdBPin,HIGH);
    } 
    if (serialString("Audio-SdB-OFF")==0) {
      digitalWrite(AudioSdBPin,LOW);
    }
    
    if (serialString("VMC-ON")==0) {
      digitalWrite(VMCPin,HIGH);
    } 
    if (serialString("VMC-OFF")==0) {
      digitalWrite(VMCPin,LOW);
    }
    
    if (serialString("SdB")==0) {
      resultSdB   = getDHT22(dhtSdBPin,   &tempSdB,   &humSdB); 
      if (resultSdB != DHT22_ERR_NONE) {
        Serial.print("Error:"); 
        Serial.print(resultSdB); 
      } 
      else {
        Serial.print(humSdB);
        Serial.print(":");
        Serial.print(tempSdB);
      }
    }
        
    if (serialString("PC")==0) {
      resultPC    = getDHT22(dhtPCPin,    &tempPC,    &humPC); 
      if (resultPC != DHT22_ERR_NONE) {
        Serial.print("Error:"); 
        Serial.print(resultPC); 
      } 
      else {
        Serial.print(humPC);
        Serial.print(":"); 
        Serial.print(tempPC);
      }
    }
        
    if (serialString("Salon")==0) {
      resultSalon = getDHT22(dhtSalonPin, &tempSalon, &humSalon); 
      if (resultSalon != DHT22_ERR_NONE) {
      Serial.print("Error:"); 
      Serial.print(resultSalon); 
      } 
      else {
        Serial.print(humSalon);
        Serial.print(":");
        Serial.print(tempSalon);
      }
    }
        
    if (serialString("Ext")==0) {
      resultExt   = getDHT22(dhtExtPin,   &tempExt,   &humExt); 
      if (resultExt != DHT22_ERR_NONE) {
        Serial.print("Error:"); 
        Serial.print(resultExt); 
        } 
        else {
          Serial.print(humExt);
          Serial.print(":"); 
          Serial.print(tempExt);
        }
    }
  }   
}
