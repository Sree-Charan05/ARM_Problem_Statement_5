# Performance Analysis

All values below are measured results from hardware benchmarking :contentReference[oaicite:1]{index=1}.

---

## 1. Hardware Throughput

| Metric | Value |
|--------|-------|
| Total Frames | 30,029 |
| Duration | 60 seconds |
| Throughput | 500.46 FPS |
| Average Latency | 1.99 ms |

---

## 2. Computational Workload

- 4,488,286,000 Operations per frame (4.49 GOP)
- INT8 Quantized model
- Multi-threaded DPU execution

---

## 3. Resource Utilization (B4096 DPU)

- DSP48 Slices: ~700–800
- BRAM: High utilization
- Workspace: 9.8 MB
- Constants: 2.1 MB

---

## 4. Power Measurement

Measured using onboard TI INA226 sensors.

| State | Power (W) |
|-------|-----------|
| Idle | 10.50 |
| Active Inference | 14.22 |
| Dynamic DPU Power | 3.72 |

---

## 5. Energy Efficiency

Energy Efficiency:

    500.46 FPS / 3.72 W = 134.5 FPS/W

This demonstrates strong edge-AI suitability.
