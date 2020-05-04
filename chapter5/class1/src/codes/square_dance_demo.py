#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import rospy  # 引用ROS的核心Python库
from geometry_msgs.msg import Twist
from math import pi


class OutAndBack():
    def __init__(self):
        # 初始化节点
        rospy.init_node('square_dance')
        # 设置回调函数，让机器人停下来
        rospy.on_shutdown(self.shutdown)

        # 定义用来发布twist命令给 /cmd_vel话题的ROS发布者
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        # 设置频率
        rospy.set_param('test_rate',50)
        rate = rospy.get_param('test_rate')  
        r = rospy.Rate(rate)

        # 设置线速度，角速度，目标距离，计算需要的时间
        linear_speed = 0.2
        goal_distance = 1.0
        linear_duration = goal_distance / linear_speed
        angular_speed = 1.0
        goal_angle = pi

        rospy.loginfo("The robot is ready to move……")
        # 获取起始时刻时间
        start_time = rospy.get_rostime()
        rospy.loginfo("Start time %i %i", start_time.secs, start_time.nsecs)

        # 前进一米，到达第一个节点
        move_cmd = Twist()
        move_cmd.linear.x = 0.2
        ticks = int(linear_duration *rate)

        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        # 旋转之前暂停一下
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)
        rospy.loginfo("The robot has arrived at the first point;")

        # 逆时针旋转135度
        move_cmd.angular.z = angular_speed
        ticks = int(3*goal_angle/4 *rate)
        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        # 暂停一下
        move_cmd = Twist()     
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)
        # 前进1.5米,到达第二个点
        move_cmd.linear.x = 0.2
        ticks = int(1.41*linear_duration *rate)
        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        # 旋转之前暂停一下
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)
        rospy.loginfo("The robot has arrived at the second point;")

        # 逆时针旋转225度
        move_cmd.angular.z = angular_speed
        ticks = int(5*goal_angle/4 *rate)
        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        # 暂停一下
        move_cmd = Twist()     
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)



        # 前进1米,到达第三个点
        move_cmd.linear.x = 0.2
        ticks = int(linear_duration *rate)
        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        # 暂停一下
        move_cmd = Twist()     
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)

        rospy.loginfo("The robot has arrived at the last point;")


        # 结束时间
        finish_time = rospy.get_rostime()
        # print(finish_time)
        rospy.loginfo("Finish time %i %i", finish_time.secs, finish_time.nsecs)

        # 停止机器人
        self.cmd_vel.publish(Twist())
        rospy.loginfo("The robot has finished the task.")

    # 我们的停机回调函数，如果脚本因任何原因停止运行，我们就会通过发布一条空的Twist消息让它停止运动
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


if  __name__ == '__main__':

    try:
        OutAndBack()

    except:
        rospy.loginfo("Out-and-Back node terminated.")

