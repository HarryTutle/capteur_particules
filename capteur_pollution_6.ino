
#include <LowPower.h> // librairie pour le mode veille.
#include <Wire.h> // librairie pour l'I2C.
#include <DS3231.h> // librairie pour l'horloge externe.
#include "DHT.h" // librairie capteur humidité et température.
#include <SDS011.h> // librairie sds particules.
#include <SPI.h> // liaison spi pour lecteur sd.
#include <SD.h> // librairie pour le lecteur sd enregistreur.



const byte wakeUpPin = 2; // borne de réveil arduino.
const byte timeCounter = 2; // durée d'acquisition des données.
const byte dede = 3; // borne digitale 3 pour le capteur dht humidité et température.
const byte rxPin = 0; // branchement série capteur particule.
const byte txPin = 1; //  branchement série capteur particule.
const byte cs=10; // branchement cs du lecteur sd.
const byte alim_dht = 5; // branchement alim dht.
const byte alim_sds = 4; // branchement alim sds.
const byte alim_diod = 6; // branchement alim diode.



SDS011 my_sds;

#define DHTTYPE DHT22 // type de dht employé.
DHT dht(dede, DHTTYPE); // initialisation dht.

// Bits dispos pour les deux alarmes.
// Found here: https://github.com/mlepard/ArduinoChicken/blob/master/roboCoop/alarmControl.ino

#define ALRM1_MATCH_EVERY_SEC  0b1111  // once a second
#define ALRM1_MATCH_SEC        0b1110  // when seconds match
#define ALRM1_MATCH_MIN_SEC    0b1100  // when minutes and seconds match
#define ALRM1_MATCH_HR_MIN_SEC 0b1000  // when hours, minutes, and seconds match

#define ALRM2_ONCE_PER_MIN     0b111   // once per minute (00 seconds of every minute)
#define ALRM2_MATCH_MIN        0b110   // when minutes match
#define ALRM2_MATCH_HR_MIN     0b100   // when hours and minutes match

RTClib RTC;
DS3231 Clock;

void setup() {

  pinMode(cs, OUTPUT); // pour envoi à la carte sd.
  pinMode(dede, INPUT); // ouverture reception dht.
  pinMode(alim_dht, OUTPUT); 
  pinMode(alim_sds, OUTPUT);
  pinMode(alim_diod, OUTPUT);
  pinMode(wakeUpPin, INPUT_PULLUP); // borne de reveil arduino.

  

  /*
  // Calibrage de l'horloge.
  Clock.setClockMode(false);// heures vont jusqu'à 24 au lieu de 12 am/12 pm.
  Clock.setYear(23);//définir l'année
  Clock.setMonth(9);//définir le mois
  Clock.setDate(27);//définir la date du mois
  Clock.setMinute(26);//définir les minutes
  Clock.setHour(12);//définir l'heure
  Clock.setSecond(00);//définir les secondes
  */
  
  Wire.begin(); // initialisation i2c pour horloge.
  dht.begin(); // initialisation du capteur température et humidité.
  my_sds.begin(rxPin, txPin); //RX, TX pour capteur sds.
  Serial.begin(9600);
  SPI.begin(); // initialisation liaison spi pour le lecteur sd.
  
  
  for (int i; i<5; i++) {

    if (SD.begin(cs)==false) {

      Serial.println("liaison sd en cours...");
      SD.begin(cs);
      delay(1000);
    }
    else if (SD.begin(cs)==true) {

      Serial.println("liaison sd ok");
      delay(1000);
      break;
    }

   
  }

  if (SD.begin(cs)==false) {

    Serial.println("erreur liaison sd");
    delay(1000);
  }
  
  
  // règlage des bits de l'alarme.
  byte ALRM1_SET = ALRM1_MATCH_MIN_SEC; // enclenche A1 quand les minutes et secondes sont les mêmes.
  byte ALRM2_SET = ALRM2_MATCH_MIN;     // enclenche A2 quand les minutes correspondent (pas de secondes sur l'alarme A2).

  int ALARM_BITS = ALRM2_SET;
  ALARM_BITS <<= 4;
  ALARM_BITS |= ALRM1_SET;
  
  // enclenche une alarme quand les minutes == 0 
  
  Clock.setA1Time(0, 0, 0, 0, ALARM_BITS, false, false, false); 
  
   
  Clock.turnOnAlarm(1);
  
  if (Clock.checkAlarmEnabled(1)) {
    Serial.println("alarme activée"); // verifie que l'alarme 1 est bien activée
    delay(1000);
  }
  
  
  if (Clock.checkIfAlarm(1)) {
    Serial.println("Ok");
    delay(1000);
  }
  
  Serial.println("mise en veille");
  
  delay(1000); // petite pause sinon ça plante.

  
  
  ShutDown(); // fonction de mise en veille de l'arduino.
  


}

