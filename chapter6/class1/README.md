
# 6.1 ROSPY（上）

从本讲开始，我们介绍ROSPY。

**本讲重点**

- 相关函数
- ROSPY Topic
- ROSPY Service

**教学目的**

- 了解ROSPY相关函数（Node、Topic、Service、Param、Time）
- 熟练使用ROSPY Topic进行编程
- 熟练使用ROSPY Service进行编程

本讲分成两部分内容，首先是介绍ROSPY相关函数，之后演示ROSPY的例子。

## 1. ROSPY相关函数

ROSPY的官方文档中可以看到ROSPY里有很多submodule子模块、很多的类以及函数，你可能感觉ROSPY文档层次不分明，实现的代码有点乱，没关系，这里把常用的函数列在下表。在ROS程序里，首先`import rospy`，然后就可以使用`rospy.init_node`来初始化node了。

**ROSPY-node相关函数**

| 函数                     | 描述                 |
| ------------------------ | -------------------- |
| init_node(name)          | 注册和初始化node     |
| MasterProxy get_master() | 获取master的句柄     |
| bool is_shutdown()       | 返回是否关闭         |
| on_shutdown(fn)          | 在node关闭时调用函数 |
| str get_node_uri()       | 返回节点的URI        |
| str get_name()           | 返回本节点的全名     |
| str get_namespace()      | 返回本节点的名字空间 |

参考链接http://docs.ros.org/api/rospy/html/

**ROSPY-topic相关函数**

ROSPY中topic通信相关的函数和类，主要是Publisher和Subscriber, 我们用`rospy.Publisher(‘topicname’,std_msgs.msg.String, queue_size=10)`来发布一个topic。ROSPY中topic的主要函数可参考下表。

| 函数                                                         | 描述                                     |
| ------------------------------------------------------------ | ---------------------------------------- |
| [[str,str]]  get_published_topics()                          | 返回正在被发布的所有topic名称和类型      |
| Message wait_for_message(topic, topic_type, time_out=None)   | 等待指定topic的一个message               |
| spin()                                                       | 触发topic或service的处理，会阻塞直到关闭 |
| **Publisher类**                                              |                                          |
| \__init__(self, name, data_class, queue_size=None)           | 构造函数                                 |
| publish(self,msg)                                            | 成员函数发布消息                         |
| unregister(self)                                             | 成员函数停止发布                         |
| **Subscriber类**                                             |                                          |
| \__init__(self, name, data_class, call_back=None, queue_size=None) | 构造函数                                 |
| unregister(self)                                             | 成员函数停止订阅                         |

**ROSPY-Service相关函数**

| 函数                                          | 描述                  |
| --------------------------------------------- | --------------------- |
| wait_for_service(service, timeout=None)       | 阻塞直到服务可用      |
| **Service类**                                 |                       |
| \__init__(self, name, service_class, handler) | 构造函数提供服务      |
| shutdown(self)                                | 成员函数关闭服务      |
| **ServiceProxy类**                            |                       |
| __init__(self,name, service_class)            | 构造函数 服务的请求方 |
| call(self,*args, **kwds)                      | 调用服务              |
| \__call__(self,*args, **kwds)                 | 调用服务              |


这里call与__call__的作用一样，但是用法不同。

**ROSPY-Param相关函数**

| 函数                                                         | 描述                       |
| ------------------------------------------------------------ | -------------------------- |
| XmlRpcLegalValue  get_param(param_name, default=_unspecified) | 获取参数的值               |
| [str] get_param_names()                                      | 获取参数的名称             |
| set_param(param_name, param_value)                           | 设置参数的值               |
| delete_param(param_name)                                     | 删除参数                   |
| bool has_param(param_name)                                   | 参数是否存在于参数服务器上 |
| str search_param()                                           | 搜索参数                   |

**ROSPY-Time相关函数**

