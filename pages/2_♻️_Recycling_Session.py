import streamlit as st
import time
import numpy as np

import Helper
import params

st.set_page_config(page_title="Recycling Session", page_icon="♻️")

st.title("♻️ Recycling Session")
st.sidebar.header("Recycling Session")

st.write(
    """This page is dedicated on showing the results of the different user sessions which automatically get uploaded when the system is used."""
)