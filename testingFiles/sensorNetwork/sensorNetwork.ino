//For testing sensor network

//pins info
const int NUM_SENSORS = 6; 
const int trigPins[NUM_SENSORS] = {1, 3, 5, 7, 9, 13};
const int echoPins[NUM_SENSORS] = {2, 4, 6, 8, 10, 14};

void setup() {
  Serial.begin(1000);

  for(int i = 0; i < NUM_SENSORS; i++){
    pinMode(trigPins[i], OUTPUT); 
    pinMode(echoPins[i], INPUT); 
  }

}

void loop() {
  long duration, inches, cm;
  
  for(int i = 0; i < NUM_SENSORS; i++){
    digitalWrite(trigPins[i], LOW);
    delayMicroseconds(2);
    digitalWrite(trigPins[i], HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPins[i], LOW);

    duration = pulseIn(echoPins[i], HIGH);

    inches = microsecondsToInches(duration);
    cm = microsecondsToCentimeters(duration);

    Serial.print("Sensor ");
    Serial.print(i+1);
    Serial.print(" : ");
    Serial.print(inches);
    Serial.print("in, ");
    Serial.print(cm);
    Serial.print("cm");
    Serial.println();
  }
  
  delay(100);
}

long microsecondsToInches(long microseconds) {
  return microseconds / 148;
}

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 58;
}