| 函数                             | 描述                            |
| -------------------------------- | ------------------------------- |
| **Time类**                       |                                 |
| \__init__(self, secs=0, nsecs=0) | 构造函数                        |
| Time  now()                      | 静态方法 返回当前时刻的Time对象 |
| **函数**                       |                                 |
| Time get_rostime()               | 当前时刻的Time对象              |
| float  get_time()                | 返回当前时间，返回float 单位秒  |
| sleep(duration)                  | 执行挂起                        |
| **Rate 类**                     |                                |
| \__init__(self, frequency)               |  构造函数              |
| sleep(self)                 | 挂起 考虑上一次的rate.sleep()时间  |
| Time remaining(self)                   | 成员函数 剩余sleep时间 |
| **Duration类 **               |   |
|\__init__(self,secs=0, nsecs=0) | 构造函数 秒和纳秒  |

Time的now是静态方法`rospy.Time.now()`。Duration理解为一段时间，Time理解为一个时刻，所以它们可以相加，Time+Duratoin=Time，Duration+Duration=Duration，Time-Time=Duration。

**topic_demo**

ROSPY是ROS提供给我们用Python来和ROS的topic、service、action、param交互的接口。先来看看ROSPY的文档，官方给的文档包括这几个主要部分。

- 初始化函数，在开始ROS程序前都必须调用这个初始化函数
- init_node(name)，与topic、service、pararm交互的公共接口
- master，可以向master查询信息
- service，向service查询信息
- param，向param server查询信息
- names，ROS计算图的资源名称

任务要求：两个node，一个发布模拟的GPS消息（格式为自定义，包括坐标和工作状态），另一个接收并处理该信息（计算到原点的距离）。

一般的topic场景类似此题，一个node发布消息，例如是一个传感器，发布测量得数值。发布的数据是从传感器里读出来的。如果厂家没有提供ROS支持，我们就得写这么一个node，把数据封装成ROS支持的格式发布出topic。这个例子是模拟了传感器的GPS数据，把它publish出来。另一个node是接收这个数据后对它做一些处理。这个例子里是计算距离，实际应用不会这么简单。希望通过这个例子让大家明白用ROSPY来写一个topic通信的流程。


开发步骤：

1. 创建Package，可以使用Roboware Studio使用图形界面创建  

2. 创建并编写msg  

3. 编写talker.py  

4. 编写listener.py  

5. 编译Package（设置CMakeList.txt&package.xml）

6. 编译

7. 运行 

具体操作：

1. 使用Roboware创建工作区和ROS包

2. gps.msg

   gps.msg文件中包括1个`string`变量表示状态信息，两个`float32`32位浮点数变量表示GPS的x轴和y轴的坐标值。

```
string state    # 状态
float32 x       # GPS x坐标
float32 y       # GPS y坐标
```

3. pylistener.py

pylistener.py是话题信息接收程序。程序从`if __name__ == '__main__‘:`处进入，首先调用`listener()`，在`listener()`中我们首先使用`rospy.init_node('pylistener')`初始化一个节点`pylistener`，之后使用`rospy.Subscriber('gps_info', gps, callback)`订阅话题`gps_info`的信息，它的数据类型是`gps`，调用回调方法`callback`。`def callback(gps)`中输入是接收到的`gps`格式的数据，` distance = math.sqrt(math.pow(gps.x, 2) + math.pow(gps.y, 2))`，处理过的数据赋值给变量`distance`，`rospy.loginfo('Listener: GPS distance=%f, state : %s', distance, gps.state)`，将处理过的数据使用`loginfo`在终端后台打印出来。从回调函数返回后`rospy.spin()`，讲程序阻塞到`rospy.Subscriber('gps_info', gps, callback)`，在程序终端时退出。程序如下

```python
#!/usr/bin/env python

import rospy
import math
from topic_demo.msg import gps

def callback(gps):
        distance = math.sqrt(math.pow(gps.x, 2) + math.pow(gps.y, 2))
        rospy.loginfo('Listener: GPS distance=%f, state : %s', distance, gps.state)

def listener():
       rospy.init_node('pylistener')
       rospy.Subscriber('gps_info', gps, callback)
       rospy.spin()

if __name__ == '__main__':
       listener()
```

