# Design Partitioning Analysis

## 1. Partition Strategy

The YOLOv5 Nano model was compiled for DPUCZDX8G (B4096).

Using:

    xdputil xmodel -l yolov5n_int8.xmodel

The model is partitioned into 5 subgraphs.

---

## 2. Subgraph Allocation

### Subgraph 1 – Executed on DPU (PL)

- CNN backbone
- 4.49 Billion Operations
- Input: 640×640
- Outputs: 3 detection feature maps (20×20, 40×40, 80×80)

This contains all convolution and batch normalization layers.

---

### Subgraphs 2–4 – Executed on ARM CPU (PS)

- Detection head scaling
- Bounding box decoding
- Class score adjustments

---

### Final Stage – CPU

- Non-Maximum Suppression (NMS)
- Confidence thresholding

---

## 3. Design Rationale

Why backbone on FPGA?

- High arithmetic intensity
- Parallelizable convolution operations
- Efficient DSP and BRAM utilization

Why NMS on CPU?

- Irregular memory access
- Control-dominant operations
- Lower arithmetic density

---

## 4. Impact of Partitioning

At full pipeline level:

- CPU-only: 0.98 FPS
- DPU-accelerated: ~24 FPS

The DPU dramatically reduces convolution latency, enabling real-time inference.
