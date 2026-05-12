# ROS 2 Prosthetic HMI: Hardware-in-the-Loop Digital Twin

### **Project Overview**
This repository contains a ROS 2 Jazzy implementation of a tactile Human-Machine Interface (HMI) designed to control a 6-DOF prosthetic leg. By bridging legacy analog hardware with modern robotic simulation, this project translates voltage gradients from a vintage 4-axis gimbal into real-time joint state telemetry for a digital twin.

---

### **The Physics: Analog-to-Digital Mapping**
The core logic utilizes a **Linear Interpolation (LERP)** algorithm to map 10-bit raw ADC values to the biomechanical constraints defined in the URDF:

$$\theta = OutMin + \frac{(RawAdc - InMin) \times (OutMax - OutMin)}{InMax - InMin}$$

* **Input Range:** 0 - 1023 (Raw ADC units) via the MCP3008.
* **Output Range:** Radians (Joint position limits).
* **Calibration:** A software-level offset was established to account for a **1.0V electrical center**, ensuring a neutral "standing" posture when the joystick is at rest.

---

### **System Architecture**
![Circuit Diagram](CircuitDiagramROS2LEG.png)

* **Hardware:** Raspberry Pi 5, MCP3008 ADC, and a 4-Axis Analog Gimbal (250kΩ Potentiometers).
* **Communication:** SPI Bus clocked at 1.35 MHz for high-frequency control loops.
* **Simulation Environment:** RViz2 for 3D visualization and Gazebo Harmonic for physics-based simulation.

---

### **Prerequisites**
To run the full hardware-in-the-loop (HIL) demo, the following environment is required:
* **OS:** Ubuntu 24.04 (Noble Numbat)
* **ROS 2 Distro:** Jazzy Jalisco
* **Python Dependencies:** `spidev`, `rclpy`, `sensor_msgs`

---

### **How to Run**

#### **1. Simulation Mode (Mouse/Slider Control)**
To test the URDF and visualization without hardware:
`ros2 launch prosthetic_leg display.launch.py`

#### **2. HIL Mode (Joystick Control)**
To bridge the physical gimbal to the digital twin:

*(Note: Close the GUI slider window after it opens to avoid topic contention.)*
Terminal 1: Launch Visualizer
`ros2 launch prosthetic_leg display.launch.py`
Terminal 2: Execute hardware bridge:
`python3 joystick_bridge.py`
