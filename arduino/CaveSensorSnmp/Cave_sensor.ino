#include "DHT22.h"
#include <SPI.h>
#include <Ethernet.h>


/* Détails technique de la connexion ethernet */
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x56, 0xB3 };  
byte ip[] = { 192, 168, 0, 60 };
byte gateway[] = { 192, 168, 0, 254 };
byte subnet[] = { 255, 255, 255, 0 }; 
EthernetServer serveurHTTP(999); 

int dhtPin=5; 
int pirPin=3; 

int pir_delay=12; 
int decompte=0;
int pir_moving;
int pir_nobody;
long previousMillis_pir = 0; 
long interval_pir = 250;    
  
void setup() {
  pinMode(dhtPin, INPUT);
  pinMode(pirPin, INPUT);
  
    // Configuration de la ethernet shield et du server
  Ethernet.begin(mac, ip, gateway, subnet);
  delay(1000); // donne le temps à la carte Ethernet de s'initialiser
  serveurHTTP.begin(); 
}

void getSensorValue(EthernetClient client, char* sensor, int dht22Pin) {

  DHT22_Err_t result;
  float temperature = 0, humidity = 0;
  unsigned long now = millis();
 
  result = getDHT22(dht22Pin, &temperature, &humidity);  

  client.print(sensor);
  if (result != DHT22_ERR_NONE)
  {
    client.print(":Error:");
    client.print(result,1);
  }
  else
  {    
    client.print(":temperature:");
    client.print(temperature,1);
    client.print(":humidity:");
    client.print(humidity,1);
  }
  client.print(":Time:");
  client.print(now,1);
  client.print(":End:");
}

void loop() {
  
  unsigned long currentMillis = millis();
  EthernetClient client = serveurHTTP.available();
 
  if(currentMillis - previousMillis_pir > interval_pir)
  {
    previousMillis_pir = currentMillis;   

    int pirVal = digitalRead(pirPin);
    
    if(pirVal == LOW)
    {
      if (decompte!=pir_delay)
      {
        pir_moving = true;
        decompte=pir_delay;
      }  
      else
      {
        pir_moving = false;
      }  
    } 
    else
    {
    // plus personne, on commence à décompter
      if(decompte > 0 )
      {
        decompte--;
        pir_nobody = false;
      }
      else if (decompte == 0)
      {
        pir_nobody = true;
        decompte=-1;
      }
    }
  }  
  
  if (client) { 
 
    if (client.connected()) {
      
      getSensorValue(client,"DHT",dhtPin); 
      client.print("PIR:Moving:");
      client.print(pir_moving,1);
      client.print(":Nobody:");
      client.print(pir_nobody,1);
      client.print(":Time:");
      client.print(currentMillis,1);
      client.print(":End:");
    
    } // --- fin if client connected
  
    delay(1);  // on donne au navigateur le temps de recevoir les données

    client.stop(); // ferme le client distant une fois réponse envoyée
    delay(10);     // laisse temps fermeture
  }
}
