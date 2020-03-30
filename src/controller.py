#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time
import serial
import math

# from https://electronics.stackexchange.com/questions/19669/algorithm-for-mixing-2-axis-analog-input-to-control-a-differential-motor-drive
def steering(x, y):
    # convert to polar
    r = math.hypot(x, y)
    t = math.atan2(y, x)

    # rotate by 45 degrees
    t -= math.pi / 4

    # back to cartesian
    left = r * math.sin(t)
    right = r * math.cos(t)

    # rescale the new coords
    left = left * math.sqrt(2)
    right = right * math.sqrt(2)

    # clamp to -1/+1
    left = max(-100, min(left, 100))
    right = max(-100, min(right, 100))

    return int(left), int(right)

def try_parse_int(s):
  try:
    return int(s)
  except ValueError:
    #print("Error parsing: " + s)
    return 0

def talker():
    ser = serial.Serial(
        port='/dev/serial0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    rospy.init_node('motor_controller', anonymous=True)
    motor_pub = rospy.Publisher('motor', String, queue_size=10)
    head_pub = rospy.Publisher('head', String, queue_size=10)
    
    rate = rospy.Rate(30) # 30hz

    while not rospy.is_shutdown():
        # Read a string from serial
        command = str(ser.readline())
        
        # Split the string and interpret
        commands = command.split(',')

        # Structure is as follows:
        # L = Left stick
        # R = Right stick
        # S = Switch
        # P = Potentiometer
        #
        # LX, LY, LZ, LB, RX, RY, RZ, RB, S1, S2, S3_three, S4, S5, P1
        # 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,       11, 12, 13
        # int,int,int,b,  int,int,int,b,  b,  b,  int,      b,  b,  b

        #try:
        # Parse left stick
        lx = try_parse_int(commands[0])
        ly = try_parse_int(commands[1])
        lz = try_parse_int(commands[2])
        lb = bool(commands[3])

        # Parse right stick
        rx = try_parse_int(commands[4])
        ry = try_parse_int(commands[5])
        rz = try_parse_int(commands[6])
        rb = try_parse_int(commands[7])

        # Switches
        s1 = try_parse_int(commands[8])
        s2 = try_parse_int(commands[9])
        s3_three = try_parse_int(commands[10])
        s4 = try_parse_int(commands[11])
        s5 = try_parse_int(commands[12])
        
        p1 = try_parse_int(commands[13])

        # s1 is drive/arms mode
        if s1 == True:
            left, right = steering(lx, ly) 
            motor = str(left) + ',' + str(right)
            rospy.loginfo("Motor: " + motor)
            motor_pub.publish(motor)

            # head = str(rx) + ',' + str(ry) + ',' + str(rz)
            # rospy.loginfo("Head: " + head)
            # head_pub.publish(head)
        
        rate.sleep()

if __name__ == '__main__':
    talker()
