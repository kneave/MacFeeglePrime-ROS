#!/usr/bin/env python
import rospy
import time

import sys
sys.path.append('/home/ubuntu/RedBoard')
import redboard

from std_msgs.msg import String

motor1 = 0
motor2 = 0
last_message = 0

def callback(data):
    global motor1, motor2, last_message

    rospy.loginfo(rospy.get_caller_id() + 'RCVD: %s', data.data)
    
    if data.data == 'w':
        setmotors(50,50)
    elif data.data == 'r':
        setmotors(50,-50)
    elif data.data == 'l':
        setmotors(-50, 50)
    elif data.data == 'b':
        setmotors(-50, -50)
    else:
        setmotors(0,0)
    
    last_message = time.time()

def setmotors(m1, m2):
    global motor1, motor2
    motor1 = m2
    motor2 = m1

def listener():
    global motor1, motor2, last_message

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('motor_driver', anonymous=True)
    rospy.Subscriber('motor', String, callback)

    while True:
        if(time.time() - last_message > 0.08):
            motor1 = 0
            motor2 = 0
        
        redboard.M1(motor1)
        redboard.M2(motor2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print("listening...")
    listener()
