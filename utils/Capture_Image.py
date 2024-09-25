import cv2
import time
import os


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
            Img_save_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Background.jpg')
            cv2.imwrite(Img_save_path, frame) #Save the image before classification

            return None
        
        # If 'q' is pressed, quit without capturing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Capture canceled.")
            cv2.destroyWindow('Live Camera Feed')
            return None

#Test module
if __name__ == "__main__":

    #Initialize the camera
    camera = cv2.VideoCapture(0)
    time.sleep(2)  # Allow the camera to warm up

    capture_image(camera)

    # Cleanup
    camera.release()
    cv2.destroyAllWindows()