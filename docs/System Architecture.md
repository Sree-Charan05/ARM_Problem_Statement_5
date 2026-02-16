# System Architecture

## 1. Overview

This project implements YOLOv5 Nano object detection on the AMD-Xilinx ZCU102 platform using a heterogeneous SoC architecture.

The design separates:

- Processing System (PS)
- Programmable Logic (PL)
- Shared DDR4 Memory

The CNN backbone executes on FPGA hardware, while control logic and post-processing execute on the ARM processor.

---

## 2. Processing System (PS)

### ARM Cortex-A53 (Quad-Core @ 1.2 GHz)

Responsibilities:

- Linux OS execution
- USB Webcam input (V4L2 driver)
- Image preprocessing (OpenCV resize to 640×640)
- INT8 normalization
- DPU scheduling via VART API
- Detection head scaling (Subgraphs 2–4)
- Non-Maximum Suppression (NMS)
- Visualization (bounding boxes + FPS overlay)

The PS orchestrates the pipeline and handles all non-convolution logic.

---

## 3. Programmable Logic (PL)

The PL hosts the compiled INT8 `.xmodel` executed by:

### DPUCZDX8G – B4096 Configuration

- Executes CNN backbone
- 4.49 GOP per frame
- 1.99 ms hardware latency
- 500.46 FPS peak throughput (isolated benchmark)

The DPU accesses shared DDR memory via high-performance AXI interfaces.

---

## 4. Memory Architecture

- 4GB DDR4 shared memory
- Accessible by both PS and PL
- Workspace: 9.8 MB
- Constants: 2.1 MB

---

## 5. End-to-End Execution Flow

1. USB webcam captures 1920×1080 frame
2. ARM resizes to 640×640
3. Input tensor written to DDR
4. DPU executes backbone (hardware acceleration)
5. Output tensors returned to DDR
6. ARM performs detection head scaling
7. ARM executes NMS
8. Final frame displayed with bounding boxes

---

## 6. Observed System Performance

- CPU-only execution: 0.98 FPS
- PL accelerated execution: ~24 FPS

The FPGA-based DPU provides ~24.5× speedup in real-time application performance.
