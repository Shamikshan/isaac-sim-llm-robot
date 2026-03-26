# LLM-Powered Robot Manipulation Pipeline

An end-to-end pipeline that uses a Large Language Model (Qwen) to control a Franka Panda robot arm in Isaac Sim through natural language commands.

## Architecture
```
Natural Language Command
        ↓
ROS2 LLM Client Node
        ↓
Qwen LLM (Google Colab + Cloudflare Tunnel)
        ↓
JSON Action {"action": "pick", "target_position": [x, y, z]}
        ↓
MoveIt2 (OMPL Motion Planning + Inverse Kinematics)
        ↓
Isaac Bridge Node
        ↓
Isaac Sim (Franka Panda) + RViz (synchronized)
```

## Tech Stack

- **Robot Simulator:** NVIDIA Isaac Sim
- **Motion Planning:** MoveIt2 (OMPL planner)
- **Middleware:** ROS2 Jazzy
- **LLM:** Qwen2.5-1.5B-Instruct
- **LLM Server:** FastAPI + Cloudflare Tunnel on Google Colab
- **Robot:** Franka Panda 7-DOF arm

## Setup

### Prerequisites
- Ubuntu 24.04
- ROS2 Jazzy
- NVIDIA Isaac Sim
- MoveIt2
- Google Colab account

### Installation
```bash
cd ~/ros2_ws/src
git clone https://github.com/Shamikshan/isaac-sim-llm-robot.git llm_robot_bridge
cd ~/ros2_ws
colcon build --packages-select llm_robot_bridge
source install/setup.bash
```

### Running the Pipeline

**Terminal 1 — MoveIt2 + RViz:**
```bash
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

**Terminal 2 — MoveIt2 Executor:**
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch llm_robot_bridge moveit_executor.launch.py
```

**Terminal 3 — Isaac Sim Bridge:**
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run llm_robot_bridge isaac_bridge_node
```

**Terminal 4 — LLM Client:**
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run llm_robot_bridge llm_client_node
```

**Terminal 5 — Send a command:**
```bash
ros2 topic pub --once /scene_description std_msgs/msg/String \
  "data: 'Scene: red cube at position (0.4, 0.1, 0.4). Task: pick up the red cube.'"
```

## Project Structure
```
llm_robot_bridge/
├── config/
│   └── moveit_cpp.yaml          # MoveIt2 planning configuration
├── launch/
│   └── moveit_executor.launch.py # Launch file for executor node
├── llm_robot_bridge/
│   ├── llm_client_node.py       # Sends scene to LLM, publishes action
│   ├── moveit_executor_node.py  # Plans and executes trajectory
│   └── isaac_bridge_node.py     # Bridges MoveIt2 to Isaac Sim
└── README.md
```

## Roadmap

- [ ] Add camera perception in Isaac Sim
- [ ] Natural language commands without coordinates
- [ ] Multi-step task planning
- [ ] Vision-Language-Action (VLA) model integration

## Author

Shamikshan — B.Tech Robotics and Automation
