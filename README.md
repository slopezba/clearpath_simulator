# Clearpath Simulator

This package provides simulation for Clearpath robots (e.g., **Husky A200 with UR5e arm and gripper**) in **ROS 2 Humble** using **Gazebo (Ignition Fortress)** and **MoveIt 2**.  

---

## 📦 Setup

### Prerequisites
- Install [ROS 2 Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

### Install Ignition Fortress

```bash
sudo apt-get update && sudo apt-get install wget
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update && sudo apt-get install ignition-fortress
```

### Workspace

```bash
mkdir -p ~/clearpath_ws/src
cd ~/clearpath_ws/src
git clone https://github.com/clearpathrobotics/clearpath_simulator.git
cd ~/clearpath_ws
rosdep install -r --from-paths src -i -y
colcon build --symlink-install
```

### Setup Path

The simulator generates configuration files based on the `clearpath` folder.  
This folder **must** be placed inside your **HOME directory** (`~/clearpath`).  

If it is not there, move it with:

```bash
mv clearpath ~/clearpath
```

Copy your `robot.yaml` into `~/clearpath`.

---

## 🚀 Launch Simulation

Run the main simulation with RViz enabled:

```bash
ros2 launch clearpath_gz simulation.launch.py rviz:=true
```

This will:

- Start Gazebo (Fortress) with the Clearpath robot.
- Launch `ros_gz_bridge` to connect Gazebo topics with ROS 2.
- Spawn controllers for both the base and manipulator.
- Open RViz2 for visualization.

---

## 🤖 Controllers

### 1. Base Velocity Controller

The robot base is controlled through the `platform_velocity_controller`, which listens on `/a200_0000/cmd_vel`.

Example (move forward at 0.3 m/s):

```bash
ros2 topic pub /a200_0000/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.3}, angular: {z: 0.0}}" -r 10
```

### 2. Arm Velocity Controller

The UR5e arm has a velocity controller interface available at:

```
/a200_0000/arm_0_velocity_controller/commands
```

Example (move elbow joint at -0.2 rad/s):

```bash
ros2 topic pub /a200_0000/arm_0_velocity_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, -0.2, 0.0, 0.0, 0.0]}"
```

### 3. Gripper Controller

The gripper is managed by a `GripperActionController`.  
By default, it is loaded as:

```
/a200_0000/arm_0_gripper_controller
```

---

## 📋 Notes

- Always ensure `~/clearpath/robot.yaml` defines your platform, arm, and gripper configuration.  
- The generated configs (URDF, SRDF, controllers) are created automatically when the simulator is launched.  
- If you want to add velocity controllers or modify limits, update the YAML configuration accordingly.  

---

## ✅ Summary

With this setup, you can:

- Simulate Clearpath robots in **Gazebo Fortress**.  
- Control the base with `/cmd_vel`.  
- Control the UR5e arm with **velocity or trajectory controllers**.  
- Operate the gripper through its **dedicated action controller**.  
