import os
import cv2
import supervision as sv
from ultralytics import YOLO

class ObjectDetectionModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.bounding_box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.Detection = 'Unknown'

    def predict(self, image):
        results = self.model(image)[0]
        detections = sv.Detections.from_ultralytics(results)
        
        labels = [
            f"{self.model.model.names[class_id]} {confidence:.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence)
        ]

        annotated_image = self.bounding_box_annotator.annotate(
            scene=image, detections=detections)
        annotated_image = self.label_annotator.annotate(
            scene=annotated_image, detections=detections, labels=labels)
        

        #TO BE EDITED
        if detections.class_id.size == 0:
            print('No detections were found.')
            return annotated_image
            

        
        # Displaying Class Prediction and confidence score
        for index, class_id in enumerate(detections.class_id):
            Highest_confidence = detections.confidence[0]
            self.Detection = self.model.model.names[0]
            print(f"Detection: {self.model.model.names[class_id]}, Confidence: {detections.confidence[index]}")
            if detections.confidence[index] > Highest_confidence:
                Highest_confidence = detections.confidence[index]
                self.Detection = self.model.model.names[class_id]
        
        return annotated_image

    def save_image(self, image, output_path):
        cv2.imwrite(output_path, image)

    def show_image(self, image):
        sv.plot_image(image)

# Example usage in the main script
if __name__ == '__main__':
    model_path = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset', 'weights', 'best.pt')
    detector = ObjectDetectionModel(model_path)

    # Replace this with the frame you capture from the camera
    image_path = os.path.join('.', 'Test_Images', 'Black_Background.png')
    image = cv2.imread(image_path)
    
    annotated_image = detector.predict(image)
    detector.show_image(annotated_image)

    # Optional: Save the annotated image
    # detector.save_image(annotated_image, 'annotated_image.jpg')