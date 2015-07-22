#include <RunningMedian.h>

RunningMedian samples_x = RunningMedian(5);
RunningMedian samples_y = RunningMedian(5);
//const int numReadings = 5;     //The number or readings being averaged

//int readingsX[numReadings];      // the readings from the analog input
//int index = 0;                  // the index of the current reading
//int totalX = 0;                  // the running total
//int averageX = 0;                // the average
//int readingsY[numReadings];      // the readings from the analog input
//int totalY = 0;                  // the running total
//int averageY = 0;                // the average
int command;
int median_x = 0;
int median_y = 0;
int sensorPin1 = A1;
int sensorPin2 = A2;// select the input pin for the potentiometer

void setup() {

  Serial.begin(9600);
  pinMode(6, OUTPUT); // pin for marking if data point was marked by psychopy
  pinMode(4, OUTPUT); // pin for marking trajectory
  pinMode(7, OUTPUT);

  digitalWrite(4, LOW);   // sets the pin to LOW
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  // initialize all the readings to 0:
  //for (int thisReadingX = 0; thisReadingX < numReadings; thisReadingX++)
  //  readingsX[thisReadingX] = 0;
  //for (int thisReadingY = 0; thisReadingY < numReadings; thisReadingY++)
    //readingsY[thisReadingY] = 0;
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();
    if (command != 'M'){
      digitalWrite(6, LOW); // to mark when an "M" is not received)
    }
    if (command == 'h') {
      //digitalWrite(13, HIGH);   // sets the pin to HIGH
      digitalWrite(7, HIGH);
    }
    if (command == 'A') {
      //digitalWrite(13, HIGH);   // sets the pin to HIGH
      digitalWrite(4, HIGH);
    }
    if (command == 'C') {
      //digitalWrite(13, HIGH);   // sets the pin to HIGH
      digitalWrite(4, LOW);
    }
    if (command == 'l') {
      digitalWrite(7, LOW);
    }
    if (command == 'M') {
      digitalWrite(6, HIGH);   // sets the pin to HIGH
      int x = analogRead(sensorPin2);
      int y = analogRead(sensorPin1);
      samples_x.add(x);
      samples_y.add(y);
      median_x = samples_x.getMedian();
      median_y = samples_y.getMedian();

      Serial.print(median_x);
      Serial.print(",");
      Serial.print(median_y);
      Serial.print('\n');
      delay(1);     // delay in between reads for stability
      digitalWrite(6, LOW);
    }
  }
}
