#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import Float64

def sine_talker():
    pub = rospy.Publisher('sine_signal',Float64,queue_size=5)
    rospy.init_node('sine_talker')
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        time_now = rospy.get_time()
        sine_signal = math.sin(time_now)
        if 0.8 > abs(sine_signal):
            out_put = "Normal output: %s" % sine_signal
            rospy.loginfo(out_put)  
        elif 0.8 < abs(sine_signal) and 0.9 > abs(sine_signal):
            out_put = "Dangerous output: %s" %sine_signal
            rospy.logwarn(out_put)
        elif 0.9 < abs(sine_signal):
            out_put = "Wrong output: %s" %sine_signal
            rospy.logerr(out_put)
        pub.publish(sine_signal)
        rate.sleep()

if __name__ == '__main__':
    try:
        sine_talker()
    except rospy.ROSInterruptException:
        pass