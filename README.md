# LLM Agent for Drone Control

## Main README.md

### Project Overview
This project focuses on developing a natural language-controlled drone system that minimizes human intervention. The system allows users to command a PX4 drone via natural language prompts, integrating various technologies:

- **Large Language Models (LLMs)** for interpreting user commands.
- **NVIDIA ISAAC SIM** for sensor simulation.
- **Computer Vision** for object detection and depth estimation.
- **MAVLink** for drone communication.
- **PX4-Autopilot** for controlling drone actions.

The system translates natural language instructions into mission commands that enable autonomous drone operation. Users can either define complete missions or utilize a real-time control setup for flexibility.

### System Architecture
The system architecture involves several interconnected components working together:

- **User Input Layer:** Receives natural language commands from the user.
- **LLM Processing Unit:** Interprets and translates commands into actionable tasks.
- **Data Integration Module:** Integrates sensor and vision data into the command processing pipeline.
- **Execution Layer:** Converts processed commands into PX4-compatible instructions and executes them.
- **Feedback Loop:** Collects and processes data from sensors to refine ongoing operations.

![System Architecture](path/to/system_architecture_diagram.png)

Refer to the diagram above for a visual representation of the system.

### Installation
For detailed setup instructions, refer to the [Installation Guide](installation.md).

### Running the Project
Instructions for executing the project are available in the [Directions to Run](directions.md).

### Output and Expected Results
Refer to the [Output and Results](output.md) for details on outputs and expected outcomes.

### Future Work
Enhancements to Minispec code generation, sensor optimization, and real-time control functionalities are planned for future releases.

---

## Installation.md

### Installation Guide

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Dependencies:**
   Ensure Python is installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up PX4 Environment:**
   Follow the official [PX4 setup instructions](https://docs.px4.io/main/en/).

4. **Install NVIDIA ISAAC SIM:**
   Download and configure NVIDIA ISAAC SIM for sensor simulation.

5. **Verify Setup:**
   Confirm all dependencies and software are correctly installed.

---

## Directions.md

### Directions to Run the Project

1. **Initialize the PX4 Simulation Environment:**
   Start the PX4 simulator.

2. **Launch the Drone Control Script:**
   Navigate to the project directory and run:
   ```bash
   python main.py
   ```

3. **Provide Natural Language Commands:**
   Use the interface to input commands (e.g., "survey area" or "capture images of an object").

4. **Analyze Mission Data:**
   Output data will be saved in mission-specific directories within the project folder.

---

## Output.md

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

### Expected Results
- **Depth Data:** Displays accurate depth estimations.
- **Mission Logs:** Visualized using [PX4 Log Analysis Tool](https://logs.px4.io/).
- **Object Detection:** JSON files contain detection details for mission objects.

### Troubleshooting
- Ensure all dependencies are installed correctly.
- Verify the PX4 simulation environment is running.
- Check log files in `logs/` for errors.

---
