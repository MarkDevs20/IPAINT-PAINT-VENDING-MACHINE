#include <AccelStepper.h>

// STEPPER MOTOR PINS
const int dirPinP = 2;
const int stepPinP = 3;
const int dirPinB = 4;
const int stepPinB = 5;
const int dirPinY = 6;
const int stepPinY = 7;
const int dirPinG = 8;
const int stepPinG = 9;
const int dirPinR = 10;
const int stepPinR = 11;
const int motorSpeed = 900;  
const int motorAccel = 500;
const int dirPinCompress = 12;  
const int stepPinCompress = 13;

const int relayPin = A4;    
const int sRelayPin = A3;  

AccelStepper stepperP(AccelStepper::DRIVER, stepPinP, dirPinP); // PERMACOAT
AccelStepper stepperB(AccelStepper::DRIVER, stepPinB, dirPinB); // THALO BLUE
AccelStepper stepperY(AccelStepper::DRIVER, stepPinY, dirPinY); // EXTERIOR YELLOW
AccelStepper stepperG(AccelStepper::DRIVER, stepPinG, dirPinG); // THALO GREEN
AccelStepper stepperR(AccelStepper::DRIVER, stepPinR, dirPinR); // EXTERIOR RED
AccelStepper stepperCompress(AccelStepper::DRIVER, stepPinCompress, dirPinCompress); // COMPRESS

// Updated function declaration to handle two colorant motors
void dispenseStepper(AccelStepper &stepper, int steps, AccelStepper *colorant1 = NULL, int stepsC1 = 0, AccelStepper *colorant2 = NULL, int stepsC2 = 0);
void compressAndShake();

char c = ' ';

void setup() {
  Serial.begin(115200);

  stepperP.setMaxSpeed(motorSpeed);
  stepperP.setAcceleration(motorAccel);
  stepperB.setMaxSpeed(motorSpeed);
  stepperB.setAcceleration(motorAccel);
  stepperY.setMaxSpeed(motorSpeed);
  stepperY.setAcceleration(motorAccel);
  stepperG.setMaxSpeed(motorSpeed);
  stepperG.setAcceleration(motorAccel);
  stepperR.setMaxSpeed(motorSpeed);
  stepperR.setAcceleration(motorAccel);
  stepperCompress.setMaxSpeed(200);
  stepperCompress.setAcceleration(300);

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);

  pinMode(sRelayPin, OUTPUT);
  digitalWrite(sRelayPin, HIGH); 
}

void loop() {
  if (Serial.available() > 0) {
    c = Serial.read();
    if (c == 'P') {
      dispenseStepper(stepperP, 5800); 
    } 
    else if (c == '1') { 
      dispenseStepper(stepperP, 5800, &stepperB, 2400);
    } 
    else if (c == '2') {
      dispenseStepper(stepperP, 5800, &stepperY, 2400);
    } 
    else if (c == '3') {
      dispenseStepper(stepperP, 5800, &stepperG, 2400);
    } 
    else if (c == '4') {
      dispenseStepper(stepperP, 5800, &stepperR, 2400);
    } 
    else if (c == '5'){
      dispenseStepper(stepperP, 5800, &stepperB, 1200, &stepperY, 1200);
    }
    else if (c == '6'){
      dispenseStepper(stepperP, 5800, &stepperG, 1200, &stepperR, 1200);
    }
    else if (c == '7'){
      dispenseStepper(stepperP, 5800, &stepperY, 1200, &stepperG, 1200);
    }
    else if (c == '8'){
      dispenseStepper(stepperP, 5800, &stepperB, 1200, &stepperR, 1200);
    }
    else if (c == '9'){
      dispenseStepper(stepperP, 5800, &stepperY, 1200, &stepperR, 1200);
    }
    else if (c == '10'){  
      dispenseStepper(stepperP, 5800, &stepperB, 1200, &stepperG, 1200);
    }
    else if (c == 'C') {  
      compressAndShake();  
    }
  }
}
void dispenseStepper(AccelStepper &stepper, int steps, AccelStepper *colorant1, int stepsC1, AccelStepper *colorant2, int stepsC2) {
  stepper.setCurrentPosition(0);
  stepper.moveTo(steps);

  if (colorant1 != NULL) {
    colorant1->setCurrentPosition(0);
    colorant1->moveTo(stepsC1);
  }
  if (colorant2 != NULL) {
    colorant2->setCurrentPosition(0);
    colorant2->moveTo(stepsC2);
  }

  unsigned long lastUpdate = 0;

  while (stepper.currentPosition() != steps || 
         (colorant1 != NULL && colorant1->currentPosition() != stepsC1) ||
         (colorant2 != NULL && colorant2->currentPosition() != stepsC2)) {
    
    stepper.run();
    if (colorant1 != NULL) {
      colorant1->run();
    }
    if (colorant2 != NULL) {
      colorant2->run();
    }
    
    int progress = map(stepper.currentPosition(), 0, steps, 0, 50);
    if (millis() - lastUpdate > 100) {
      Serial.println(progress);
      lastUpdate = millis();
    }
  }
  
  delay(500);
  digitalWrite(sRelayPin, LOW);
  stepper.moveTo(0);
  if (colorant1 != NULL) {
    colorant1->moveTo(0);
  }
  if (colorant2 != NULL) {
    colorant2->moveTo(0);
  }
  while (stepper.currentPosition() != 0 || 
         (colorant1 != NULL && colorant1->currentPosition() != 0) ||
         (colorant2 != NULL && colorant2->currentPosition() != 0)) {
    
    stepper.run();
    if (colorant1 != NULL) {
      colorant1->run();
    }
    if (colorant2 != NULL) {
      colorant2->run();
    }
    int progress = map(stepper.currentPosition(), steps, 0, 50, 100);
    if (millis() - lastUpdate > 100) {
      Serial.println(progress);
      lastUpdate = millis();
    }
  }
  
  digitalWrite(sRelayPin, HIGH);
  Serial.println("DONE");
}

void compressAndShake() {
  Serial.println("COMPRESSING STARTED");
  stepperCompress.setCurrentPosition(0);
  stepperCompress.moveTo(1800);  // bucket size
  while (stepperCompress.currentPosition() != 1800) { 
    stepperCompress.run();
  }
  Serial.println("SHAKING STARTED");
  digitalWrite(relayPin, LOW);
  unsigned long startTime = millis();
  while (millis() - startTime < 60000) { // Relay time
    int progress = map(millis() - startTime, 0, 60000, 0, 100);
    Serial.print("SHAKING PROGRESS: ");
    Serial.println(progress);
    delay(1000);
  }
  digitalWrite(relayPin, HIGH);
  Serial.println("SHAKING DONE");
  stepperCompress.moveTo(0);
  while (stepperCompress.currentPosition() != 0) {
    stepperCompress.run();
  }
  Serial.println("MIXING DONE");
}