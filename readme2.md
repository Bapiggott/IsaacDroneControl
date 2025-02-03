# LLM Agent for Drone Control

[![PX4-Autopilot 1.14.3](https://img.shields.io/badge/PX4-Autopilot--1.14.3-green.svg)](https://docs.px4.io/main/en/releases/1.14.html)
[![IsaacSim](https://img.shields.io/badge/IsaacSim-4.5.0-silver.svg)](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)
[![Ros2](https://img.shields.io/badge/Ros2-Humble-violet.svg)](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
[![QGroundControl](https://img.shields.io/badge/QGroundControl-v4.4.3-yellow.svg)](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/quick_start.html)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3/whatsnew/3.10.html)
[![Linux platform](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/22.04/)

---

## 📜 Table of Contents

1. [🌟 Project Overview](#-project-overview)
2. [📐 System Architecture](#-system-architecture)
3. [🛠️ Installation Guide](#%EF%B8%8F-installation-guide)
4. [🚀 Directions to Run the Project](#-directions-to-run-the-project)
5. [🎯 Expected Results](#-expected-results)
6. [🔍 Troubleshooting](#-troubleshooting)
7. [🎥 Demo Video](#-demo-video)
8. [👨‍💻 Contributors](#-contributors)
9. [📜 License](#-license)

---

## 🌟 Project Overview

This project focuses on developing a natural language-controlled drone system that minimizes human intervention. The system allows users to command a PX4 drone via natural language prompts, integrating cutting-edge technologies:

- 🚀 **Large Language Models (LLMs)** for interpreting user commands.
- 🎮 **NVIDIA ISAAC SIM** for sensor simulation.
- 🖼️ **Computer Vision** for object detection and depth estimation.
- 🔗 **MAVLink** for drone communication.
- ✈️ **PX4-Autopilot** for controlling drone actions.

The system translates natural language instructions into mission commands that enable autonomous drone operation, offering flexibility and scalability for real-world applications.

![System Demo GIF](https://via.placeholder.com/800x400.gif?text=Demo+of+Drone+Control)

---

## 📐 System Architecture

The system architecture involves several interconnected components working seamlessly together:

![System Architecture Diagram](https://via.placeholder.com/1200x600.png?text=System+Architecture+Diagram)

- **User Input Layer:** Receives natural language commands from the user.
- **LLM Processing Unit:** Interprets and translates commands into actionable tasks.
- **Data Integration Module:** Integrates sensor and vision data into the command processing pipeline.
- **Execution Layer:** Converts processed commands into PX4-compatible instructions and executes them.
- **Feedback Loop:** Collects and processes data from sensors to refine ongoing operations.

---

## 🛠️ Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Bapiggott/IsaacDroneControl.git
cd IsaacDroneControl
```

### 2. Install Dependencies
Ensure Python is installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Install Omniverse Launcher
Download the Omniverse Launcher:
```bash
wget https://install.launcher.omniverse.nvidia.com/installers/omniverse-launcher-linux.AppImage
chmod +x omniverse-launcher-linux.AppImage
./omniverse-launcher-linux.AppImage
```

### 4. Install ROS 2 Humble
Follow the official [ROS 2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

### 5. Install NVIDIA ISAAC SIM
Follow the official [ISAAC SIM Installation Guide](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html).

### 6. Install Pegasus Simulator
Follow the [Pegasus Simulator Installation Guide](https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html#installing-the-pegasus-simulator).

### 7. Verify Setup
Confirm all dependencies and software are correctly installed.

---
## 🚀 Directions to Run the Project

### Command-Line Arguments

The system can be run with the following options to control specific components:

- `--llm_model_name` or `-l`: Name of the language model (default: `deepseek-r1:8b`).
- `--vlm_model_name` or `-v`: Name of the vision model (default: `llama3.2-vision`).
- `----interface_port` or `-p`: Port on which the web interface runs (default: `http://localhost:5000`).
- `--vlm_api_url` or `-va`: API endpoint for the VLM (default: `http://localhost:8889`).
- `--llm_api_url` or `-la`: API endpoint for the Ollama LLM (default: `http://localhost:8888`).
- `--components` or `-c`: Choose which components to start (`qgroundcontrol`, `ollama`, `image_server`, or `all` as default).

### Example Commands

#### Run IsaacSim Environment with Pegasus
Before starting the main components, ensure the Isaac Sim world is running:
```bash
ISAACSIM_PYTHON isaac_sim_world.py
```

#### Start All Components
```bash
python3 start_system.py --components=all
```

or

```bash
python3 start_system.py -c all
```

#### Start Specific Components
To start only specific components like QGroundControl and the Image Server:
```bash
python3 start_system.py --components=qgroundcontrol,image_server
```

or

```bash
python3 start_system.py -c qgroundcontrol,image_server
```

### Access the User Interface
Once started, navigate to `http://localhost:5000` in your browser to interact with the system.

### Provide Natural Language Commands
Use the interface to input commands like "survey area" or "capture images of an object."

### Analyze Mission Data
Output data is saved in mission-specific directories within the project folder.
---

## 🎯 Expected Results

- **Depth Data:** Displays accurate depth estimations.
- **Mission Logs:** Visualized using [PX4 Log Analysis Tool](https://logs.px4.io/).
- **Object Detection:** JSON files contain detection details for mission objects.

---

## 🔍 Troubleshooting

- Verify all dependencies are installed correctly.
- Ensure the PX4 simulation environment is running.
- Check log files in `logs/` for errors.

---

## 🎥 Demo Video

[![Watch the Demo](https://via.placeholder.com/800x400.png?text=Click+to+Watch+Demo)](https://example.com/demo)

---

## 👨‍💻 Contributors

- **Brett Piggott** - [GitHub](https://github.com/Bapiggott)
- **The rest of our team...**

---

## 📜 License

This project is licensed under...
<!--the MIT License. See the LICENSE file for details.

![Footer Image](https://via.placeholder.com/1200x200.png?text=Thank+You+for+Visiting)-->
