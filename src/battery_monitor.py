#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import time
import smbus

import sys
sys.path.append('/home/ubuntu/RedBoard')
import redboard

def readAdc_0():
    bus.write_i2c_block_data(address, 0x01, [0xc3, 0x83])
    time.sleep(0.01)
    adc = bus.read_i2c_block_data(address,0x00,2)
    return adc


def talker():
    rospy.init_node('robot_voltage_node', anonymous=True)
    voltage_pub = rospy.Publisher('robot_voltage', Float32, queue_size=10)
    
    rate = rospy.Rate(1) # 1Hz

    while not rospy.is_shutdown():

        voltage0 = readAdc_0()

        # Battery Voltage

        conversion_0 = (voltage0[1])+(voltage0[0]<<8)
        volts_0 = conversion_0 / ADC_bat_conversion_Value

        rounded_voltage = round(volts_0,2)
                    
        rospy.loginfo(rounded_voltage)
        voltage_pub.publish(rounded_voltage)
        rate.sleep()

if __name__ == '__main__':
    ADC_bat_conversion_Value = 1109.0

    bus = smbus.SMBus(1)
    address = 0x48
    
    talker()