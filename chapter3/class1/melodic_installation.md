# 附件-Ubuntu安装

## Ubuntu 18.04 的安装和配置

**软硬件要求** 

- USB2.0或3.0盘 (最小2GB)
- Internet网络连接
- 安装盘制作工具 [Rufus下载](https://rufus.ie/)
Rufus是一个Linux USB安装盘制作工具，可用于格式化和创建可启动的USB flash drives
- Ubuntu Desktop 18.04.4 LTS 安装镜像 [下载](https://isrc.iscas.ac.cn/mirror/ubuntu-release/)

***有些比较新的电脑可能会出现驱动问题（比如：没有WIFI功能）。此时，我们需要安装Ubuntu 18.04。 Ubuntu 18.04对应 ROS 版本 Melodic***

**安装ROS**

现在我们来安装和配置ROS环境，在操作演示之前，先跟大家介绍一下ROS的网站ROS Wiki。我们打开浏览器，地址是ros.org，回车那这就是ROS的官方网站，我们可以看到有各种介绍和新闻，最重要的就是这里，ROS Wiki，相当于ROS提供的一个百科，或者官方手册。里面包含了从安装到入门，各种软件包，以及ROS支持的机器人、传感器，还有相关的书籍和课程。做ROS开发，这里会是你经常来的地方。我们的安装从install开始，选好ROS版本，ROS Kinetic版本是在Ubuntu 16.04上运行，千万不要安装错了，然后是安装步骤，我们看到很多命令，为了节约时间，我总结了一下，大致就四步，就四步，如果你看不懂命令行什么意思， 不要紧，复制进terminal里就可以了，首先是添加镜像源，这里推荐国内的源，我们用的是在软件所专门给课程做的镜像。第二步是添加公钥，我们把它拷进来，然后需要更新一下系统 `sudo apt-get update`。这里提醒一下各位，在`Ubuntu 18.04`上，apt-get有了一个简化版本apt。下一步是安装ROS，请注意选对版本，这里是`ros-melodic`，ROS我们就安装完了。



1、替换Ubuntu源镜像

- 首先备份本地默认源列表文件 `sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak`

- 执行以下命令，替换源

```bash
sudo wget https://mirror.iscas.ac.cn/mirror/xlab_ubuntu18.04.list -O /etc/apt/sources.list.d/xlab_ubuntu18.04.list
```

或者单独下载软件源文件 [xlab_ubuntu18.04.list](https://mirror.iscas.ac.cn/mirror/xlab_ubuntu18.04.list)

2、Ubuntu添加 ROS 源命令

- 首先添加 ROS 源公钥

```bash
# wget -qO - https://isrc.iscas.ac.cn/mirror/ros/ros.gpg | sudo apt-key add -

sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
```
- 添加软件源列表

```bash
sudo sh -c 'echo "deb http://isrc.iscas.ac.cn/mirror/ros/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```

3、**系统更新**

升级软件列表

```bash
sudo apt update 
```
下一步来配置好ROS环境，三步，照着说明来做就行。rosdep是一个系统依赖项的管理工具，把它装好，然后把我们安装好的ROS环境导入到bashrc。这里注意，我们刚才apt安装的ros安装到哪里了？ 就在/opt/ros/melodic下面。我们希望每次打开一个终端，就可以添加ros环境，所以我们把ROS环境放到.bashrc里面，每次自动刷新环境。最后是安装ROS包管理的一些工具，成功之后我们的ROS就安装完了。

**桌面全安装（推荐）**: ROS, rqt, rviz, robot-generic libraries, 2D/3D simulators, navigation and 2D/3D perception

```bash
sudo apt install ros-melodic-desktop-full
sudo apt install ros-melodic-ros-controllers
```

**单独安装特定包**：用户可以安装特定的 ROS package

```bash
sudo apt install ros-melodic-PACKAGE
e.g.
sudo apt install ros-melodic-slam-gmapping
```

**查找可用的packages**

```bash
apt search ros-melodic
```

- **rosdep初始化**
使用ROS之前你需要使用rosdep进行初始化。rosdep用于安装ROS核心部件编译或运行时需要的系统依赖。 

```bash
sudo apt install python-rosdep
sudo rosdep init
rosdep update
```

- **环境设置**
把ROS环境变量自动添加到每次自动启动的shell session
```bash
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
**ROS工具安装** 

目前已完成了ROS核心包运行环境安装。为了创建和管理ROS工作空间，需要安装大量工具，例如 rosinstall 是一个高频使用的命令行工具，它用于下载ROS package需要的大量资源

**以下命令可安装这些工具** 

```bash
sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential
```

- **ROS安装成功验证**

输入roscore命令可以验证ROS已经安装成功

```bash
roscore
```

![2](./src/images/Figure_1.3.2.png)

打开一个终端，输入`roscore`，如果显示如上图，恭喜你，已经成功的安装，ROS安装配置就到这里。

## 4. 教学代码包的安装

接下来我们会下载并安装本书配套的ROS-Academy-for-Beginners软件包，演示源码包下载-编译-
运行的完整流程。后续章节的主要代码都基于这个软件包，所以希望大家熟悉这一过程。

- 登录重德智能GitHub网页 ： https://github.com/DroidAITech/
- 下载和安装教学软件包：ROS-Academy-for-Beginners

教学软件包源代码在github上。

1.确保git已经安装
2.创建一个名为catkin_ws的工作空间，在它的的src路径下克隆ROS-Academy-for-Beginners软件包
3.安装依赖项，查看Gazebo版本
4.在工作空间下进行编译
5.source环境变量
6.运行仿真环境

ROS-Academic-for-Beginners教学包是贯穿整个学习过程所使用的教学代码包，本教学包是源码包，需要下载后对其进行编译才可以使用。该教学包中集成了Xbot仿真环境，在后续的课程中会大量的用到，初学者通过对本章的学习可以熟悉XBot仿真环境。

**任务一：安装教学包**

1.二级制包和源码包

第一步，需要弄清楚二进制包和源码包的区别。一般软件包可以分成二进制包和源码包两种，二进制包里包含了已经编译完成，并可以直接运行的程序，源码包里是程序的原始代码，下载完成后必须编译成可执行文件才可以安装。ROS-Academic-for-Beginners教学包是源码包。

2.建立工作空间

catkin工作空间是组织和管理包的文件夹，以catkin工具进行编译；catkin工作空间下应该有源码src目录用于存放源代码。第二步就是我们需要建立一个工作空间；ROS的工作空间使用到了catkin，catkin工作空间是组织和管理包的文件夹，以catkin工具进行编译，catkin工作空间下应该有源码src目录用于存放源代码。

3.下载源码包

git clone命令用于从服务器上克隆完整的git仓库（包括代码和版本信息）到单机上；需要将教学源码包克隆到源码目录下。第三步，建立好工作空间后我们需要将教学包源码下载下来，刚刚也说了ROS-Academic-for-Beginners教学包是源码包，需要将其下载并编译才可以使用。

4.安装依赖项

缺少依赖项会导致软件包无法正常编译和运行。第四步，我们需要安装教学包所需要的依赖项，因为缺少依赖项会导致软件包无法正常编译和运行。

5.查看Gazebo版本

第五步，查看Gazebo的版本，Gazebo是ROS中的一个实现物理仿真的工具包，Gazebo本身就是一款机器人的仿真软件，可以模拟机器人以及环境中的很多物理特性，这一步主要是看一看Gazebo的版本是不是在7.0 以上，如果低于7.0就需要对其进行更新。

6.编译工作空间

最后一步也就是编译，编译的过程中用到了catkin_make，在来学习catkin_make之前我们需要先了解一下cmake，cmake是一个跨平台的编译(Build)工具,可以用简单的语句来描述所有平台的编译过程；cmake的核心是读取一个容易理解的文本文件CMakeLists.txt，通过使用cmake命令根据CMakeLists.txt内容生成对用的项目文件；关于cmake的知识，推荐大家花一些时间去阅读一下《CMake实践》这本书。catkin是ROS定制的编译构建系统，是对cmake的扩展。

**1  二级制包 vs 源码包**

- 二进制包和源码包的安装是有区别的
- 二进制包里不包含源码，可通过`sudo apt install`进行下载和安装
- 源码包的安装必须将源码`git clone`到本地并进行编译

| 区别          | 二进制包                   | 源代码包                         |
| ------------- | -------------------------- | -------------------------------- |
| 下载方式      | apt- get install／直接下载 | git clone /连接下载源代码        |
| ROS包存放位置 | /opt/ros/melodic           | 通常 ~/catkin_ws/src             |
| 编译方式      | 无需编译                   | 通过make/cmake/caktin            |
| 来源          | 官方apt软件源              | 开源项目、第三方开发者           |
| 扩展性        | 无法修改                   | 通过源代码修改                   |
| 可读性        | 无法查看源代码             | 方便阅读源代码                   |
| 优点          | 下载简单，安装方便         | 源码可修改，便于定制功能         |
| 缺点          | 无法修改                   | 编译工具、软件包依赖、版本和参数 |
| 应用场景      | 基础软件                   | 需要查看、开发和修改的程序       |

**2  建立工作空间**

`mkdir -p catkin_ws/src`
其中工作空间` catkin_ws`名可任意修改，但工作空间下必须带有src目录。关于catkin工作空间的组织和结构，这里先不介绍，我们会在下一节向大家详细的介绍，在这里我们需要注意的是catkin工作空间下应该有源码src目录用于存放源代码；`mkdir -p catkin_ws/src`这个是建立catkin工作空间的指令，工作空间的名字可以随便取，但是一定要包含src目录。

```bash
mkdir -p catkin_ws/src          #创建catkin工作空间
cd catkin_ws/src                #进入catkin_ws下的src目录
```

**3  下载源码包**

建立好工作空间之后，我们需要将教学包源码下载到src目录下用于后续对教学包源码的编译；首先我们需要在github上找到我们的教学包；教学包下面有本教学包的安装教程，大家可以根据教程完成对教学包的安装；下载到本地之前我们需要确认系统中是否已经安装git；源码需要下载到src目录下，可以通过教学包的地址直接进行clone。

```bash
sudo apt install git        #安装git
cd catkin_ws/src            #进入catkin_ws下的src目录
git clone https://github.com/DroidAITech/ROS-Academy-for-Beginners.git	#下载教学包
```

**4  安装依赖**

下载完代码后，我们需要安装其相应的依赖，缺少依赖会导致软件包无法正常编译和运行。

```bash
cd ~/catkin_ws  #进入catkin_ws目录
rosdep install --from-paths src --ignore-src --rosdistro=melodic -y  #安装依赖项
```

**5  查看Gazebo版本**

第五个子任务是查看Gazebo的版本，看一下Gazebo的版本是不是在9.10以上。在终端中输入`gazebo –v`用以查看gazebo版本。

![92](./src/images/Figure_1.4.2.png)

如果版本过低

```bash
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
#添加安装公钥

sudo apt update              #更新软件源
sudo apt install gazebo9     #更新Gazebo9
```

打开Gazebo

```bash
roslaunch gazebo_ros empty_world.launch #打开一个空的Gazebo世界
```
![94](./src/images/Figure_1.4.3.png)

**6  编译工作空间**

刷新环境变量方法只在本终端中有效，`source ~/catkin_ws/devel/setup.bash`是在本终端中刷新catkin工作空间环境变量。在新开的终端中需要重新刷新环境变量，为解决此问题，可将刷新指令添加到`~/.bashrc`文件中，`~/.bashrc`是一个bash脚本，会在打开新的终端时自动执行。

```bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```
`vim ~/.bashrc`修改~/.bashrc，添加环境变量和主从计算机，ROS使用分布式结构，主机运行Master节点，从机可运行各种进程，因此要设置ROS Master主机，设置方法为`export ROS_MASTER_URI=http://127.0.0.1:11311`，和设置从机`export ROS_HOSTNAME=127.0.0.1       `，使得分布在不同计算机上的程序可以彼此通信，以上例子是Master节点和从机都运行在笔记本电脑上。当连接XBot的WIFI时，XBot地址固定为`http://192.168.8.101:11311`，设置方法是`export ROS_MASTER_URI=http://192.168.8.101:11311`，从机是客户机，IP由DHCP动态分配，可使用`ifconfig`查看客户机IP。

```bash
source /opt/ros/melodic/setup.bash            #添加ROS Melodic环境
source ~/catkin_ws/devel/setup.bash           #添加ROS源码工作空间环境     

#添加主从机，当使用仿真时添加如下
export ROS_MASTER_URI=http://127.0.0.1:11311  #主机IP和端口，默认为11311端口
export ROS_HOSTNAME=127.0.0.1                 #从机IP。仿真为主从机使用同一台计算机

#添加主从机，当使用XBot时添加如下
export ROS_MASTER_URI=http://192.168.8.101:11311   #主机IP和端口，默认为11311端口
export ROS_HOSTNAME=192.168.8.x             #从机IP，请在笔记本上使用ifconfig查看实际IP
```
接下来就是本次教学包安装的最后一步了，编译。需要注意的是编译必须在源码所在的工作空间目录下。编译完成后必须刷新一下工作空间的环境，通过输入指令`source ~/catkin_ws/devel/setup.bash`来刷新环境，但是这样只满足于当前终端，在其他终端中需要重新刷新，为了使每次打开终端不用重新刷新环境，可以将`source`命令追加到`~/.bashrc`文件中。


```bash
# 1、打开终端，cd进入刚刚建好的工作空间下
cd ~/catkin_ws

# 2、输入指令catkin_make进行编译
catkin_make

# 当rosdep连接不上时,需根据反馈缺少的包,手动逐个安装ros-melodic-xx-xxx
sudo apt install ros-melodic-yocs-cmd-vel-mux

# 3、刷新环境变量
source ~/catkin_ws/devel/setup.bash

# 4、将”source ~/catkin_ws/devel/setup.bash"写入~/.bashrc
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

对`catkin_make`运行后终端部分内容解析如图。

**~/.bashrc**

![97](./src/images/Figure_1.4.5.png)

**编译后的工作空间**

安装完成后的教学包其内容如图所示

![99](./src/images/Figure_1.4.6.png)

以上教学包安装命令可总结为

```bash
sudo apt-get install git
mkdir -p catkin_ws/src
cd catkin_ws/src
git clone https://github.com/YunxiangLuo/roscode.git
cd ..
sudo rosdep install --from-paths src --ignore-src --rosdistro=melodic -y
catkin_make

echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
echo "export ROS_MASTER_URI=http://127.0.0.1:11311" >> ~/.bashrc
echo "export ROS_HOSTNAME=127.0.0.1" >> ~/.bashrc

source ~/.bashrc
```
启动XBot仿真
```bash
roslaunch robot_sim_demo robot_spawn.launch 
```

常见问题：Gazebo打开时有些会出现长时间等待或黑屏空白，因为http://gazebosim.org/models/地址已经变换http://models.gazebosim.org， 导致在线下载Gazebo模型文件时，访问无法自动转换地址。

解决方法

```bash
#1. 打开新终端，输入gazebo，打开gazebo
gazebo

#2. 关闭gazebo

#3. 打开新终端，cd ~/.gazebo/models/
cd ~/.gazebo/models/

# 4. 将课件包中src目录下的osrf-gazebo_models-e6d645674e8a.zip解压，把所有文件连同目录拷贝到~/.gazebo/models目录下
unzip osrf-gazebo_models-e6d645674e8a.zip -d ~/.gazebo/models
```

**任务二：XBot仿真环境**

接下来我们尝试在XBot仿真环境中控制XBot机器人移动。任务要点主要有以下两个方面，首先需要启动XBot环境，XBot仿真环境是根据我们软件博物馆实际结构建立的，我们可以通过在仿真环境中操作XBot机器人进行实验，在后续的课程中，我们会频繁的用得到；第二个就是要控制仿真环境中的Xbot机器人移动。

1. 启动XBot仿真环境。打开一个终端，输入以下命令。

```bash
roslaunch robot_sim_demo robot_spawn.launch
```

![Figure_1.4.7](./src/images/Figure_1.4.7.png)

当终端出现上图所示情况，说明之前ROS-Academic-for-Beginners教学包的安装没有问题，并且可以正确打开仿真环境。

常见问题：

当Gazebo进程未被关闭时，新启动Gazebo会出现错误。需要关闭所有Gazebo进程，参考以下命令

```bash
ps -ef | grep gazebo                  #查看gazebo进程
kill -9 xxx xxx xxx                   #kill gazebo进程
```

XBot仿真环境

![Figure_1.4.8](./src/images/Figure_1.4.8.png)

仿真环境如上图所示，是按照软件博物馆所做的模型，中间是XBot机器人，许多必要的参数已经加入了进去，像激光雷达等传感器。我们可以通过鼠标来移动我们的视角。

2. 控制XBot机器人移动

我们的任务需要在仿真环境中移动XBot机器人，我们需要调用控制机器人移动的程序，在我们的教学代码包里有一个早已经写好的Python脚本，我们可以直接调用。

```bash
#1、打开一个终端

#2、启动控制机器人移动的Python脚本
rosrun robot_sim_demo robot_keyboard_teleop.py
```

启动机器人控制

![Figure_1.4.9](./src/images/Figure_1.4.9.png)

调用该脚本后我们可以看到图示界面，从界面中我们可以看到控制小车移动的按键，使用i件控制机器人前进，k为停止键，j和l为左右转；通过这些命令，这里我们控制仿真环境中的机器人移动。

![Figure_1.4.10](./src/images/Figure_1.4.10.png)

![Figure_1.4.12](./src/images/Figure_1.4.12.png)![Figure_1.4.11](./src/images/Figure_1.4.11.png)

由于赛迪场地障碍物较多，可能在初次启动时xbot机器人不容易被发现，使用键盘控制移动过程中可能会将机器人卡在角落里，此时可以使用gazebo中的上帝视角对场地进行查看，在页面上端选择投影页面。

![Figure_1.4.13](./src/images/Figure_1.4.13.png)

查看当前摄像头所对应的画面，打开一个终端，输入一下命令，启动rqt_image_view。

```bash
rosrun image_view image_view image:=/camera/rgb/image_raw
```

![Figure_1.4.14](./src/images/Figure_1.4.14.png)

接下来我们尝试一下查看机器人的摄像头所对应的画面，可以看到此时摄像头正好面对窗户。

![Figure_1.4.15](./src/images/Figure_1.4.15.png)

我们打开一个终端，输入如下命令，启动键盘控制程序，如下。看一下机器人在运动过程中摄像头画面的变化情况。

```bash
roslaunch robot_sim_demo robot_keyboard_teleop.py
```
学会了控制机器人之后我们来了解一下，Xbot机器人的启动涉及到了多少个节点。可以看到gazebo的前端和后端，robot state publisher用来发布机器人当前的状态，spawner用来启动我们的机器人模型。cmd_vel_mux,这是一个速度选择器的节点。

```bash
rosnode list              #列出所有节点
```

![Figure_1.4.16](./src/images/Figure_1.4.16.png)

我们来看一下这个cmd_vel_mux节点的详细信息。

```bash
rosnode info /cmd_vel_mux  #查看/cmd_vel_mux节点信息
```

ROS入门教程的代码示例，包括以下ROS软件包

| 软件包                        | 内容                                                      |
| ----------------------------- | --------------------------------------------------------- |
| **robot_sim_demo**            | 机器人仿真程序，大部分示例会用到这个软件包                |
| **topic_demo**                | topic通信，自定义msg，包括C++和python两个版本实现         |
| **service_demo**              | service通信，自定义srv，分别以C++和python两种语言实现     |
| **action_demo**               | action通信，自定义action，C++和python两种语言实现         |
| **param_demo**                | param操作，分别以C++和python两种语言实现                  |
| **msgs_demo**                 | 演示msg、srv、action文件的格式规范                        |
| **tf_demo**                   | tf相关API操作演示，tf示例包括C++和python两个版本          |
| **tf_follower**               | 制作mybot机器人 实现mybot跟随xbot的功能                   |
| **urdf_demo**                 | 创建机器人urdf模型，在RViz中显示                          |
| **navigation_sim_demo**       | 导航演示工具包，包括AMCL, Odometry Navigation等演示       |
| **slam_sim_demo**             | 同步定位与建图演示，包括Gmapping, Karto, Hector等SLAM演示 |
| **robot_orbslam2_demo**       | ORB_SLAM2的演示                                           |
| **ros_academy_for_beginners** | Metapacakge示例，依赖了本仓库所有的pacakge                |
