import streamlit as st
import cv2
import os
import time
import json
from datetime import datetime
from Inductive_Proximity_Sensor import Inductive_Proximity
from utils import Image_Modification
import Predict_Frame

def create_session_directory(session_id):
    """Create a unique directory for storing session images if not already created."""

    directory = session_id
    path = os.path.join('.', 'User_Session', directory) 
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def initialize_session_data():
    """Initialize session data."""
    return {
        "session_id": str(int(time.time())),
        "timestamp": datetime.now().isoformat(),
        "session_dir": "",
        "objects": [],
        "analytics": {
            "total_objects": 0,
            "metal_objects": 0,
            "plastic_objects": 0
        }
    }

def save_session_data(session_data):
    """Save the session data to a JSON file."""
    file_path = os.path.join(session_data["session_dir"], "session_data.json")
    with open(file_path, 'w') as f:
        json.dump(session_data, f, indent=4)


def capture_image(camera, session_data, obj_num):

    ImgBefore_save_path = os.path.join(session_data["session_dir"], f'RPI_img{obj_num}.jpg')

    # Create a placeholder for the image and the buttons
    # Initialize the placeholders in session_state if not already
    if 'image_placeholder' not in st.session_state:
        st.session_state['image_placeholder'] = st.empty()
    if 'buttons_placeholder' not in st.session_state:
        st.session_state['buttons_placeholder'] = st.empty()

    # Initialize the session state for capturing or canceling
    if f"image_captured_{obj_num}" not in st.session_state:
        st.session_state[f"image_captured_{obj_num}"] = False
    if f"capture_cancelled_{obj_num}" not in st.session_state:
        st.session_state[f"capture_cancelled_{obj_num}"] = False

    with st.session_state['buttons_placeholder']:
        # Display the buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Make Prediction", key=f"make_prediction_{obj_num}"):
                st.session_state[f"image_captured_{obj_num}"] = True  # Update state on capture

        with col2:
            if st.button("Cancel Session", key=f"cancel_session_{obj_num}"):
                st.session_state[f"capture_cancelled_{obj_num}"] = True  # Update state on cancel

    frame = None  # Initialize frame

    # Continuously update the image feed
    while not st.session_state[f"image_captured_{obj_num}"] and not st.session_state[f"capture_cancelled_{obj_num}"]:

        ret, frame = camera.read()
        if not ret:
            st.error("Failed to capture image")
            time.sleep(1)  # Delay before retrying
            break  # Exit the loop if frame capture fails

        # Update the image in the placeholder
        st.session_state['image_placeholder'].image(frame, channels="BGR", use_column_width=True)
        st.session_state[f"last_frame_{obj_num}"] = frame  # Save the last frame using Streamlit session_state

        time.sleep(0.1)  # Avoid high CPU usage by adding a small delay

    # Check if the capture button was pressed
    if st.session_state[f"image_captured_{obj_num}"]:
        # Save the image
        try:
            cv2.imwrite(ImgBefore_save_path, st.session_state[f"last_frame_{obj_num}"])
        except Exception as e:
            st.sidebar.error("Could not save image: " + str(e))


    camera.release()  # Release camera when done

    if st.session_state[f"capture_cancelled_{obj_num}"]:
        st.warning("Session canceled.")

        #Empty the placeholders
        st.session_state['image_placeholder'].empty()
        st.session_state['buttons_placeholder'].empty()
        return None, None  # Indicate cancellation
    
    #Empty the placeholders
    st.session_state['image_placeholder'].empty()
    st.session_state['buttons_placeholder'].empty()

    return st.session_state[f"last_frame_{obj_num}"], ImgBefore_save_path  # Return the captured frame and path


def image_preprocessing(unprocessed_img_path, session_data, obj_num):
    """Preprocess the image for object classification."""
    background_image_path = os.path.join(os.path.dirname(__file__), 'Background_modification', 'Background.jpg')
    
    extracted_result = Image_Modification.remove_background(unprocessed_img_path, background_image_path)
    extracted_image_path = os.path.join(os.path.dirname(__file__), 'Background_modification', 'Extracted_object', 'extracted_result.png')
    
    # Save the extracted image
    cv2.imwrite(extracted_image_path, extracted_result)

    new_background_path = os.path.join(os.path.dirname(__file__), 'Background_modification', 'Black_background.jpg')
    img_modified = Image_Modification.place_on_new_background(extracted_image_path, new_background_path)
    img_modified_path = os.path.join(session_data["session_dir"], f'RPI_ImgModified{obj_num}.jpg')
    img_modified.save(img_modified_path)

    return img_modified_path