4. pytalker.py

程序是话题信息发布程序。程序从`if __name__ == '__main__‘:`处进入，首先调用`talker()`，`talker()`中首先初始化节点`pytalker`，`rospy.init_node('pytalker', anonymous=True)`。之后发布话题`gps_info`，它的类型是`gps`。之后为`gps`类型中的变量设置初值`state = 'working'`，`x = 1.0`和`y = 2.0`。`rate = rospy.Rate(1)`设置数据处理速度为每秒1次，即以下一个循环共1秒钟。

```python
        rospy.loginfo('Talker: GPS: x=%f , y = %f')
        pub.publish(gps(state, x, y))
        x = 1.03 * x
        y = 1.01 * y
        rate.sleep()
```

`while not rospy.is_shutdown():`循环内的程序是数据处理的主体，`pub.publish(gps(state, x, y))`是话题发布，发布的数据是`gps(state, x, y)`，之后改变`x`，`y` 的值。`rate.sleep()`到1s后，重复`while`中的程序。


```python
#!/usr/bin/env python
import rospy
from topic_demo.msg import gps

def talker():
    rospy.init_node('pytalker', anonymous=True)
    pub = rospy.Publisher('gps_info', gps, queue_size=10)
    x = 1.0
    y = 2.0
    state = 'working'
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        rospy.loginfo('Talker: GPS: x=%f , y = %f', x, y)
        pub.publish(gps(state, x, y))
        x = 1.03 * x
        y = 1.01 * y
        rate.sleep()

if __name__ == '__main__':
    talker()
```

5. CMakeLists.txt（使用Roboware Studio时省略此步，Roboware Studio会自动创建和配置）

```makefile
cmake_minimum_required(VERSION 2.8.3)
project(topic_demo) 

find_package(catkin REQUIRED COMPONENTS message_generation roscpp rospy std_msgs)
add_message_files(FILES gps.msg)
generate_messages(DEPENDENCIES std_msgs)

catkin_package(CATKIN_DEPENDS  roscpp rospy std_msgs message_runtime)

include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(talker src/talker.cpp )
add_dependencies(talker topic_demo_generate_messages_cpp)
target_link_libraries(talker ${catkin_LIBRARIES})

add_executable(listener src/listener.cpp )
add_dependencies(listener topic_demo_generate_messages_cpp)
target_link_libraries(listener ${catkin_LIBRARIES})
```

package.xml（使用Roboware Studio时省略此步，Roboware Studio会自动创建和配置）

```xml
<?xml version="1.0"?>
<package>
  <name>topic_demo</name>
  <version>0.0.0</version>
  <description>The publish_subscribe_demo package</description>
  <maintainer email="luoyunxiang@droid.com">luoyunxiang</maintainer>
  <license>BSD</license>
  <buildtool_depend>catkin</buildtool_depend>
  <build_depend>message_generation</build_depend>
  <build_depend>roscpp</build_depend>
  <build_depend>rospy</build_depend>
  <build_depend>std_msgs</build_depend>
  <run_depend>roscpp</run_depend>
  <run_depend>rospy</run_depend>
  <run_depend>std_msgs</run_depend>
  <run_depend>message_runtime</run_depend>
  <export>
    <!-- Other tools can request additional information be placed here -->
   </export>
</package>
```

6. 编译

```bash
cd ~/catkin_ws
catkin_make
```

8. 运行

- 设置权限

```bash
chmod u+x pytalker.py pylistener.py
```

- 刷新ROS环境

```bash
source ~/catkin_ws/devel/setup.bash
```

- 启动master

```bash
roscore
```

- 运行程序

```bash
rosrun 包名 pytalker.py
rosrun 包名 pylistener.py
```

**service_demo**

接着我们来看一个service的例子。

任务要求：两个node，一个发布请求（格式自定义），另一个接收处理该信息，并返回信息。

开发步骤：

1. 创建package  

2. 编写srv文件  

3. 编写server_demo.py  

4. 编写client_demo.py 

5. 编译（设置CMakeList.txt&package.xml）

