#define hwserial Serial1

//  Trim values
int lx_trim = 0;
int ly_trim = 0;
int lz_trim = 0;

int rx_trim = 0;
int ry_trim = 0;
int rz_trim = 0;

int deadspot = 15;

// the setup routine runs once when you press reset:
void setup() {
  
  pinMode(2, INPUT_PULLDOWN);
  pinMode(3, INPUT_PULLDOWN);
  pinMode(4, INPUT_PULLDOWN);
  pinMode(5, INPUT_PULLDOWN);
  pinMode(6, INPUT_PULLDOWN);
  pinMode(7, INPUT_PULLDOWN);
  pinMode(8, INPUT_PULLDOWN);
  pinMode(9, INPUT_PULLDOWN);
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  
  hwserial.begin(115200);
}

//  Creates a deadspot around 0
int check_deadspot(int input)
{
  if(abs(input) > deadspot)
  {
    return input;
  }
  else
  {
    return 0;
  }
}

// the loop routine runs over and over again forever:
void loop() {
  int sensorValueLX = map(analogRead(A1), 1023, 0, -100, 100);
  int sensorValueLY = map(analogRead(A0), 1023, 0, -100, 100);
  int sensorValueLZ = map(analogRead(A2), 0, 1023, -100, 100);

  int sensorValueRX = map(analogRead(A4), 1023, 0, -100, 100);
  int sensorValueRY = map(analogRead(A3), 1023, 0, -100, 100);
  int sensorValueRZ = map(analogRead(A5), 0, 1023, -100, 100);

  int sensorValuePot = map(analogRead(A6), 0, 1023, 0, 100);
  
  int buttonPressL = digitalRead(2);
  int buttonPressR = digitalRead(3);

  int switch1 = digitalRead(4);
  int switch2 = digitalRead(5);

  //  3 and 4 are the three way switch
  int switch3 = digitalRead(6);
  int switch4 = digitalRead(7);
  
  int switch5 = digitalRead(8);
  int switch6 = digitalRead(9);

  // print out the value you read:
  int lx = check_deadspot(sensorValueLX + lx_trim);
  int ly = check_deadspot(sensorValueLY + ly_trim); 
  int lz = check_deadspot(sensorValueLZ + lz_trim);

  int rx = check_deadspot(sensorValueRX + rx_trim);
  int ry = check_deadspot(sensorValueRY + ry_trim); 
  int rz = check_deadspot(sensorValueRZ + rz_trim);

  
  String rightStick = String(rx) + "," + 
                      String(ry) + "," + 
                      String(rz) + "," + 
                      String(buttonPressR);

  String leftStick = String(lx) + "," + 
                     String(ly) + "," + 
                     String(lz) + "," + 
                     String(buttonPressL);
                     
  int threeway = switch3 - switch4;

  String buttons =  String(switch1) + "," +
                    String(switch2) + "," +
                    String(threeway) + "," +
                    String(switch5) + "," +
                    String(switch6) + "," +
                    String(sensorValuePot);
                    
  Serial.println(leftStick + "," + rightStick + "," + buttons);
  hwserial.println(leftStick + "," + rightStick + "," + buttons);
      
  delay(100);        // delay in between reads for stability
}
