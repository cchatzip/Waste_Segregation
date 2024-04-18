import os
import cv2
import supervision as sv
from ultralytics import YOLO

model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
image_path = 'C:/Users/Christos/Desktop/datasets/WaDaBa/HDPE/0099_a02b01c1d3e0f1g0h1.jpg'

model = YOLO(model_path)
image = cv2.imread(image_path)
results = model(image)[0]
detections = sv.Detections.from_ultralytics(results)

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

labels = [
    model.model.names[class_id]
    for class_id
    in detections.class_id
]

annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections, labels=labels)

sv.plot_image(annotated_image)