#!/usr/bin/env python
import rospy
import time

import sys
sys.path.append('/home/ubuntu/RedBoard')
import redboard

from std_msgs.msg import String

#  Servo values, 0 is centre
pan_value = 0
tilt_value = 0

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'RCVD: %s', data.data)
    command = str(data.data)
    commands = command.split(',')

def setservos(pan, tilt):
    global pan_value, tilt_value

    pan_value += pan
    tilt_value += tilt

    redboard.servo21(pan_value)
    redboard.servo22(tilt_value)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('head_driver', anonymous=True)
    rospy.Subscriber('head', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print("Head driver listening...")
    setservos(0, 0)
    listener()
