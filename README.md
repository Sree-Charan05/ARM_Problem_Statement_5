# 🚀 YOLOv5 Nano FPGA Acceleration on ZCU102

## 📌 Project Overview

This project demonstrates a hardware/software co-design implementation of YOLOv5 Nano object detection on the AMD-Xilinx ZCU102 platform.

The convolution backbone of the neural network is offloaded to the DPU (Deep Learning Processor Unit) instantiated in the FPGA fabric (Programmable Logic), while input/output operations and system control run on the ARM Cortex-A53 (Processing System).

This architecture enables real-time object detection with significant acceleration compared to CPU-only execution.

---

# 🏗 System Architecture

<img width="1381" height="804" alt="image" src="https://github.com/user-attachments/assets/97de8dbf-3a69-4c2f-97dd-a47dee5595cc" />


## Architecture Description

### 🔹 Processing System (PS) – ARM Cortex-A53

- Quad-core ARM Cortex-A53 @ 1.2 GHz
- Linux OS
- USB Webcam capture (V4L2)
- Image preprocessing (resize to 640×640)
- VART runtime invocation
- Detection head scaling
- Non-Maximum Suppression (NMS)
- Visualization and display output

All input and output operations are handled in the PS.

---

### 🔹 Programmable Logic (PL) – FPGA Fabric

- DPUCZDX8G (B4096 configuration)
- Executes compiled INT8 `.xmodel`
- Accelerates CNN backbone (4.49 GOP per frame)

The PL performs only computation.  
All control and I/O remain in the PS.

---

# 📊 Performance Results

## 🔹 End-to-End Application Performance (Measured)

| Implementation | FPS | Approximate Latency |
|---------------|------|--------------------|
| CPU Only (ARM A53) | **0.98 FPS** | ~1020 ms |
| PL Accelerated (DPU) | **~24 FPS** | ~41 ms |

### 🔥 Real-World Speedup

24 / 0.98 ≈ **24.5× faster**

Hardware acceleration transforms the system from non-real-time to real-time performance.

---

## 🔹 Raw DPU Hardware Benchmark (Isolated Backbone)

Measured using DPU benchmark utility:

| Metric | Value |
|--------|-------|
| Peak Throughput | **500.46 FPS** |
| Average DPU Latency | **1.99 ms** |
| Operations per Frame | 4.49 GOP |
| Energy Efficiency | 134.5 FPS/W |

> Note: 500 FPS reflects pure CNN backbone execution without webcam and post-processing overhead.

---

# ⚡ Power Analysis

Measured using onboard INA226 sensors.

| State | Power |
|-------|--------|
| Idle Board Power | 10.50 W |
| Active Inference Power | 14.22 W |
| Dynamic DPU Power | 3.72 W |

Energy Efficiency:

500.46 FPS / 3.72 W = **134.5 FPS/W**

This demonstrates strong suitability for edge AI deployment.

---

# 🧠 Model Details

- Model: YOLOv5 Nano
- Dataset: COCO (80 classes)
- Input Resolution: 640 × 640
- Precision: INT8 Quantized
- Target DPU: DPUCZDX8G (B4096)
- Operations per Frame: 4.49 Billion

---

# 🔄 Design Partitioning

| Module | Execution Domain |
|---------|----------------|
| CNN Backbone | FPGA (DPU) |
| Detection Head Scaling | ARM CPU |
| Non-Maximum Suppression | ARM CPU |
| Visualization | ARM CPU |

This partitioning balances computational efficiency and system flexibility.

---

# 📸 Demo Results

## CPU Implementation (~0.98 FPS)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4af78da4-1eea-44ec-95a7-66d32defa313" />


---

## PL Implementation (~24 FPS)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7f850350-cf8e-45fc-bf91-94ff8b6a688a" />


---

# 🖥 How to Run

## 1️⃣ Verify DPU Availability

```bash
xdputil query
