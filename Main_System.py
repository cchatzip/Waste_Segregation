import time
import cv2
import os

from Inductive_Proximity_Sensor import Inductive_Proximity # Metal detection function
import Predict_Frame # Your YOLO detection function


def capture_image(camera):
    ret, frame = camera.read()
    if not ret:
        raise Exception("Failed to capture image")
    return frame

def classify_object(image, gpio, model_path):


    # 1. Detect if the object is metal

    # Initialize Proximity sensor
    Inductive_Proximity.initialInductive(gpio)
    metal_detected = Inductive_Proximity.detectMetal()
    
    if metal_detected:
        print("Metal detected. Object is classified as 'Metal'.")
        return "Metal"
    
    # 2. Run YOLO object detection for non-metallic objects
    detector = Predict_Frame.ObjectDetectionModel(model_path)
    detector.predict(image)


    
    return detector.Detection

def main_system():
    camera = cv2.VideoCapture(0)  # Initialize the camera
    proximity_sensor_pin = 17  # Initialize your proximity sensor here
    model_path = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset', 'weights', 'best.pt')

    
    while True:
        # 1. Prompt the user to place the object
        input("Please place the object in the system and press Enter to continue...")
        
        # 2. Capture a single image
        image = capture_image(camera)
        
        # 3. Classify the object
        classification_result = classify_object(image, proximity_sensor_pin, model_path)
        
        # 4. Display the classification result
        print(f"Classification Result: {classification_result}")
        
        # Display the captured image with classification result
        cv2.putText(image, f"Classification: {classification_result}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Captured Image', image)
        
        # 5. Ask if the user wants to process another object
        continue_processing = input("Do you want to process another object? (y/n): ").lower()
        if continue_processing != 'y':
            break
    
    # Cleanup
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main_system()