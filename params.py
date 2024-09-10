import os

# ML Model config
MODEL_DIR = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset', 'weights')
DETECTION_MODEL = os.path.join(MODEL_DIR, 'best.pt')

# Sources (Main_Page)
IMAGE = 'Image'
WEBCAM = 'Webcam' #(Working only when streamlit runs locally)

# Sources (Model_Metrics)
CONFUSION_MATRIX = 'Confusion Matrix'
CURVES = 'Curves'
LABELS = 'Labels'
RESULTS = 'Loss & MAP Plots'
VALIDATION = 'Validation batches and Detections'

# Sources (Recycling_Session)
USERSESSION_DIR = os.path.join('.', 'User_Session')
items = os.listdir(USERSESSION_DIR)

if len(items) > 10:
    latest_sessions = items[:10]
else:
    latest_sessions = items
    


SOURCES_LIST = [IMAGE]
METRICS_LIST = [CONFUSION_MATRIX, CURVES, LABELS, RESULTS, VALIDATION]
SESSIONS_LIST = latest_sessions


# Default Images config (Main_Page)
IMAGES_DIR = os.path.join('.', 'Test_Images')
PREDICTIONS_DIR = os.path.join('.', 'Predictions')
DEFAULT_IMAGE = os.path.join(IMAGES_DIR, 'Multiple_bottles3.jpg')
DEFAULT_DETECT_IMAGE = os.path.join(PREDICTIONS_DIR, 'Multiple_bottles3_detected.jpg')

#Metrics Images config (Model_Metrics)
METRICS_DIR = os.path.join('.', 'runs', 'detect', 'train4_300ep_ReformedDataset')

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