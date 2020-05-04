#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include <iostream>
#include <sys/time.h>
#include <math.h>

using namespace std;

unsigned long GetTime()
{
	struct timespec time1 = {0, 0};   
    clock_gettime(CLOCK_REALTIME, &time1); 
    long nows = time1.tv_nsec+ time1.tv_sec *1000000000;
    return nows;
}

int main(int argc, char **argv)
{
	ros::init(argc,argv,"sine_talker");//初始化ros,传递参数，定义节点名称
	ros::NodeHandle n;
	ros::Publisher chatter_pub = n.advertise<std_msgs::Float64> ("sine_signal",10);
	ros::Rate loop_rate(20.0);
	long time_init = 0;
	long time_now = 0;
	time_init = GetTime();

	while(ros::ok()){
		time_now = GetTime();
		std_msgs::Float64 msg;
		double sine = sin(  (double)( time_now - time_init )/1000000000 );
		if (0.8 > abs(sine))
			ROS_INFO("Normal output:%lf", abs(sine));
		else if (0.8 < abs(sine) && 0.9 > abs(sine))
			ROS_WARN("Danger output:%lf", abs(sine));
		else if (0.9 < abs(sine))
			ROS_ERROR("Wrong output:%lf", abs(sine));
		msg.data = sine;
		chatter_pub.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
	}
	return 0;
}

