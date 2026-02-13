Detection Model: YOLOv5 Nano 

The core of this project is the YOLOv5 Nano model, the most compact and efficient version of the YOLO (You Only Look Once) family. It is a single-stage object detector designed specifically for edge devices with limited resources. In this implementation, the model is trained on the COCO (Common Objects in Context) dataset, enabling it to identify and localize 80 distinct classes, including:
·	Vehicles: Cars, trucks, buses, motorcycles, and bicycles.
·	People: Pedestrians and crowds in various environments.
·	Animals: Common species such as dogs, cats, birds, and horses.
·	Everyday Items: Cell phones, laptops, chairs, cups, and backpacks.

Hardware Acceleration: The DPU Advantage

Running a complex neural network like YOLOv5 on a standard embedded CPU (ARM Cortex-A53) often results in high latency, typically delivering only 1–2 frames per second (FPS). This project solves the bottleneck by offloading the computational workload to the DPU (Deep Learning Processor Unit) inside the ZCU102’s FPGA fabric. The DPU acts as a dedicated engine for tensor operations, executing billions of mathematical calculations in parallel. This hardware-software co-design allows the system to reach "Real-Time+" speeds, where the hardware capacity far exceeds the standard requirements of human-eye perception.
System Execution: Real-Time Pipeline

The system operates as a continuous real-time pipeline, moving data from the lens to the screen in milliseconds:
1.	Image Acquisition: A frame is captured from a USB webcam.
2.	Preprocessing: The CPU resizes the image to $640 \times 640$ and prepares the data.
3.	Inference: The FPGA-based DPU executes the heavy convolutional math.
4.	Post-processing: The CPU calculates final bounding box coordinates and filters out overlapping detections (NMS).
5.	Visualization: The results are rendered as a live video feed with overlaid bounding boxes and confidence scores.

Primary Performance Outcomes
The final implementation provides a clear distinction between raw hardware capability and end-to-end application speed:
·	Hardware Capacity (Peak): 500.46 FPS. This confirms that the FPGA can process a single frame in approximately 1.99 ms, leaving significant room for multi-camera streams.
·	Real-Time Constraint: While the hardware can run at 500 FPS, the live demonstration is typically synchronized to the webcam’s native frame rate (30 or 60 FPS), ensuring smooth, jitter-free video.
·	Efficiency: The DPU achieves this performance while consuming significantly less power than a high-end GPU, making it ideal for industrial or mobile robotics.

