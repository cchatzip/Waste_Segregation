from ultralytics import YOLO
import torch

# print(torch.cuda.is_available())

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

if __name__ == '__main__':
    # Use the model
    model.train(data="config.yaml", epochs=300, patience=10)  # train the model
    metrics = model.val()

