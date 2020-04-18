#define USE_TEENSY_HW_SERIAL

#include <ros.h>
#include <std_msgs/Int16MultiArray.h>
#include <math.h>

ros::NodeHandle  nh;

std_msgs::Int16MultiArray motor_array;
ros::Publisher motor_pub("motor_controller", &motor_array);

std_msgs::Int16MultiArray head_array;
ros::Publisher head_pub("head_controller", &head_array);

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
  
  nh.initNode();

  //  Instatiate motor array
  motor_array.layout.dim = (std_msgs::MultiArrayDimension *)
  malloc(sizeof(std_msgs::MultiArrayDimension)*2);
  motor_array.layout.dim[0].label = "motors";
  motor_array.layout.dim[0].size = 2;
  motor_array.layout.dim[0].stride = 1;
  motor_array.layout.data_offset = 0;
  motor_array.data_length = 2;

  //  Instantiate head array
  head_array.layout.dim = (std_msgs::MultiArrayDimension *)
  malloc(sizeof(std_msgs::MultiArrayDimension)*2);
  head_array.layout.dim[0].label = "head";
  head_array.layout.dim[0].size = 2;
  head_array.layout.dim[0].stride = 1;
  head_array.layout.data_offset = 0;
  head_array.data_length = 2;
  
  nh.advertise(motor_pub);
  nh.advertise(head_pub);
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
           
  int threeway = switch3 - switch4;

  if(switch1 == 1)
  {
    //  Calculate the motor values

    // convert to polar
    float r = hypot(lx, ly);
    float t = atan2(ly, lx);
    
    // rotate by 45 degrees
    t -= M_PI_4;
    
    // back to cartesian
    float left = r * sin(t);
    float right = r * cos(t);
    
    // rescale the new coords
    left = left * sqrt(2);
    right = right * sqrt(2);
    
    // clamp to -1/+1
    left = max(-100, min(left, 100));
    right = max(-100, min(right, 100));
    
    motor_array.data[0] = int(left);
    motor_array.data[1] = int(right);    

    motor_pub.publish( &motor_array );

    //  calculate the head movement values
    int pan = rx / 10;
    int tilt = ry / 10; 

    head_array.data[0] = pan;
    head_array.data[1] = tilt * -1;

    head_pub.publish( &head_array );
    
    nh.spinOnce();   
  }
        
  delay(30);        // delay in between reads for stability
}