具体操作：

1. 创建package

   使用Roboware Studio创建

2. 编写srv 

Greeting.srv

`string name`，`int32 age`是服务中`request`下的数据，`string feedback`是`response`下的数据。

```
string name
int32 age
---
string feedback
```

Greeting.srv编译后会产生三个类，分别是

- service_demo.srv.Greeting
- service_demo.srv.GreetingRequest
- service_demo.srv.GreetingResponse

其中service_demo是包名，在开发ROSPY程序时我们需要用`from service_demo.srv import *`来import这三个类。

3. 编写server_demo.py

程序是`service`服务端程序。程序从`if __name__ == '__main__‘:`处进入，调用`server_srv()`，`server_srv()`中首先使用`rospy.init_node('greetings_server')`初始化节点`greetings_server`，之后创建`service`服务端`s = rospy.Service('greetings', Greeting, handle_function)`，其中服务的名称是`greetings`，类型是`Greeting`，回调函数是`handle_function`。进入回调函数`handle_function(req)`，`req`是`request`数据。处理和返回`response`数据，`return GreetingResponse('Hi %s. I’m server!'%req.name)`，其中返回的字符串内容是`'Hi %s. I’m server!'`和`req.name`变量值。跳回`server_srv()`后，`rospy.spin()`阻塞程序退出，等待客户端新的访问`s = rospy.Service('greetings', Greeting, handle_function) `。

```python
#!/usr/bin/env python
# coding:utf-8

# 上面指定编码utf-8，使python能够识别中文

# 加载必需模块，注意service模块的加载方式，from 包名.srv import *
# 其中srv指的是在包根目录下的srv文件夹，也即srv模块
import rospy
from service_demo.srv import *

def server_srv():
    # 初始化节点，命名为 "greetings_server"
    rospy.init_node("greetings_server")
    # 定义service的server端，service名称为"greetings"， service类型为Greeting
    # 收到的request请求信息将作为参数传递给handle_function进行处理
    s = rospy.Service("greetings", Greeting, handle_function)
    rospy.loginfo("Ready to handle the request:")
    # 阻塞程序结束
    rospy.spin()

# Define the handle function to handle the request inputs
def handle_function(req):
    # 注意我们是如何调用request请求内容的，与前面client端相似，都是将其认为是一个对象的属性，通过对象调用属性，在我们定义
    # 的Service_demo类型的service中，request部分的内容包含两个变量，一个是字符串类型的name，另外一个是整数类型的age
    rospy.loginfo( 'Request from %s with age %d', req.name, req.age)
    # 返回一个Service_demoResponse实例化对象，其实就是返回一个response的对象，其包含的内容为我们再Service_demo.srv中定义的
    # response部分的内容，我们定义了一个string类型的变量，因此，此处实例化时传入字符串即可
    return GreetingResponse("Hi %s. I' server!"%req.name)

# 如果单独运行此文件，则将上面定义的server_srv作为主函数运行
if __name__=="__main__":
    server_srv()
```

在ROSPY的处理函数里，传入的只是request，返回值是response，直接返回GreetingResponse类型的变量。

4. client_demo.py

程序是`service`客户端程序。程序从`if __name__ == '__main__‘:`处进入，调用`client_srv()`，`client_srv()`中首先初始化节点`greetings_client`，`rospy.init_node('greetings_client')`，之后使用`greetings_client('HAN', 20)`，将`request`赋值，同时访问服务端，将`response`的数据赋值给变量`rosp`，并`rospy.loginfo('Message From Server: %s'%rosp.feedback)`打印到终端。

