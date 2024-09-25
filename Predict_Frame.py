import os
import cv2
import supervision as sv
from ultralytics import YOLO

class ObjectDetectionModel:
    def __init__(self, model_path, confidence_threshold=0.5):
        self.model = YOLO(model_path)
        self.bounding_box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.Detection = 'Unknown'
        self.Highest_confidence = 0
        self.confidence_threshold = confidence_threshold  # Confidence threshold for YOLO predictions

    def predict_class(self, image):
        # Use the 'conf' parameter to set the confidence threshold
        results = self.model.predict(image, conf=self.confidence_threshold)[0] #predict function provided by yolo is used
        detections = sv.Detections.from_ultralytics(results)

        if detections.class_id.size == 0:
            print('No detections with sufficient confidence were found.')
            return image  # Return the original image if no detections pass the threshold

        #Extract class names and confidence scores
        labels = [
            f"{self.model.model.names[class_id]} {confidence:.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence)
        ]

        annotated_image = self.bounding_box_annotator.annotate(
            scene=image, detections=detections)
        annotated_image = self.label_annotator.annotate(
            scene=annotated_image, detections=detections, labels=labels)

        # Displaying Class Prediction and confidence score
        for index, class_id in enumerate(detections.class_id):
            print(f"Detection: {self.model.model.names[class_id]}, Confidence: {detections.confidence[index]}")

            # Update the highest confidence detection
            if detections.confidence[index] > self.Highest_confidence:
                self.Highest_confidence = detections.confidence[index]
                self.Detection = self.model.model.names[class_id]

        return annotated_image

    def save_image(self, image, output_path):
        cv2.imwrite(output_path, image)

    def show_image(self, image):
        sv.plot_image(image)


# Example usage in the main script
if __name__ == '__main__':
    model_path = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset', 'weights', 'best.pt')
    confidence_threshold = 0.6  # Set your desired confidence threshold here
    detector = ObjectDetectionModel(model_path, confidence_threshold)

    # Replace this with the frame you capture from the camera
    image_path = os.path.join('.', 'Test_Images', 'Black_Background.png')
    image = cv2.imread(image_path)

    annotated_image = detector.predict(image)
    detector.show_image(annotated_image)

    # Optional: Save the annotated image
    # detector.save_image(annotated_image, 'annotated_image.jpg')