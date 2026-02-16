import cv2
import numpy as np
import vart
import xir
import os
import time

ANCHORS = np.array([
    [[10,13], [16,30], [33,23]],    
    [[30,61], [62,45], [59,119]],   
    [[116,90], [156,198], [373,326]] 
], dtype=np.float32)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def draw_precision_hud(img, label, conf, x, y, w, h):
    color = (0, 255, 0)
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2, lineType=cv2.LINE_AA)
    text = f"{label.upper()} {int(conf*100)}%"
    font = cv2.FONT_HERSHEY_DUPLEX
    (t_w, t_h), _ = cv2.getTextSize(text, font, 0.5, 1)
    cv2.rectangle(img, (x, y - t_h - 12), (x + t_w + 10, y), color, -1)
    cv2.putText(img, text, (x + 5, y - 8), font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)

def main(model_path, names_path):
    with open(names_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    graph = xir.Graph.deserialize(model_path)
    subgraph = [s for s in graph.get_root_subgraph().get_children() if s.get_attr("device") == "DPU"][0]
    runner = vart.Runner.create_runner(subgraph, "run")

    try:
        input_tensors = runner.get_input_tensors()
        output_tensors = runner.get_output_tensors()
        in_scale = 2**input_tensors[0].get_attr("fix_point")
        in_h, in_w = input_tensors[0].dims[1], input_tensors[0].dims[2]
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        cv2.namedWindow("ZCU102_FAST", cv2.WINDOW_GUI_NORMAL)

        while True:
            ret, frame = cap.read()
            if not ret: break
            start_time = time.time()
            f_h, f_w = frame.shape[:2]

           
            img_resized = cv2.resize(frame, (in_w, in_h))
            img_quant = (img_resized * (in_scale / 255.0)).astype(np.int8)
            
           
            input_data = [np.expand_dims(img_quant, axis=0)]
            output_data = [np.empty(ot.dims, dtype=np.int8) for ot in output_tensors]
            runner.wait(runner.execute_async(input_data, output_data))
            
            all_boxes, all_confs, all_ids = [], [], []

           
            for i, tensor in enumerate(output_data):
                scale = 2**output_tensors[i].get_attr("fix_point")
                feat = tensor[0].astype(np.float32) / scale
                
                gh, gw = feat.shape[0], feat.shape[1]
                feat = feat.reshape(gh, gw, 3, -1)
                
                
                mask = feat[..., 4] > 0 
                if not np.any(mask): continue
                
               
                candidates = feat[mask]
                grid_coords = np.argwhere(mask) # [N, 3] -> (y, x, anchor_idx)
                
            
                probs = sigmoid(candidates[:, 4:]) 
                obj_conf = probs[:, 0]
                cls_probs = probs[:, 1:]
                
                cls_ids = np.argmax(cls_probs, axis=1)
                final_confs = obj_conf * np.max(cls_probs, axis=1)
                
            
                conf_mask = final_confs > 0.45
                if not np.any(conf_mask): continue
                
            
                stride = in_w // gw
                row = candidates[conf_mask]
                g_idx = grid_coords[conf_mask]
                
            
                cx = (sigmoid(row[:, 0]) * 2.0 - 0.5 + g_idx[:, 1]) * stride
                cy = (sigmoid(row[:, 1]) * 2.0 - 0.5 + g_idx[:, 0]) * stride
                
                anch = ANCHORS[i][g_idx[:, 2]]
                bw = (sigmoid(row[:, 2]) * 2.0)**2 * anch[:, 0]
                bh = (sigmoid(row[:, 3]) * 2.0)**2 * anch[:, 1]
                
            
                l = ((cx - bw/2) * (f_w / in_w)).astype(int)
                t = ((cy - bh/2) * (f_h / in_h)).astype(int)
                w = (bw * (f_w / in_w)).astype(int)
                h = (bh * (f_h / in_h)).astype(int)
                
                all_boxes.extend(np.stack([l, t, w, h], axis=1).tolist())
                all_confs.extend(final_confs[conf_mask].tolist())
                all_ids.extend(cls_ids[conf_mask].tolist())

            
            indices = cv2.dnn.NMSBoxes(all_boxes, all_confs, 0.45, 0.4)
            if len(indices) > 0:
                for idx in indices.flatten():
                    draw_precision_hud(frame, classes[all_ids[idx]], all_confs[idx], *all_boxes[idx])

            fps = 1 / (time.time() - start_time)
            cv2.putText(frame, f"FPS: {fps:.1f}", (20, 30), 0, 0.7, (0, 255, 0), 2)
            cv2.imshow("ZCU102_FAST", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
    finally:
        del runner
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main("yolov5_nano_pt.xmodel", "coco.names")
