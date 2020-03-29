#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time
import serial

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
        text = str(ser.readline())
        command = text[2:][:-5])

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

        lx = int(commands[0])
        ly = int(commands[1])
        lz = int(commands[2])

        debug = str(lx) + ',' + str(ly) + ',' + str(lz) 

        rospy.loginfo(debug)
        motor_pub.publish(command)
        #rate.sleep()

if __name__ == '__main__':
    talker()
