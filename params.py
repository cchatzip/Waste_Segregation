import os

# ML Model config
MODEL_DIR = os.path.join('.', 'runs', 'detect', 'train2_300ep', 'weights')
DETECTION_MODEL = os.path.join(MODEL_DIR, 'best.pt')

# Sources
IMAGE = 'Image'
WEBCAM = 'Webcam'

# Model Metrics
CONFUSION_MATRIX = 'Confusion Matrix'
CURVES = 'Curves'
LABELS = 'Labels'
RESULTS = 'Loss & MAP Plots'
VALIDATION = 'Validation batches and Detections'

SOURCES_LIST = [IMAGE, WEBCAM]
METRICS_LIST = [CONFUSION_MATRIX, CURVES, LABELS, RESULTS, VALIDATION]


# Images config
IMAGES_DIR = os.path.join('.', 'Test_Images')
PREDICTIONS_DIR = os.path.join('.', 'Predictions')
DEFAULT_IMAGE = os.path.join(IMAGES_DIR, 'PET_bottles.jpg')
DEFAULT_DETECT_IMAGE = os.path.join(PREDICTIONS_DIR, 'PET_bottles_detected.jpg')

#Metrics Images config
METRICS_DIR = os.path.join('.', 'runs', 'detect', 'train2_300ep')

CONF_MTRX = os.path.join(METRICS_DIR, 'confusion_matrix.png')
CONF_MTRX_NORM = os.path.join(METRICS_DIR, 'confusion_matrix_normalized.png')
F1_CURVE = os.path.join(METRICS_DIR, 'F1_curve.png')
P_CURVE = os.path.join(METRICS_DIR, 'P_curve.png')
PR_CURVE = os.path.join(METRICS_DIR, 'PR_curve.png')
R_CURVE = os.path.join(METRICS_DIR, 'R_curve.png')
LBLS = os.path.join(METRICS_DIR, 'labels.jpg')
RSLTS = os.path.join(METRICS_DIR, 'results.png')
BATCH0_LBLS = os.path.join(METRICS_DIR, 'val_batch0_labels.jpg')
BATCH0_PRED = os.path.join(METRICS_DIR, 'val_batch0_pred.jpg')
BATCH1_LBLS = os.path.join(METRICS_DIR, 'val_batch1_labels.jpg')
BATCH1_PRED = os.path.join(METRICS_DIR, 'val_batch1_pred.jpg')


# Webcam
WEBCAM_PATH = 0