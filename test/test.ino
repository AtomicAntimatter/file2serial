// Simple test code for file2serial
unsigned long i = 0;
unsigned long sleep_time = 1000;
unsigned long last_time = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {

  if(millis() > last_time + sleep_time) {
    i++;
    Serial.println(i);
    last_time = millis();
  }

  if(Serial.available() > 0) {
    if(Serial.readStringUntil('\n').equals("Hey")) {
      Serial.println("Hola");
    }
  }
}
