[![ROS2 Version](https://img.shields.io/badge/ROS2-Jazzy-blue)](https://docs.ros.org/en/jazzy/)
[![Gazebo Version](https://img.shields.io/badge/Gazebo-Harmonic-orange)](https://gazebosim.org/)

这是一个基于 **ROS2 Jazzy** 的机器人功能包，包含 FishBot 机器人的 URDF/Xacro 模型文件，支持 **Gazebo Harmonic (gz-sim)** 仿真和 **RViz2** 可视化。

---

## 📋 功能特性

- ✅ 差分驱动底盘控制
- ✅ 激光雷达 (LiDAR) 仿真
- ✅ 摄像头仿真
- ✅ Gazebo Harmonic + RViz2 联合仿真
- ✅ ROS2 桥接通信

---

## 📦 依赖环境

| 依赖 | 版本 |
|------|------|
| ROS2 | Jazzy |
| Gazebo | Harmonic (gz-sim) |
| Ubuntu | 24.04 (Noble) |

### 安装依赖

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-ros-gz-bridge
sudo apt install ros-jazzy-robot-state-publisher ros-jazzy-joint-state-publisher
sudo apt install ros-jazzy-rviz2 ros-jazzy-teleop-twist-keyboard
```

🚀 快速开始
1. 构建工作空间
```bash
cd ~/your_ws
colcon build --packages-select fishbot_description
source install/setup.bash
```
2. 启动仿真
```bash
ros2 launch fishbot_description display_robot.launch.py
```
这将启动：

Gazebo Harmonic 仿真器

机器人模型

ROS-Gazebo 桥接节点

RViz2 可视化界面

3. 控制机器人移动
在新终端中运行键盘控制节点：

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
键盘控制按键：

按键	功能
i	前进
, (逗号)	后退
j	左转
l	右转
k	停止
q	加速 +10%
z	减速 -10%
💡 提示：确保运行 teleop_twist_keyboard 的终端窗口处于激活状态（鼠标点击一下），才能接收键盘输入。

4. RViz2 可视化
RViz2 会自动启动并配置好以下显示：

RobotModel（机器人模型）

LaserScan（激光雷达数据）

TF（坐标变换）

如果 RViz2 未自动启动，可手动运行：

```bash
rviz2 -d $(ros2 pkg prefix fishbot_description)/share/fishbot_description/config/display_robot_model.rviz
```
🔧 激光雷达可视化技巧
⚠️ 重要提示：在 Gazebo 中，激光雷达的蓝色射线有时需要手动激活才能正确跟随机器人。这是一个已知的 Gazebo Harmonic 小问题。

激活步骤
启动仿真并等待 Gazebo GUI 完全加载

用键盘控制机器人移动一段距离，确保激光雷达探测到物体（跑出原点雷达探测范围）

在终端中执行以下命令：

```bash
gz model -m fishbot -l laser_link
```
注意：

请将 fishbot 替换为你的机器人模型名称

请将 laser_link 替换为你的激光雷达 link 名称

需要打开 Gazebo 一段时间后执行此命令才有效

这通常取决于你部署的平台算力的多少，在gzsim启动lidar窗口后，可先等待几分钟让gzsim相关组件加载完成

关于启动SLAM建图
```bash
sudo apt update
sudo apt install ros-jazzy-slam-toolbox
```
确保软件包已安装

在前面的launch文件成功启动了gzsim和Rviz2后，在新的终端向执行这句代码
```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=/path/to/your/config/slam_toolbox_params.yaml \
  use_sim_time:=True
```

这将会启动官方的2D SLAM建图软件包
接下来在Rviz2的ADD里面选择By topic,选择/map,然后你就可以看到2D建图了

当你感觉地图已经覆盖了整个环境，就可以保存它了：

```bash
# 保存地图和元数据文件
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "{name: {data: 'my_warehouse'}}"
```
