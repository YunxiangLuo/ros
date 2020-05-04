#!/usr/bin/env python
import rospy
import rosbag

from std_msgs.msg import Int32, String

def writemsg():
    bag = rosbag.Bag('test.bag', 'w')
    try:  
        str = String()  
        str.data = 'foo'
        i = Int32()  
        i.data = 42  
        bag.write('chatter', str)  
        bag.write('numbers', i)  
    finally:  
        bag.close() 

def showmsg(topic_name):
	bag  = rosbag.Bag('test.bag')
	Iter = 0
	for topic, msg, t in bag.read_messages(topics=topic_name):
		sec         =(t.to_nsec()-1508618888979416609)*1e-9
		Iter += 1
		print msg
	print Iter


if __name__ == '__main__':
    writemsg()
    topic_name = 'chatter'
    showmsg(topic_name)
    topic_name = 'numbers'
    showmsg(topic_name)