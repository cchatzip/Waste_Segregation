# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st

# Local Modules
import params
import Helper

# Setting page layout
st.set_page_config(
    page_title="Waste Segregation Project",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("🚀 Waste Segregation Project 🚀")

# Sidebar
st.sidebar.header("ML Model Config")

# Model Options
confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

# Setting the model path
model_path = Path(params.DETECTION_MODEL)

# Load Pre-trained ML Model
try:
    model = Helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Webcam Config")
source_radio = st.sidebar.radio(
    "Select Source", params.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == params.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(params.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(params.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")


elif source_radio == params.WEBCAM:
    Helper.play_webcam(confidence, model)

else:
    st.error("Please select a valid source type!")

st.markdown("""
  <p style='text-align: center; font-size:16px; margin-top: 32px'>
    Christodoulos Hadjipetrou - ISSEL @2024
  </p>
""", unsafe_allow_html=True)