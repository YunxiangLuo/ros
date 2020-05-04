cmake_minimum_required(VERSION 2.8.3)
project(sine_plot)#项目名称

add_compile_options(-std=c++11)#编译选项

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)#指定依赖

catkin_package(CATKIN_DEPENDS roscpp rospy std_msgs)#用于配置ROS和package配置文件和cmake文件

include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(sine_talker src/sine_talker.cpp)#生成可执行文件
target_link_libraries(sine_talker ${catkin_LIBRARIES})

