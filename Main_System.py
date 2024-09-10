import time
import cv2
import os
import json
from datetime import datetime

from Inductive_Proximity_Sensor import Inductive_Proximity # Metal detection function
import Predict_Frame # Your YOLO detection function


def capture_image(camera, session_data, obj_num):
    print("Live camera feed is active. Press 'Enter' to capture the image.")
    
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture image. Retrying...")
            continue
        
        # Display the live feed
        cv2.imshow('Live Camera Feed', frame)

        # Wait for the Enter key to be pressed to capture the image
        if cv2.waitKey(1) & 0xFF == ord('\r'):  # '\r' is the Enter key
            print("Image captured.")
            cv2.destroyWindow('Live Camera Feed')  # Close the live feed window

            #Save the image before classifying it
            ImgBefore_save_path = os.path.join(session_data["session_dir"], f'RPI_img{obj_num}.jpg')
            cv2.imwrite(ImgBefore_save_path, frame)

            return frame, ImgBefore_save_path
        
        # If 'q' is pressed, quit without capturing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Capture canceled.")
            cv2.destroyWindow('Live Camera Feed')
            return None
        
def classify_object(image, gpio, model_path, session_data, ImgBefore_path, obj_num):

    # 1. Detect if the object is metal

    # Initialize Proximity sensor
    metal_detector = Inductive_Proximity.InductiveProximitySensor(gpio)
    metal_detector.initialize()
    metal_exists = metal_detector.detect_metal()
    
    if metal_exists:
        print("Metal detected. Object is classified as 'Metal'.")

        #Save the image with a header classifying it as metal
        ImgAfter_path = os.path.join(session_data["session_dir"], f'RPI_Prediction{obj_num}.jpg')
        cv2.putText(image, "Classification: Metal", (10, 30), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(ImgAfter_path, image)

        # Append result to session data
        session_data['objects'].append({
            "type": "Metal",
            "confidence": "N/A",  # Metal detection doesn't provide confidence
            "image_before": ImgBefore_path,
            "image_after": ImgAfter_path
        })

        return "Metal"
    
    # 2. Run YOLO object detection for non-metallic objects
    detector = Predict_Frame.ObjectDetectionModel(model_path)
    detector.predict(image)

    ImgAfter_path = os.path.join(session_data["session_dir"], f'RPI_Prediction{obj_num}.jpg')
    cv2.putText(image, f"Classification: {detector.Detection}", (10, 30), 
    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    detector.save_image(image, ImgAfter_path)

    # Append result to session data
    session_data['objects'].append({
        "type": detector.Detection,
        "confidence": float(detector.Highest_confidence),
        "image_before": ImgBefore_path,
        "image_after": ImgAfter_path
    })

    return detector.Detection



def save_session_data(session_data):
    """Saves the session data to a JSON file."""
    file_path = os.path.join(session_data["session_dir"], "session_data.json")

    try:
        # Write the session data directly as a JSON object to the file
        with open(file_path, 'w') as f:
            json.dump(session_data, f, indent=4)
        print("Session data saved successfully.")
    
    except Exception as e:
        print(f"An error occurred while saving session data: {e}")


def create_session_directory(session_id):
    """Create a unique directory for storing session images."""
    directory = session_id
    path = os.path.join('.', 'User_Session', directory) 
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def main_system():
    proximity_sensor_pin = 17  # Initialize your proximity sensor here
    model_path = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset', 'weights', 'best.pt')

    #Initialize session data
    session_data = {
        "session_id": str(int(time.time())),  # Using timestamp as unique session ID
        "timestamp": datetime.now().isoformat(),
        "session_dir": "",
        "objects": [],
        "analytics": {
            "total_objects": 0,
            "metal_objects": 0,
            "plastic_objects": 0
            }
    }
    
    session_dir = create_session_directory(session_data["session_id"])
    session_data.update({'session_dir': session_dir})

    counter = 1

    
    while True:

        # 1. Prompt the user to place the object
        input("Get your object ready and press Enter to open the live camera feed...")

        # 2. Initialize the camera
        camera = cv2.VideoCapture(0)
        time.sleep(2)  # Allow the camera to warm up
        
        # 3. Capture a single image
        image, ImgBefore_path = capture_image(camera, session_data, counter)
        camera.release()
        if image is None:
            print("No image captured. Exiting...")
            break
        
        # 4. Classify the object
        classification_result = classify_object(image, proximity_sensor_pin, model_path, session_data, ImgBefore_path, counter)
        
        # 5. Display the classification result
        print(f"Classification Result: {classification_result}")

        # 6. Update analytics
        session_data['analytics']['total_objects'] += 1
        if classification_result == "Metal":
            session_data['analytics']['metal_objects'] += 1
        else:
            session_data['analytics']['plastic_objects'] += 1
        
        
        # 8. Ask if the user wants to process another object
        continue_processing = input("Do you want to process another object? (y/n): ").lower()
        if continue_processing != 'y':
            save_session_data(session_data)
            break

        #Increase the counter variable so the images are being saved with a unique name
        counter+=1
    
    # Cleanup
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main_system()