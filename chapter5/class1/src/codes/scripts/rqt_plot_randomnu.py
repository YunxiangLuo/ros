#!/usr/bin/env python
'''demo ROS Node'''
# license removed for brevity
import rospy
from random import random
from std_msgs.msg import Float32

def talker():
    '''demo Publisher'''
    pub = rospy.Publisher('chatter', Float32, queue_size=10)
    rospy.init_node('demo')
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_int = random() * 50
        rospy.loginfo(hello_int)
        pub.publish(hello_int)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
