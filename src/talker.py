#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import curses 

stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(True)

def talker(stdscr):
    pub = rospy.Publisher('motor', String, queue_size=10)
    rospy.init_node('motor_controller', anonymous=True)
    rate = rospy.Rate(30) # 30hz

    while not rospy.is_shutdown():
        c = stdscr.getch()

        if(c == ord('w')):
            hello_str = "w"
        elif (c == ord('d')):
            hello_str = "r"
        elif (c == ord('a')):
            hello_str = "l"
        elif (c == ord('s')):
            hello_str = "b"
        elif (c == 32):
            hello_str = "s"
        elif (c == -1):
            hello_str = "s"
        else:
            hello_str = ""
            
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        curses.wrapper(talker)
    except rospy.ROSInterruptException:
        pass
