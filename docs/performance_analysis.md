# Performance Analysis

## 1. End-to-End Application Performance

Measured during live webcam inference on ZCU102.

| Implementation | FPS | Approx. Latency |
|----------------|------|----------------|
| CPU Only (ARM A53) | 0.98 FPS | ~1020 ms |
| PL Accelerated (DPU) | ~24 FPS | ~41 ms |

Real-world speedup:

    24 / 0.98 ≈ 24.5×

---

## 2. Raw DPU Hardware Benchmark

Measured using multi-threaded benchmark utility.

| Metric | Value |
|--------|-------|
| Total Frames | 30,029 |
| Duration | 60 seconds |
| Peak Throughput | 500.46 FPS |
| Average Latency | 1.99 ms |

This benchmark isolates the CNN backbone without I/O or post-processing.

---

## 3. Computational Workload

- 4,488,286,000 Operations per frame (4.49 GOP)
- INT8 quantized model
- DPUCZDX8G B4096 configuration

---

## 4. Power Measurement

Measured using onboard INA226 sensors.

| State | Power (W) |
|-------|-----------|
| Idle | 10.50 W |
| Active Inference | 14.22 W |
| Dynamic DPU Power | 3.72 W |

Energy Efficiency (hardware benchmark):

    134.5 FPS/W
