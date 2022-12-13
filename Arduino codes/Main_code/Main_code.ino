#include <AFMotor.h>

AF_DCMotor motor1 (4);
String nom = "Arduino";
String msg;
void setup() {
   Serial.begin(9600);
   motor1.setSpeed(255);
}
void loop() {
  readSerialPort();
  if (msg != "") {
      sendData();
  }
  delay(500);
}
void readSerialPort() {
  msg = "";
  if (Serial.available()) {
      delay(10);
      while (Serial.available() > 0) {
          msg += (char)Serial.read();
      }
      Serial.flush();
  }
}
void sendData() {
  //write data
  Serial.print(nom);
  Serial.print(" received : ");
  Serial.print(msg);
  if (msg == "frente") {
    motor1.run(FORWARD);
    delay(5000);
    Serial.print("Indo para Frente");
  }
  if (msg == "tras") {
    motor1.run(BACKWARD);
    delay(5000);
    Serial.print("Indo para Tras");
  }
  if (msg == "parar") {
    motor1.run(RELEASE);
    delay(5000);
    Serial.print("Parar");
  }
}