void loop() {

  Serial.begin(9600);
 
  digitalWrite(alim_dht, HIGH); //ouverture alim dht.
  digitalWrite(alim_sds, HIGH); //ouverture alim sds.
  if (SD.exists("data.txt")==true) {
      digitalWrite(alim_diod, HIGH);
    }
    
   
  
  
  DateTime now = RTC.now(); // On récupère les données temporelles de l'horloge dans la boucle.
  int years = now.year();
  int months = now.month();
  int days = now.day();
  int hours = now.hour();
  int minutes = now.minute();
  int seconds = now.second();

  int h = dht.readHumidity();
  int t = dht.readTemperature();
  
  float pm10, pm25;
  int err;
  

  err = my_sds.read(&pm25, &pm10);
  

    if (minutes<timeCounter) {

    
    Serial.print(years);
    Serial.print("/");
    Serial.print(months);
    Serial.print("/");
    Serial.print(days);
    Serial.print("/");
    Serial.print(hours);
    Serial.print("/");
    Serial.print(minutes);
    Serial.print("/");
    Serial.print(seconds);
    Serial.print("/");
    Serial.print(t);
    Serial.print("/");
    Serial.print(h);
    Serial.print("/");
    Serial.print(pm10);
    Serial.print("/");
    Serial.print(pm25);
    Serial.print("/");
    Serial.println(SD.exists("data.txt"));

    

     delay(1000);
    }
    
  
  
  else if ((minutes>=timeCounter) && (minutes<(timeCounter+1))) {
  
    

   for (int i;i<5;i++) {

    if (SD.exists("data.txt")==false) {

      Serial.println("fichier pas détecté");
      delay(1000);
      
    }

    else if (SD.exists("data.txt")==true) {

      Serial.println("fichier détecté");
      delay(1000);
      break;
      
    }
   }

  
    File fichier=SD.open("data.txt", FILE_WRITE); // crée le fichier data pour enregistrer les données.
    fichier.print(years);
    fichier.print(";");
    fichier.print(months);
    fichier.print(";");
    fichier.print(days);
    fichier.print(";");
    fichier.print(hours);
    fichier.print(";");
    fichier.print(h);
    fichier.print(";");
    fichier.print(t);
    fichier.print(";");
    fichier.print(pm10);
    fichier.print(";");
    fichier.println(pm25);
    fichier.close();
   
    delay(1000);
  }
  
  else if (minutes==(timeCounter+1)) {
    
   
    Clock.turnOnAlarm(1); // on remet en route l'alarme avant la remise en veille de l'arduino.
    
    if (Clock.checkAlarmEnabled(1)) {

      Serial.println("alarme activée");
      delay(1000);
    }

    if (Clock.checkIfAlarm(1)) {

      Serial.println("ok");
      delay(1000);
    }

    Serial.println("mise en veille");
    
    delay(1000);

    
    
    ShutDown(); // on remet à nouveau en veille.
    
    

}
}

void WakeUp () {
   
}

void ShutDown () {

  digitalWrite(alim_dht, LOW); //fermeture alim dht.
  digitalWrite(alim_sds, LOW); //fermeture alim sds.
  digitalWrite(alim_diod, LOW); //fermeture alim ecran.
  Serial.end();
  delay(1000);
  attachInterrupt(digitalPinToInterrupt(wakeUpPin), WakeUp, FALLING);
  LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
  detachInterrupt(digitalPinToInterrupt(wakeUpPin));

}
