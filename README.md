# LLM Agent for Drone Control
![IsaacSim 4.2.0](https://img.shields.io/badge/IsaacSim-4.2.0-brightgreen.svg)
![PX4-Autopilot 1.14.3](https://img.shields.io/badge/PX4--Autopilot-1.14.3-brightgreen.svg)
![ArduPilot-Copter 4.4](https://img.shields.io/badge/ArduPilot--Copter-4.4.0-brightgreen.svg)

[![IsaacSim](https://img.shields.io/badge/IsaacSim-4.5.0-silver.svg)](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3/whatsnew/3.10.html)
[![Linux platform](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/20.04/)

## Project Overview
This project focuses on developing a natural language-controlled drone system that minimizes human intervention. The system allows users to command a PX4 drone via natural language prompts, integrating various technologies:

- **Large Language Models (LLMs)** for interpreting user commands.
- **NVIDIA ISAAC SIM** for sensor simulation.
- **Computer Vision** for object detection and depth estimation.
- **MAVLink** for drone communication.
- **PX4-Autopilot** for controlling drone actions.

The system translates natural language instructions into mission commands that enable autonomous drone operation. Users can either define complete missions or utilize a real-time control setup for flexibility.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Installation Guide](#Installation-Guide)
- [Directions to Run the Project](#Directions-to-Run-the-Project)
- [Output and Results](#Output-andpresults)
- [Expected Results](#Expected-Results)
- [Troubleshooting](#Troubleshooting)


## System Architecture
The system architecture involves several interconnected components working together:

- **User Input Layer:** Receives natural language commands from the user.
- **LLM Processing Unit:** Interprets and translates commands into actionable tasks.
- **Data Integration Module:** Integrates sensor and vision data into the command processing pipeline.
- **Execution Layer:** Converts processed commands into PX4-compatible instructions and executes them.
- **Feedback Loop:** Collects and processes data from sensors to refine ongoing operations.

<!--# ![System Architecture](path/to/system_architecture_diagram.png)

Refer to the diagram above for a visual representation of the system.-->

<!--### Installation
# For detailed setup instructions, refer to the [Installation Guide](installation.md).

### Running the Project
Instructions for executing the project are available in the [Directions to Run](directions.md).

### Output and Expected Results
Refer to the [Output and Results](output.md) for details on outputs and expected outcomes.

### Future Work
Enhancements to Minispec code generation, sensor optimization, and real-time control functionalities are planned for future releases.-->

---

## Installation Guide

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Bapiggott/IsaacDroneControl.git
   cd IsaacDroneControl
   ```

2. **Install Dependencies:**
   Ensure Python is installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Omniverse Launcher:**
   Download the Omniverse Launcher:
   ```bash
   wget https://install.launcher.omniverse.nvidia.com/installers/omniverse-launcher-linux.AppImage
   chmod +x omniverse-launcher-linux.AppImage
   ./omniverse-launcher-linux.AppImage
   ```

4. **Install ROS 2 Humble:**
   Follow the official [ROS 2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

5. **Install NVIDIA ISAAC SIM:**
   Follow the official [ISAAC SIM Installation Guide](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html).

6. **Update Bash Configuration:**
   Add the following lines to your `~/.bashrc` or `~/.zshrc` file:
   ```bash
   # Isaac Sim root directory
   export ISAACSIM_PATH="${HOME}/.local/share/ov/pkg/isaac_sim-4.2.0"
   # Isaac Sim python executable
   alias ISAACSIM_PYTHON="${ISAACSIM_PATH}/python.sh"
   # Isaac Sim app
   alias ISAACSIM="${ISAACSIM_PATH}/isaac-sim.sh"
   ```
   Reload the shell configuration:
   ```bash
   source ~/.bashrc
   ```

7. **Install Pegasus Simulator:**
   Follow the [Pegasus Simulator Installation Guide](https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html#installing-the-pegasus-simulator).

8. **Install QGroundControl:**
   Download and install [QGroundControl](https://qgroundcontrol.com/).

9. **Verify Setup:**
   Confirm all dependencies and software are correctly installed.


---


## Directions to Run the Project

1. **Start QGroundControl:**
   Make the AppImage executable:
   ```bash
   chmod +x ./QGroundControl.AppImage
   ```
   Execute QGroundControl by running:
   ```bash
   ./QGroundControl.AppImage
   ```

2. **Run IsaacSim Environment with Pegasus:**
   Use the following command to integrate IsaacSim with Pegasus:
   ```bash
   ISAACSIM_PYTHON examples/4_python_single_vehicle.py
   ```

3. **Start System Components:**
   Run the shell command to start the required components:
   ```bash
   ./start_system.sh --components=image_server,ollama_llm_server,ui_prompt --default=all
   ```
   This will:
   - Start the Image Server.
   - Launch the Ollama LLM Server.
   - Initialize the UI for user prompts.

4. **Access the User Interface:**
   Open a web browser and navigate to the specified port (e.g., `http://localhost:8080`) to access the UI 

5. **Provide Natural Language Commands:**
   Use the interface to input commands (e.g., "survey area" or "capture images of an object").

6. **Analyze Mission Data:**
   Output data will be saved in mission-specific directories within the project folder.

---

### Output and Results

The output is organized into mission-specific directories containing:

1. **ULog Files:**
   Raw sensor data collected during the mission, suitable for analysis.

2. **Image Data:**
   Includes:
   - Original images (`original.jpg`)
   - Depth maps (`depth.jpg`)
   - Depth coordinates (`depth_with_coordinates.npy`)

3. **Minispec Code:**
   Translations of natural language commands into Minispec and Python commands for execution.

### Example: Loading Depth Coordinates
```python
import numpy as np

# Load depth data
depth_with_coordinates = np.load("depth_with_coordinates.npy")
print("Data shape:", depth_with_coordinates.shape)
print(depth_with_coordinates)
```

## Expected Results
- **Depth Data:** Displays accurate depth estimations.
- **Mission Logs:** Visualized using [PX4 Log Analysis Tool](https://logs.px4.io/).
- **Object Detection:** JSON files contain detection details for mission objects.

## Troubleshooting
- Ensure all dependencies are installed correctly.
- Verify the PX4 simulation environment is running.
- Check log files in `logs/` for errors.

---
