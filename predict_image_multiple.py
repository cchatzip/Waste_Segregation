"""
The following script was created to make predictions on multiple images inside a folder and save them.

PREREQUISITES:
-A folder named Test_Images inside the main project folder
-A folder named Predictions where Images with detections will be saved with the exact same name as the original image.

"""


import os
import cv2
import supervision as sv
from ultralytics import YOLO

model_path = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset', 'weights', 'best.pt')
images_path = os.path.join('.', 'Test_Images')


items = os.listdir(images_path)



for i in range(len(items)):

    test_img = items[i]
    TestImg_path = os.path.join(images_path, test_img)

    model = YOLO(model_path)
    image = cv2.imread(TestImg_path)
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
    # sv.plot_image(annotated_image)


    # Save the image
    Saving_path = os.path.join('.', 'Predictions', test_img)

    cv2.imwrite(Saving_path, annotated_image) 





