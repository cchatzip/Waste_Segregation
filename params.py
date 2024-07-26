import os

# ML Model config
MODEL_DIR = os.path.join('.', 'runs', 'detect', 'train2_300ep', 'weights')
DETECTION_MODEL = os.path.join(MODEL_DIR, 'best.pt')

# Sources
IMAGE = 'Image'
WEBCAM = 'Webcam'

SOURCES_LIST = [IMAGE, WEBCAM]


# Images config
IMAGES_DIR = os.path.join('.', 'Test_Images')
DEFAULT_IMAGE = os.path.join(IMAGES_DIR, 'PET_bottles.jpg')
DEFAULT_DETECT_IMAGE = os.path.join(IMAGES_DIR, 'PET_bottles_detected.jpg')

# Webcam
WEBCAM_PATH = 0