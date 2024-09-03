import time
import cv2
import os
import json

from Inductive_Proximity_Sensor import Inductive_Proximity # Metal detection function
import Predict_Frame # Your YOLO detection function


def capture_image(camera):
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
            save_path = os.path.join('.', 'User_Session', 'RPI_img.jpg')
            cv2.imwrite(save_path, frame)

            return frame
        
        # If 'q' is pressed, quit without capturing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Capture canceled.")
            cv2.destroyWindow('Live Camera Feed')
            return None
        
def classify_object(image, gpio, model_path):

    # 1. Detect if the object is metal

    # Initialize Proximity sensor
    metal_detector = Inductive_Proximity.InductiveProximitySensor(gpio)
    metal_detector.initialize()
    metal_exists = metal_detector.detect_metal()
    
    if metal_exists:
        print("Metal detected. Object is classified as 'Metal'.")
        return "Metal"
    
    # 2. Run YOLO object detection for non-metallic objects
    detector = Predict_Frame.ObjectDetectionModel(model_path)
    detector.predict(image)

    save_path = os.path.join('.', 'User_Session', 'RPI_Prediction.jpg')
    cv2.putText(image, f"Classification: {detector.Detection}", (10, 30), 
    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    detector.save_image(image,save_path)

    
    return detector.Detection



# def save_session_data(session_data, file_path="session_data.json"):
#     """Saves the session data to a JSON file."""
#     # Read existing data from JSON file
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             data = json.load(f)
#     else:
#         data = []
    
#     # Append the new session data
#     data.append(session_data)
    
#     # Write updated data back to JSON file
#     with open(file_path, 'w') as f:
#         json.dump(data, f, indent=4)


def main_system():
    proximity_sensor_pin = 17  # Initialize your proximity sensor here
    model_path = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset', 'weights', 'best.pt')

    
    while True:

        # 1. Prompt the user to place the object
        input("Get your object ready and press Enter to open the live camera feed...")

        # 2. Initialize the camera
        camera = cv2.VideoCapture(0)
        time.sleep(2)  # Allow the camera to warm up
        
        # 3. Capture a single image
        image = capture_image(camera)
        camera.release()
        if image is None:
            print("No image captured. Exiting...")
            break
        
        # 4. Classify the object
        classification_result = classify_object(image, proximity_sensor_pin, model_path)
        
        # 5. Display the classification result
        print(f"Classification Result: {classification_result}")

        # # 6. Collect session data
        # session_data = {
        #     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        #     "classification_result": classification_result,
        #     "image_path": os.path.join('.', 'User_Session', 'RPI_Prediction.jpg')
        # }
        
        # session_data["objects"].append(object_data)

        # # 7. Save session data to JSON file
        # save_session_data(session_data)
        
        
        # 8. Ask if the user wants to process another object
        continue_processing = input("Do you want to process another object? (y/n): ").lower()
        if continue_processing != 'y':
            break
    
    # Cleanup
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main_system()