def classify_object(gpio, model_path, session_data, ImgBefore_path, obj_num):
    
    #Load the modified image
    image = cv2.imread(ImgBefore_path)

    # 1. Detect if the object is metal

    # Initialize Proximity sensor
    metal_detector = Inductive_Proximity.InductiveProximitySensor(gpio)
    metal_detector.initialize()
    metal_exists = metal_detector.detect_metal()
    
    if metal_exists:
        st.write("Metal detected. Object is classified as 'Metal'.")

        #Save the image with a header classifying it as metal
        ImgAfter_path = os.path.join(session_data["session_dir"], f'RPI_Prediction{obj_num}.jpg')
        cv2.putText(image, "Classification: Metal", (10, 30), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(ImgAfter_path, image) #Save image after classification

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
    detector.predict_class(image)

    ImgAfter_path = os.path.join(session_data["session_dir"], f'RPI_Prediction{obj_num}.jpg')
    cv2.putText(image, f"Classification: {detector.Detection}", (10, 30), 
    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    detector.save_image(image, ImgAfter_path) #Save the image after classification

    # Append result to session data
    session_data['objects'].append({
        "type": detector.Detection,
        "confidence": float(detector.Highest_confidence),
        "image_before": ImgBefore_path,
        "image_after": ImgAfter_path
    })

    return detector.Detection



def main_system():

    """Main function of the recycling system."""
    
    if not st.session_state.system_initialized:
        st.session_state.proximity_sensor_pin = 17
        st.session_state.model_path = os.path.join('.', 'runs', 'detect', 'final_model_150ep', 'weights', 'best.pt')

        st.session_state.session_data = initialize_session_data()
        st.session_state.session_dir = create_session_directory(st.session_state.session_data["session_id"])
        st.session_state.session_data['session_dir'] = st.session_state.session_dir
        st.session_state.system_initialized = True
    
    camera = cv2.VideoCapture(0)
    time.sleep(2)  # Allow the camera to warm up
        
    #The counter is used to keep track of the objects entered the system and save the images appropriately
    if "counter" not in st.session_state: 
        st.session_state.counter = 1


    if st.session_state.session_active:

        image, CapturedImg_path = capture_image(camera, st.session_state.session_data, st.session_state.counter)
        camera.release()

        if image is None:
            st.write("No image captured. Exiting...")
            st.session_state.session_active = False
            camera.release()
            cv2.destroyAllWindows()
            return

        # Preprocess image
        ProcessedImg_path = image_preprocessing(CapturedImg_path, st.session_state.session_data, st.session_state.counter)

        # Classify object
        classification_result = classify_object(st.session_state.proximity_sensor_pin, st.session_state.model_path, st.session_state.session_data, ProcessedImg_path, st.session_state.counter)
        st.write(f"Classification Result: {classification_result}")

        # Update analytics
        st.session_state.session_data['analytics']['total_objects'] += 1
        if classification_result == "Metal":
            st.session_state.session_data['analytics']['metal_objects'] += 1
        else:
            st.session_state.session_data['analytics']['plastic_objects'] += 1


        # Display the before and after classification images to user
        results = st.empty()

        # Check if there are any objects in session data
        if st.session_state.session_data["objects"]:
            # Get the last object processed
            last_obj = st.session_state.session_data["objects"][-1]  # Access the last object directly


            with results.container():

                # Display the last object's details and images
                st.write(f"Session ID: {st.session_state.session_data['session_id']}")
                st.write(f"Object {st.session_state.counter}:")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.image(last_obj['image_before'], caption="Before Classification", use_column_width=True)
                
                with col2:
                    st.image(last_obj['image_after'], caption="After Classification", use_column_width=True)
                
                st.write(f"Type: {last_obj['type']}")
                st.write(f"Confidence: {last_obj['confidence']}")
                
        # Update counter and session active state
        st.session_state.counter += 1 
        st.session_state.session_active = False


    # Display the buttons
    buttons_placeholder2 = st.empty()

    with buttons_placeholder2.container():

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Process Another Object"):
                st.session_state.session_active = True
                buttons_placeholder2.empty()
                camera.release()
                cv2.destroyAllWindows()
                main_system()

        with col2:
            if st.button("Finish Session"):
                save_session_data(st.session_state.session_data)
                st.session_state.session_active = False  # Mark session as no longer active
                st.session_state.session_complete = True  # Mark the session as complete
                buttons_placeholder2.empty()
                camera.release()
                cv2.destroyAllWindows()

if __name__ == "__main__":
    main_system()