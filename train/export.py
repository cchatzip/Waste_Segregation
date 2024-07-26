from ultralytics import YOLO
model_path = 'C:/Users/Christos/Desktop/python/ODyolo/runs/detect/train/weights/best.pt'
# Load the YOLOv8 model
model = YOLO(model_path)

# Export the model to TFLite format
results=model.export(format='tflite') # creates 'yolov8n_float32.tflite'