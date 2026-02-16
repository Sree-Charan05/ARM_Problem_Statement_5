# System Architecture

## 1. Overview

The system follows a heterogeneous System-on-Chip (SoC) architecture based on the AMD-Xilinx Zynq UltraScale+ MPSoC. The design partitions compute-intensive CNN operations to FPGA hardware while retaining control, I/O, and post-processing on the ARM Processing System.

The architecture is divided into:

- Processing System (PS)
- Programmable Logic (PL)
- Shared DDR4 Memory Subsystem

---

## 2. Processing System (PS)

### ARM Cortex-A53 (Quad-core @ 1.2 GHz)

Responsibilities:

- Linux OS execution
- USB Webcam capture (V4L2)
- Image preprocessing (OpenCV resize to 640×640)
- INT8 normalization
- DPU task scheduling (VART API)
- Detection head scaling (Subgraphs 2–4)
- Non-Maximum Suppression (NMS)
- Visualization (Bounding boxes + FPS display)

The PS acts as the system orchestrator.

---

## 3. Programmable Logic (PL)

The PL hosts the compiled INT8 `.xmodel` executed on:

### DPUCZDX8G – B4096 Configuration

- Executes 4.49 GOP per frame
- Average hardware latency: 1.99 ms
- Peak throughput: 500.46 FPS

The DPU reads input tensors from DDR memory and writes feature maps back via high-performance AXI interfaces.

---

## 4. Memory Architecture

- 4GB DDR4 Shared Memory
- Unified memory space accessible by both PS and PL
- AXI4 High-Performance Ports connect DPU to DDR controller

Memory Footprint:

- 9.8 MB Workspace (REG_1)
- 2.1 MB Constants (REG_0)

---

## 5. End-to-End Data Flow

1. USB webcam captures 1920×1080 frame
2. ARM CPU resizes to 640×640 (INT8)
3. Input tensor written to DDR
4. DPU executes CNN backbone (4.49 GOP)
5. Output tensors written back to DDR
6. ARM performs detection head scaling + NMS
7. Bounding boxes rendered to display

---

## 6. Key Architectural Advantage

The heavy convolution backbone runs entirely in hardware, reducing latency from ~500 ms (CPU) to 1.99 ms (DPU).