```python
#!/usr/bin/env python
# coding:utf-8

# 上面的第二句指定编码类型为utf-8，是为了使python能够识别中文

# 加载所需模块
import rospy
from service_demo.srv import *

def client_srv():
    rospy.init_node('greetings_client')
    # 等待有可用的服务 "greetings"
    rospy.wait_for_service("greetings")
    try:
        # 定义service客户端，service名称为“greetings”，service类型为Greeting
        greetings_client = rospy.ServiceProxy("greetings",Greeting)

        # 向server端发送请求，发送的request内容为name和age,其值分别为"HAN", 20
        # 注意，此处发送的request内容与service文件中定义的request部分的属性是一致的
        #resp = greetings_client("HAN",20)
        resp = greetings_client.call("HAN",20)

        # 打印处理结果，注意调用response的方法，类似于从resp对象中调取response属性
        rospy.loginfo("Message From server:%s"%resp.feedback)
    except rospy.ServiceException, e:
        rospy.logwarn("Service call failed: %s"%e)

# 如果单独运行此文件，则将上面函数client_srv()作为主函数运行
if __name__=="__main__":
    client_srv()
```

Greetings_client用greetings_client.call()来调用服务。

**param_demo**

程序是ROS`param`相关函数的演示程序。程序从`if __name__ == '__main__‘:`处进入，调用`param_demo()`，首先初始化节点`param_demo`，`rospy.init_node('param_demo')`。` rate = rospy.Rate(1)`设置数据处理时间为每秒1次，当程序不异常退出时，执行`while(not rospy.is_shutdown):`中循环。

`parameter1 = rospy.get_param('/param1')`获取全局参数`/param1`

`rospy.delete_param('/param1')`删除全局参数`/param1`

```python
if(rospy.has_param('/param2')):
 	       rospy.loginfo('/param2 exists')
```

`if(rospy.has_param('/param2'))`如果存在全局参数`/param2`，打印`loginfo`信息。

```python
import rospy

def param_demo():
       rospy.init_node('param_demo')
       rate = rospy.Rate(1)
       while(not rospy.is_shutdown):
              parameter1 = rospy.get_param('/param1')
              rospy.delete_param('/param1')
              rospy.set_param('/param1', 1)
              if(rospy.has_param('/param2')):
 	       rospy.loginfo('/param2 exists')
              else:
                       rospy.loginfo('/param3 does not exist')

              params = rospy.get_param_names()
              rospy.loginfo('param list: %s', params)
        rate.sleep()

if __name__='__main__':
      param_demo()
```

## 2. ROSPY练习

下面我们结合XBot机器人来做些练习。

**ROSPY Topic**

在Ubuntu的终端里输入下面这段命令：

这条命令用于向`/cmd_vel`话题，发类型为`geometry_msgs/Twist`的信息，其中`linear`下`x`方向，机器人向前方向的速度设置为每秒0.5米，`angular`下`z`方向，机器人顺时针旋转，速度为每秒0.5米。此信号值发布一次。

```bash
rostopic pub /cmd_vel geometry_msgs/Twist "linear:
  x: 0.5
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.5"
```

在输入命令的时候，你可以尝试使用自动补全的功能，比如你在输入`rosto`的时候按下`Tab`键，它就会自动补全成`rostopic`，通过这一方式也可以帮助你检查是否输入了错的命令。刚才输入的命令有关键词pub，它是用来发布topic的，在这个例子里我们发布的话题是`/cmd_vel`这是一个在ROS中比较常见的话题。那么我们通过这个命令发布了什么东西呢？我们发布的是后面的`geometry_msgs/Twist`这样一个消息(message)，它包含两部分，分别是线速度和角速度。通过这一命令我们可以直接发布机器人的速度信息，通过仿真环境中的或者实际环境中的控制器使机器人运动起来，运行结果如下图。

![Example 1.1](src/images/Figure_5.2.1.gif  "Example 1.1")

在这一例子中，我们让机器人沿着x轴的方向，也就是前方以0.5m/s的速度运动，同时有一个0.5rad/s的角速度绕着z轴进行旋转。一旦发布了这一消息，机器人就会按照消息上的命令一直执行，要想使机器人停下来需要重新发布话题消息，将机器人的线速度和角速度都设置为0，即：

```bash
rostopic pub /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
```

好的，我们用ROSPY替换以上命令功能。

**仿真环境下**

1. 编写程序topic_demo1.py

