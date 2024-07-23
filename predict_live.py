import os
import cv2
from ultralytics import YOLO
import supervision as sv

# Define the frame width and height for video capture
frame_width = 1280
frame_height = 720

model_path = os.path.join('.', 'runs', 'detect', 'train2_300ep', 'weights', 'best.pt')

def main():
    # Initialize video capture from default camera
    try:
        cap = cv2.VideoCapture(0)
    except:
        print('Camera not valid')

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)


    # Load YOLOv8 model
    model = YOLO(model_path)

    # Initialize bounding box and Label annotator for visualization
    box_annotator = sv.BoundingBoxAnnotator(
        thickness=2,
    )

    label_annotator = sv.LabelAnnotator()

    # Main loop for video processing
    while True:
        # Read frame from video capture
        ret, frame = cap.read()

        # Perform object detection using YOLOv8
        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_ultralytics(result)

        # Prepare labels for detected objects
        labels = [
            model.model.names[class_id]
            for class_id
            in detections.class_id
        ]

        # Annotate frame with bounding boxes and labels
        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
        )

        frame = label_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )


        # Display annotated frame
        cv2.imshow("yolov8", frame)

        # Check for quit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
