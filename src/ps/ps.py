import torch
import cv2
import numpy as np
import time

def main():

 
    print("Loading YOLOv5n weights to ARM CPU...")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True, force_reload=False)
    model.cpu()  # Ensure it is on the PS (CPU)
    model.eval() # Set to inference mode
    
  
    classes = model.names if hasattr(model, 'names') else [f"ID:{i}" for i in range(80)]

   
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Inference started on PS. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        start_time = time.time()
        
      
       
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img, (640, 640))
        img_tensor = torch.from_numpy(img_resized).permute(2, 0, 1).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0)

 
        with torch.no_grad():
            results = model(img_tensor)
        
  
   
        predictions = results[0]
        
    
        conf_thres = 0.4
        mask = predictions[..., 4] > conf_thres
        detections = predictions[mask]

        if detections.shape[0] > 0:
            for det in detections:
                # Coordinate scaling back to frame size
                cx, cy, w, h, conf = det[:5]
                # Get class with highest probability
                cls_id = torch.argmax(det[5:]).item()
                
     
                x1 = int((cx - w/2) * frame.shape[1] / 640)
                y1 = int((cy - h/2) * frame.shape[0] / 640)
                bw = int(w * frame.shape[1] / 640)
                bh = int(h * frame.shape[0] / 640)

      
                cv2.rectangle(frame, (x1, y1), (x1 + bw, y1 + bh), (0, 255, 0), 2)
                label = f"{classes[cls_id]} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

       
        fps = 1 / (time.time() - start_time)
        cv2.putText(frame, f"PS-CPU FPS: {fps:.2f}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        
        cv2.imshow("Pure_Python_No_Pandas", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
