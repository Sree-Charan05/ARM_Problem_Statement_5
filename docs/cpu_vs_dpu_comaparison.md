# CPU vs Hardware-Accelerated Comparison

## 1. Real-Time Application Results

| Metric | CPU (PS Only) | DPU (PL Accelerated) |
|--------|---------------|----------------------|
| FPS | 0.98 | ~24 |
| Latency | ~1020 ms | ~41 ms |
| Execution Domain | ARM Cortex-A53 | FPGA DPU |
| CNN Backbone | Software | Hardware |

Speedup:

    ~24.5× faster

---

## 2. Hardware Capability vs Application Throughput

| Category | Value |
|----------|--------|
| Theoretical DPU Throughput | 500.46 FPS |
| Application Throughput | ~24 FPS |
| Webcam Limit | ~30 FPS |

The difference is caused by:

- USB webcam frame rate
- Python preprocessing overhead
- CPU-based detection head
- CPU-based NMS
- Memory transfer overhead

---

## 3. Conclusion

Hardware acceleration transforms the system from non-real-time (0.98 FPS) to real-time (~24 FPS), while the DPU itself is capable of >500 FPS under isolated benchmark conditions.
