import os
import cv2
import supervision as sv
from ultralytics import YOLO

model_path = os.path.join('.', 'runs', 'detect', 'train2_300ep', 'weights', 'best.pt')
image_path = 'C:/Users/Christos/Desktop/hdpe_test3.jpg'

model = YOLO(model_path)
image = cv2.imread(image_path)
results = model(image)[0]
detections = sv.Detections.from_ultralytics(results)

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

labels = [
    f"{model.model.names[class_id]} {confidence:.2f}"
    for class_id, confidence in zip(detections.class_id, detections.confidence)
]

annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections, labels=labels)

#Displaying Class Prediction and confidence score
index=0

for class_id in detections.class_id:
    print(f"Detection: {model.model.names[class_id]}, Confidence: {detections.confidence[index]}")
    index+=1

#Plotting the image
sv.plot_image(annotated_image)