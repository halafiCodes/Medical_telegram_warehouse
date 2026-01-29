import os
import pandas as pd
from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO('yolov8n.pt')

def run_detection(image_dir):
    results_list = []
    
    valid_extensions = ('.jpg', '.png', '.jpeg')
    
    for root, _, files in os.walk(image_dir):
        for img_file in files:
            if not img_file.lower().endswith(valid_extensions):
                continue
            img_path = os.path.join(root, img_file)
            
            results = model(img_path)
            
            for r in results:
                classes = r.boxes.cls.tolist()
                confidences = r.boxes.conf.tolist()
                
                has_person = 0 in classes
                has_product = any(c in [39, 41] for c in classes)

                if has_person and has_product:
                    category = 'promotional'
                elif has_product:
                    category = 'product_display'
                elif has_person:
                    category = 'lifestyle'
                else:
                    category = 'other'
                
                if confidences:
                    max_index = confidences.index(max(confidences))
                    class_id = int(classes[max_index])
                    detected_class = model.names.get(class_id, str(class_id))
                else:
                    detected_class = None

                file_stem = os.path.splitext(img_file)[0]
                results_list.append({
                    'image_name': img_file,
                    'message_id': file_stem.split('_')[0],
                    'detected_class': detected_class,
                    'confidence_score': max(confidences) if confidences else 0,
                    'image_category': category
                })
                
    df = pd.DataFrame(results_list)
    df.to_csv('data/yolo_detections.csv', index=False)
    print("Detection complete. Results saved to data/yolo_detections.csv")

run_detection('data/raw/images')
