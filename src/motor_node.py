#!/usr/bin/env python
import rospy
import time

import sys
sys.path.append('/home/ubuntu/RedBoard')
import redboard

from std_msgs.msg import Int16MultiArray

motor1 = 0
motor2 = 0
last_message = 0

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'RCVD: %s', data.data)
    
    setmotors(data.data[0], data.data[1])

    time.sleep(0.09)

    setmotors(0,0)

def setmotors(m1, m2):
    redboard.M1(m1)
    redboard.M2(m2)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('motor_driver', anonymous=True)
    rospy.Subscriber('motor_controller', Int16MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print("Motor node listening...")
    listener()
