from ultralytics import YOLO
import os


model_path = os.path.join(os.path.dirname( __file__ ), '..', 'runs', 'detect', 'final_model_150ep', 'weights', 'best.pt')

# Load the YOLO model (specify the path to your trained weights)
model = YOLO(model_path)

# Print the current working directory
# current_directory = os.getcwd()
# print(f"Current working directory: {current_directory}")

# Run validation on the test dataset (specify your yaml file)
metrics = model.val(data='/home/cchatzip/Desktop/Theses_files/Waste_Segregation/train/config.yaml', split='test', conf=0.5, plots=True)

# The 'metrics' object will contain evaluation results like mAP, precision, recall, etc.
print(metrics)

# You can also save a confusion matrix or other plots as needed.