首先`rospy.init_node('topic_demo')`初始化节点`topic_demo`，`pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)`，创建话题发布程序，话题是`/cmd_vel`，消息的数据类型是`Twist`，设置数据处理时间是每秒1次。机器人速度赋值`move.linear.x = 0.5, move.angular.z = 0.5`。

```python
for i in xrange(5):
    pub.publish(move)
    rate.sleep()
```

执行5次，共5s，移动命令。之后将机器人速度设置为0，`move.linear.x = 0, move.angular.z = 0`，发布消息是机器人停止运动，`pub.publish(move)`。

```python
#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse # import the service message python classes generated from Empty.srv.
from geometry_msgs.msg import Twist

rospy.init_node('topic_demo')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(1)
move = Twist()
move.linear.x = 0.5
move.angular.z = 0.5
for i in xrange(5):
    pub.publish(move)
    rate.sleep()
    
move.linear.x = 0
move.angular.z = 0
pub.publish(move)
```
2. 添加ROS主从配置

```
vim ~/.bashrc
```

```bash
#export ROS_MASTER_URI=http://192.168.8.101:11311
export ROS_MASTER_URI=http://127.0.0.1:11311
#export ROS_HOSTNAME=192.168.8.xxx
export ROS_HOSTNAME=127.0.0.1
```

3. 启动XBot Gazebo仿真

```bash
roslaunch robot_sim_demo robot_spawn.launch
```

4. 运行程序

```bash
python topic_demo1.py
```

**XBot环境下**

1. 编写程序topic_demo1.py

```python
#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse 
from geometry_msgs.msg import Twist

rospy.init_node('topic_demo')
pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
rate = rospy.Rate(1)
move = Twist()
move.linear.x = 0.5
move.angular.z = 0.5
for i in xrange(5):
    pub.publish(move)
    rate.sleep()
    
move.linear.x = 0
move.angular.z = 0
pub.publish(move)
```

2. 添加ROS主从配置

```bash
vim ~/.bashrc
```

```bash
export ROS_MASTER_URI=http://192.168.8.101:11311
#export ROS_MASTER_URI=http://127.0.0.1:11311
export ROS_HOSTNAME=192.168.8.xxx
#export ROS_HOSTNAME=127.0.0.1
```

3. 启动XBot

```bash
roslaunch xbot_bringup xbot-u.launch
```
4. 运行程序topic_demo1.py

```bash
python topic_demo1.py
```

话题之所以如此重要，是因为在机器人的编程中离不开各个模块之间的通信，话题承担了这一重任，通过订阅和发布的操作实现传感器和机器人的通信，从而实现机器人控制。

**ROSPY  Service**

下面我们介绍ROS中的服务(service)，正如其名字所表示的那样在ROS中你可以使用服务实现各种各样的功能，并且由机器人提供并方便调用。服务相对来说要比话题更复杂一些，它共有两个部分即服务器(server)部分和客户端(client)部分。服务器是提供服务的一方比如建立一个服务让机器人移动五秒后停下，而客户端是请求使用服务的一方比如调用刚才说的那个服务以使机器人真正去移动。下面我们进行一个示例，来大致了解服务运行的过程。

```bash
roslaunch my_service my_service.launch
rosservice call /my_service "{}"
```

第一个命令是使用`roslauch`运行service_launch.launch这一launch文件，这个文件的内容是运行一个名为service_test_node的节点，它运行的逻辑也就是程序是由service_code.py来实现的，具体的程序都在下面给出了，这个节点即是我们创建的服务器，其中my_callback即是定义的服务。而第二个命令则是调用上述定义的服务。通过调用这一服务，我们可以让我们的机器人运动5秒后停下来并结束服务。

1. 编写my_srv.srv

```
int32 time
float64 linear_velocity
float64 angular_velocity
---
bool success
```

**仿真环境下**

2. 编写服务端程序service_server.py

