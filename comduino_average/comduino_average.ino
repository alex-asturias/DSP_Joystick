
const int numReadings = 5;     //The number or readings being averaged

int readingsX[numReadings];      // the readings from the analog input
int index = 0;                  // the index of the current reading
int totalX = 0;                  // the running total
int averageX = 0;                // the average
int readingsY[numReadings];      // the readings from the analog input
int totalY = 0;                  // the running total
int averageY = 0;                // the average
int command;
int sensorPin1 = A1;
int sensorPin2 = A2;// select the input pin for the potentiometer

void setup() {

  Serial.begin(9600);
  pinMode(4, OUTPUT); // pin for marking if data point was marked by psychopy
  pinMode(5, OUTPUT); // pin for marking trajectory
  pinMode(6, OUTPUT); // pin for marking if data point was marked by psychopy
  pinMode(7, OUTPUT);

  digitalWrite(4, LOW);   // sets the pin to LOW
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  // initialize all the readings to 0:
  for (int thisReadingX = 0; thisReadingX < numReadings; thisReadingX++)
    readingsX[thisReadingX] = 0;
  for (int thisReadingY = 0; thisReadingY < numReadings; thisReadingY++)
    readingsY[thisReadingY] = 0;
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();
    if (command == 'D') {
      digitalWrite(5, HIGH);
      delay(500);
      digitalWrite(5, LOW);
    }
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
      // subtract the last reading:
      totalX = totalX - readingsX[index];
      totalY = totalY - readingsY[index];
      // read from the sensor:
      readingsX[index] = analogRead(sensorPin2);
      readingsY[index] = analogRead(sensorPin1);
      // add the reading to the total:
      totalX = totalX + readingsX[index];
      totalY = totalY + readingsY[index];
      // advance to the next position in the array:
      index = index + 1;


      // if we're at the end of the array...
      if (index >= numReadings) {
        // ...wrap around to the beginning:
        index = 0;
      }
      // calculate the average:
      averageX = totalX / numReadings;
      averageY = totalY / numReadings;
      // send it to the computer as ASCII digits
      Serial.print(averageX);
      Serial.print(",");
      Serial.print(averageY);
      Serial.print('\n');
      delay(1);     // delay in between reads for stability
      digitalWrite(6, LOW);
    }
  }
}
