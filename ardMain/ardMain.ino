const int analogInPina = A0;
const int analogInPinb = A1;
const int analogInPinc = A2;

int sensorValuea = 0;
int sensorValueb = 0;
int sensorValuec = 0;

void setup() {

  Serial.begin(9600); 
}

void loop() {
  if(Serial.available() && Serial.read() <= 1000){
  // read the analog in value:
  sensorValuea = analogRead(analogInPina);
  sensorValueb = analogRead(analogInPinb);
  sensorValuec = analogRead(analogInPinc);
  // print the values to serial, with A0 starting from 1, A1 2, A2 3
  Serial.println(sensorValuea+1000);
  Serial.println(sensorValueb+2000);
  Serial.println(sensorValuec+3000);}
}
