from ultralytics import YOLO
import torch
from pathlib import Path

# print(torch.cuda.is_available())

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
dataset_yaml = Path(__file__).parent / '..' / 'data' / '2024-09-30_5-Fold_Cross-val' / 'split_4' / 'split_4_dataset.yaml'


if __name__ == '__main__':
    # Use the model
    model.train(data= dataset_yaml,
                project = "Waste_Segregation", 
                epochs=200,
                batch=8,
                workers=8,
                lr0= 0.01416,
                lrf= 0.01305,
                momentum= 0.91028,
                weight_decay= 0.00056,
                warmup_epochs= 2.31108,
                warmup_momentum= 0.95,
                box= 5.81979,
                cls= 0.66789,
                dfl= 1.94152,
                hsv_h= 0.01538,
                hsv_s= 0.74193,
                hsv_v= 0.27941,
                degrees= 0.0,
                translate= 0.14851,
                scale= 0.27241,
                shear= 0.0,
                perspective= 0.0,
                flipud= 0.0,
                fliplr= 0.35491,
                bgr= 0.0,
                mosaic= 1.0,
                mixup= 0.0,
                copy_paste= 0.0,
                plots=True,
                val=False)  # train the model
    # metrics = model.val()