此程序是`service`服务端程序，首先初始化节点`service_server`，`rospy.init_node('service_server')`，之后创建话题`/cmd_vel`的发布端，`pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)`，数据类型是`Twist`，数据处理时间为每秒1次，创建`service`服务端，`my_service = rospy.Service('/my_service', my_srv, my_callback)`，其中`service`名称是`/my_service`，类型是`my_srv`，调用回调函数`my_callback`，`my_callback(request):`中输入是`request`，对速度赋值

```python
    twist = Twist()
    twist.linear.x = request.linear_velocity
    twist.angular.z = request.angular_velocity
```

设置机器人运动的时间`time = request.time`，循环发布速度信息`pub.publish(twist)`，时间变量每次循环减1。时间变量减到0时，终端打印信息，返回`True`，`rospy.spin()`对程序进行阻塞，等待用户端请求`my_service = rospy.Service('/my_service', my_srv, my_callback)`。


```python
#! /usr/bin/env python

import rospy
from my_service.srv import my_srv, my_srvResponse
from geometry_msgs.msg import Twist


def my_callback(request):
    print('Come on! XBot!')
    twist = Twist()
    twist.linear.x = request.linear_velocity
    twist.angular.z = request.angular_velocity
    time = request.time
    while time >= 0:
        pub.publish(twist)
        time -= 1
        rate.sleep()
    print('XBot finished!')
    return True
    

rospy.init_node('service_server')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(1)
my_service = rospy.Service('/my_service', my_srv, my_callback)
rospy.spin()
```
3. 编写客户端程序service_client.py
```python
#! /usr/bin/env python

import rospy
from my_service.srv import my_srv, my_srvRequest
import sys

rospy.init_node('service_client')
rospy.wait_for_service('/my_service')
my_service = rospy.ServiceProxy('/my_service', my_srv)
req = my_srvRequest()
req.linear_velocity = 0.5
req.angular_velocity = 0.5
req.time = 10
result = my_service(req)
print(result)
```

4. 编写my_service.launch

```xml
<launch>
    <node pkg="my_service" type="service_server.py" name="server" output="screen">
    </node>
	<node pkg="my_service" type="service_client.py" name="client" output="screen">
    </node>
</launch>
```

5. 添加ROS主从配置

```bash
vim ~/.bashrc
```

```bash
#export ROS_MASTER_URI=http://192.168.8.101:11311
export ROS_MASTER_URI=http://127.0.0.1:11311
#export ROS_HOSTNAME=192.168.8.xxx
export ROS_HOSTNAME=127.0.0.1
```

6. 启动XBot Gazebo仿真

```bash
roslaunch robot_sim_demo robot_spawn.launch
```

7. 运行程序

```bash
roslaunch 包名 my_service.launch
```

