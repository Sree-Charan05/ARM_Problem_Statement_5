# Design Partitioning Analysis

## 1. Partitioning Strategy

The YOLOv5 Nano model was compiled for the DPUCZDX8G (B4096) architecture.

Using:

    xdputil xmodel -l yolov5n_int8.xmodel

The model is partitioned into 5 subgraphs.

---

## 2. Subgraph Mapping

### Subgraph 1 – DPU (PL)

- Entire CNN backbone
- 4.49 Billion Operations
- Input: 640×640
- Outputs: Detection feature maps
  - 20×20
  - 40×40
  - 80×80

This subgraph contains all 2D convolutions and batch normalization layers.

---

### Subgraphs 2–4 – CPU (PS)

- Detection head scaling
- Bounding box coordinate decoding
- Class probability adjustments

---

### User-Level CPU Execution

- Initial quantization stub
- Final Non-Maximum Suppression (NMS)

---

## 3. Design Rationale

Why CNN backbone on DPU?

- High arithmetic intensity
- Parallel convolution operations
- Optimal DSP and BRAM utilization

Why NMS on CPU?

- Control-heavy logic
- Irregular memory access
- Lower arithmetic density

---

## 4. Partitioning Trade-Off

At 30 FPS (webcam-limited), CPU overhead is acceptable.

At 500 FPS theoretical throughput, CPU-based NMS becomes a bottleneck.

Future optimization:

- C++ NMS implementation
- Full hardware offloading of detection heads
