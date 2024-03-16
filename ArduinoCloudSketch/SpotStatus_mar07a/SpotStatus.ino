#include "arduino_secrets.h"
/* 
  Arduino IoT Cloud Thing "SpotStatus"
  https://create.arduino.cc/cloud/things/5060b90f-b8f0-46a8-940a-afd5922c7cf5 

  Arduino IoT Cloud Variables:
  bool spot1;
  bool spot2;
  bool spot3;
  bool spot4;
  bool spot5;
*/

#include "thingProperties.h"

const int NUM_SENSORS = 5; 
const int trigPins[NUM_SENSORS] = {3, 5, 7, 9, 13};
const int echoPins[NUM_SENSORS] = {4, 6, 8, 10, 14};

void setup() {
  Serial.begin(9600);
  delay(1500); 

  //connect to Arduino Cloud 
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
  
  //set up trig and echo pins for HC-SR04 sensors
  for(int i = 0; i < NUM_SENSORS; i++){
    pinMode(trigPins[i], OUTPUT); 
    pinMode(echoPins[i], INPUT); 
  }
  
}

void loop() {
  ArduinoCloud.update();
  long duration, inches, cm;
  
  for(int i = 0; i < NUM_SENSORS; i++){

    //trigger sensor and retrieve readings 
    digitalWrite(trigPins[i], LOW);
    delayMicroseconds(2);
    digitalWrite(trigPins[i], HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPins[i], LOW);

    duration = pulseIn(echoPins[i], HIGH);

    inches = microsecondsToInches(duration);
    cm = microsecondsToCentimeters(duration);

    //print readings
    Serial.print("Sensor ");
    Serial.print(i+1);
    Serial.print(" : ");
    Serial.print(inches);
    Serial.print("in, ");
    Serial.print(cm);
    Serial.print("cm");
    Serial.println();
    
    //update Arduino Thing  
    if(i == 0) spot1 = (cm > 10); 
    else if (i == 1) spot2 = (cm > 10); 
    else if (i == 2) spot3 = (cm > 10); 
    else if (i == 3) spot4 = (cm > 10);
    else if (i == 4) spot5 = (cm > 10); 
    
  }
  
  delay(100);
}

//time to distance conversion functions 
long microsecondsToInches(long microseconds) {
  return microseconds / 148;
}

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 58;
}

void onSpot1Change()  {}

void onSpot2Change()  {}

void onSpot3Change()  {}

void onSpot4Change()  {}

void onSpot5Change()  {}

