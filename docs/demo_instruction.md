# Demo Instructions

## 1. Hardware Setup

- ZCU102 board
- SD card with PetaLinux image
- USB webcam
- HDMI display

---

## 2. Boot Board

1. Insert SD card
2. Power ON board
3. Login via serial console or SSH

---

## 3. Verify DPU

Run:

    xdputil query

Confirm DPUCZDX8G is detected.

---

## 4. Run CPU-Only Implementation

    python3 yolov5n_cpu_only.py

Expected Result:

- ~0.98 FPS
- ~1 second latency per frame
- Bounding boxes displayed slowly

---

## 5. Run PL-Accelerated Implementation

    python3 yolov5n_dpu_webcam.py

Expected Result:

- ~23.8–24 FPS
- Smooth real-time video
- Bounding boxes and confidence overlay

---

## 6. Raw Hardware Benchmark

To measure isolated DPU throughput:

    ./benchmark_model yolov5n_int8.xmodel

Expected:

- 500.46 FPS
- 1.99 ms latency
