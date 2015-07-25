

//Data Logger SD Card Libraries
#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include "RTClib.h"

// Variabels for the RTC to create a unique Filename

int HOUR = 0;
int DAY = 0;
int MIN = 0;

#define LOG_INTERVAL  1000 // millis between entries

unsigned long START_MICROS;
const int chipSelect = 10;

int psychopy_data_pin6 = 6;
int trajcectory_pin4 = 4;
int data_logging_signal7 = 7;
int directory_pin5 = 5;
int sensorPin1 = A1;
int sensorPin2 = A2;
int greenLED = 2;
int redLED = 3;
char directory[13];


RTC_DS1307 RTC;


// Globals for us to mess around with
int previous_read = LOW;
int this_read = HIGH;
int psychopy_signal = LOW;
int trajectory_signal = LOW;
int directory_signal = LOW;
File logfile;
int FILENUM=0;
int trajectory=0; // if trajectroy=0 then towards center, if =1 then towards outer target
int psychopy_data_point=0; //if psychopy_data_point=1 then these pointscorrespond to the data collected by psychopy




void setup() {
  //Serial.begin(9600);
  Wire.begin();
  RTC.begin();
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(psychopy_data_pin6, INPUT);
  pinMode(trajcectory_pin4, INPUT);
  pinMode(directory_pin5, INPUT);
  pinMode(data_logging_signal7, INPUT);
  pinMode(chipSelect, OUTPUT);
  pinMode(10, OUTPUT);
//  DateTime now = RTC.now();
//  HOUR = (now.hour());
//  DAY = (now.day());
//  MIN = (now.minute());
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)){ 
    //Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  //char directory[13];
//  sprintf(directory, "%02d_%02d_%02d",DAY, HOUR, MIN);
//  SD.mkdir(directory);
}

void newdirectory(){
  char new_directory[13];
  DateTime now = RTC.now();
  HOUR = (now.hour());
  DAY = (now.day());
  MIN = (now.minute());
  sprintf(new_directory, "%02d_%02d_%02d",DAY, HOUR, MIN);
  SD.mkdir(new_directory);
  FILENUM=0;
}

void newfile(){
  char filename[24];
  sprintf(filename, "%02d_%02d_%02d/%02d%02dT%03d.txt",DAY, HOUR, MIN, DAY, HOUR, FILENUM);
  FILENUM++;
  // only open a new file if it doesn't exist
  logfile = SD.open(filename, FILE_WRITE); //note that only one file can be open at a time
  START_MICROS = micros();
}

void loop(){
  char message[50];
  // delay for the amount of time we want between readings
  delayMicroseconds((LOG_INTERVAL -1) - (micros() % LOG_INTERVAL));
  
  // create a new file if the loop is
  trajectory_signal=digitalRead(trajcectory_pin4);
  directory_signal=digitalRead(directory_pin5);
  psychopy_signal=digitalRead(psychopy_data_pin6);
  this_read=digitalRead(data_logging_signal7);
  if (directory_signal == HIGH){
    newdirectory();
    digitalWrite(redLED, HIGH);
    delay(1000);
    digitalWrite(redLED, LOW);
    
  }
  if  (psychopy_signal == HIGH){
    psychopy_data_point=1;
  }
  if  (psychopy_signal == LOW){
    psychopy_data_point=0;
  }
  if  (trajectory_signal == HIGH){
    trajectory=1;
  }
  if (trajectory_signal == LOW){
    trajectory=0;
  }
  if ( (this_read == LOW) && ( previous_read == LOW)){
    digitalWrite(greenLED, HIGH);
    digitalWrite(redLED, LOW);
    //Serial.println(this_read);
  }
  if ( (this_read == HIGH) && (previous_read == LOW)){
    newfile();
    digitalWrite(greenLED, LOW);
    //Serial.println(previous_read);
    //Serial.println(this_read);
  }
  if ( (this_read == HIGH) && (previous_read == HIGH)){
    //if(logfile){
          digitalWrite(redLED, HIGH);
          int read1 = analogRead(sensorPin1);
          int read2 = analogRead(sensorPin2);
          unsigned long t = micros() - START_MICROS;
          //Serial.println("all is high");
          sprintf(message,"%lu,%d,%d,%d,%d",t, read1, read2, trajectory, psychopy_data_point);
          // if the file is available, write to it:
          logfile.println(message);
          //print to the serial port too:
         // Serial.println(message);
     // }
  }
  if ( (this_read == LOW) && (previous_read == HIGH)){
    //if (logfile)
        //logfile.flush();
        logfile.close();
        digitalWrite(redLED, LOW);
        digitalWrite(greenLED, LOW);
        //previous_read == LOW;
  
  }
  previous_read = this_read;
}
    
 









