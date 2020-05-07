#!/usr/bin/env python
import rospy
import time

import sys
sys.path.append('/home/ubuntu/RedBoard')
import redboard

from std_msgs.msg import Int16MultiArray

#  Servo values, 0 is centre
pan_value = 0
tilt_value = 0

def callback(data):    
    rospy.loginfo(rospy.get_caller_id() + 'RCVD: %s', data.data)
    setservos(data.data[0], data.data[1])
    
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('head_driver', anonymous=True)
    rospy.Subscriber('head_controller', Int16MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def setservos(pan, tilt):
    global pan_value, tilt_value

    pan_max = 65

    # Positive is back, negative forward, due to servo orientation
    tilt_backward_max = 25
    tilt_forward_max = -55

    new_pan = pan_value + pan
    if(abs(new_pan) < pan_max):
        pan_value = new_pan

    new_tilt = tilt_value + tilt
    if(tilt_backward_max >= new_tilt >= tilt_forward_max):
        tilt_value = new_tilt

    redboard.servo22(pan_value)
    redboard.servo21(tilt_value)

if __name__ == '__main__':
    print("Head node listening...")
    #setservos(0, 0)
    #listener()
    redboard.servo8_off()
    rospy.spin()
