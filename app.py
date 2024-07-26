import streamlit as st
import cv2
import numpy as np

st.set_page_config(
  page_title="Waste Segregation Project",
  page_icon="🚀"
)

st.title('Waste Segregation Project')

st.markdown('This is an application for object detection and classification')
st.markdown('Powered by YOLOv8')

img_files = st.file_uploader(label="Choose image files",
                 type=['png', 'jpg', 'jpeg'],
                 accept_multiple_files=True)


# function to convert file buffer to cv2 image
def create_opencv_image_from_stringio(img_stream, cv2_img_flag=1):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)


for n, img_file_buffer in enumerate(img_files):
  if img_file_buffer is not None:
    # we'll do this later
    # 1) image file buffer will converted to cv2 image
    open_cv_image = create_opencv_image_from_stringio(img_file_buffer)
    # 2) pass image to the model to get the detection result
    im0 = run(source=open_cv_image, \
    conf_thres=0.25, weights="runs/detect/yolov7.pt")
    # 3) show result image using st.image()

if im0 is not None:
  st.image(im0, channels="BGR", \
  caption=f'Detection Results ({n+1}/{len(img_files)})')
  


st.markdown("""
  <p style='text-align: center; font-size:16px; margin-top: 32px'>
    Christodoulos Hadjipetrou - ISSEL @2024
  </p>
""", unsafe_allow_html=True)