可以看到机器人运动的结果和在使用话题时的情况十分相似，服务这一机制在ROS中也是十分重要而且功能强大的一个工具。(XBot下）

![Example 1.2](src/images/Figure_5.2.2.gif  "Example 1.2")

**ROSPy Action**

回顾一下，我们刚才演示了ROSPY中的话题和服务机制，这两个机制是ROS中非常非常重要的概念。除此之外，我们演示一下动作(Action)。动作与服务是十分相似的两个概念，在动作中同样像服务那样支持你的机器人提供各种各样功能的类似的服务，你也同样可以去调用这些任务但是动作将会增加一些复杂性。其最主要的区别在于在你使用服务并且当你调用一个服务的时候，你必须要一直等待直到机器人完成了这一命令，例如在之前的例子中就是必须要等待机器人运动5秒并停下来后，才能继续调用并响应其他的服务，而action则不同。在执行一个动作时，你也完全可以去执行其他动作去控制机器人的其他模块，与此同时action带有一个反馈机制，可以在任务实施的过程中不断反馈任务的实施进度，甚至还可以在任务实施的过程中终止运行。比如接下来的这个例子，我们运行命令。

```bash
roslaunch action_demo action_launch.launch
rostopic pub /action_demo/goal actionlib/TestActionGoal "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
goal_id:
  stamp:
    secs: 0
    nsecs: 0
  id: ''
goal:
  goal: 10"
```
1. 编写.action文件，my_action.action

```bash
int32 goal_time
geometry_msgs/Twist velocity
---
bool success
---
float64 progress
```

**仿真环境下**

2. 编写action_server.py

```python
#! /usr/bin/env python

import rospy
import actionlib
from my_action.msg import my_actionAction, my_actionFeedback, my_actionResult
from geometry_msgs.msg import Twist


def my_goal_callback(goal):
    print('Come on! Little XBot!')
    time = goal.goal_time
    while time >= 0:
        progress = my_actionFeedback(1 - (time*1.0) / goal.goal_time)
        my_action_service.publish_feedback(progress)
        time -= 1
        pub.publish(goal.velocity)
        rate.sleep()
    print('XBot finished!')
    result = my_actionResult(True)
    my_action_service.set_succeeded(result)

rospy.init_node('action_server')
rate = rospy.Rate(1)
my_action_service = actionlib.SimpleActionServer('/my_action', my_actionAction, my_goal_callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rospy.spin()
```

**XBot环境下**

2. 编写action_server_xbot.py

```python
#! /usr/bin/env python

import rospy
import actionlib
from my_action.msg import my_actionAction, my_actionFeedback, my_actionResult
from geometry_msgs.msg import Twist


def my_goal_callback(goal):
    print('Come on! Little XBot!')
    time = goal.goal_time
    while time >= 0:
        progress = my_actionFeedback(1 - (time*1.0) / goal.goal_time)
        my_action_service.publish_feedback(progress)
        time -= 1
        pub.publish(goal.velocity)
        rate.sleep()
    print('XBot finished!')
    result = my_actionResult(True)
    my_action_service.set_succeeded(result)

rospy.init_node('action_server')
rate = rospy.Rate(1)
my_action_service = actionlib.SimpleActionServer('/my_action', my_actionAction, my_goal_callback)
pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)

rospy.spin()
```

**以下仿真和XBot下相同**

3. 编写action_client.py

```python
#! /usr/bin/env python

import rospy
from my_action.msg import my_actionAction, my_actionGoal, my_actionFeedback
from geometry_msgs.msg import Twist
import actionlib


def feedback_callback(feed):
    print(feed)


rospy.init_node('service_client')
my_action_client = actionlib.SimpleActionClient('/my_action', my_actionAction)
my_action_client.wait_for_server()

goal = my_actionGoal()
goal.goal_time = 10
goal.velocity.linear.x = 0.5
goal.velocity.angular.z = 0.5
my_action_client.send_goal(goal, feedback_cb=feedback_callback)

my_action_client.wait_for_result()
print(my_action_client.get_result())
```

4. 编写launch文件，my_actkin.launch

```xml
<launch>
    <node pkg="my_action" type="action_server.py" name="server" output="screen">
    </node>
    <node pkg="my_action" type="action_client.py" name="client" output="screen">
    </node>
</launch>
```

**仿真环境下**

5. 添加ROS主从配置

```bash
vim ~/.bashrc
```

```bash
#export ROS_MASTER_URI=http://192.168.8.101:11311
export ROS_MASTER_URI=http://127.0.0.1:11311
#export ROS_HOSTNAME=192.168.8.xxx
export ROS_HOSTNAME=127.0.0.1
```

6. 启动XBot Gazebo仿真

```bash
roslaunch robot_sim_demo robot_spawn.launch
```

7. 运行程序

```bash
roslaunch 包名 my_actkin.launch
```

![Example 1.3](src/images/Figure_5.2.3.gif  "Example 1.3")

**XBot环境下**

5. 添加ROS主从配置

```bash
vim ~/.bashrc
```

```bash
export ROS_MASTER_URI=http://192.168.8.101:11311
#export ROS_MASTER_URI=http://127.0.0.1:11311
export ROS_HOSTNAME=192.168.8.xxx
#export ROS_HOSTNAME=127.0.0.1
```

6. 启动XBot

```bash
roslaunch xbot_bringup xbot-u.launch
```

7. 运行程序my_actkin.launch

```bash
roslaunch 包名 my_actkin.launch
```

感谢大家，我们这讲就到这里。
