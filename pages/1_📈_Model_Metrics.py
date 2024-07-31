import streamlit as st
import time
import numpy as np

import Helper
import params

st.set_page_config(page_title="Model Metrics", page_icon="📈")

st.title("📈 Model Metrics")
st.sidebar.header("Model Metrics")

source_radio = st.sidebar.radio(
    "Select an Option", params.METRICS_LIST)
st.write(
    """This page is dedicated on showing the metrics of the model to give you a grasp of it's performance"""
)

#IF THE OPTION IS CONFUSION MATRIX
if source_radio == params.CONFUSION_MATRIX:
    col1, col2 = st.columns(2)


    with col1:
        try:
            st.image(params.CONF_MTRX, caption="Confusion Matrix",
                use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        try:
            st.image(params.CONF_MTRX_NORM, caption="Confusion Matrix Normalized",
                use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)


#IF THE OPTION IS CURVES
if source_radio == params.CURVES:
    try:
        st.image(params.F1_CURVE, use_column_width=True)
    except Exception as ex:
        st.error("Error occurred while opening the image.")
        st.error(ex)
    
    try:
        st.image(params.P_CURVE, use_column_width=True)
    except Exception as ex:
        st.error("Error occurred while opening the image.")
        st.error(ex)
    
    try:
        st.image(params.PR_CURVE, use_column_width=True)
    except Exception as ex:
        st.error("Error occurred while opening the image.")
        st.error(ex)
    
    try:
        st.image(params.R_CURVE, use_column_width=True)
    except Exception as ex:
        st.error("Error occurred while opening the image.")
        st.error(ex)

#IF THE OPTION IS LABELS
if source_radio == params.LABELS:
    try:
        st.image(params.LBLS, use_column_width=True)
    except Exception as ex:
        st.error("Error occurred while opening the image.")
        st.error(ex)

#IF THE OPTION IS Loss & MAP Plots
if source_radio == params.RESULTS:
    try:
        st.image(params.RSLTS, use_column_width=True)
    except Exception as ex:
        st.error("Error occurred while opening the image.")
        st.error(ex)

#IF THE OPTION IS Loss & MAP Plots
if source_radio == params.VALIDATION:
    col1, col2 = st.columns(2)


    with col1:
        try:
            st.image(params.BATCH0_LBLS, caption="Batch 0 labels",
                use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        try:
            st.image(params.BATCH0_PRED, caption="Batch 0 model predictions",
                use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)
    
    #Page second row
    with col1:
        try:
            st.image(params.BATCH1_LBLS, caption="Batch 1 labels",
                use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        try:
            st.image(params.BATCH1_PRED, caption="Batch 1 model predictions",
                use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

st.markdown("""
  <p style='text-align: center; font-size:16px; margin-top: 32px'>
    Christodoulos Hadjipetrou - ISSEL @2024
  </p>
""", unsafe_allow_html=True)