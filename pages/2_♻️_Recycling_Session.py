import streamlit as st

import params
import Helper

st.set_page_config(page_title="Recycling Session", page_icon="♻️")

st.title("♻️ Recycling Session")
st.sidebar.header("Recycling Session")

st.write(
    """This page is dedicated on showing the results of the different user sessions which automatically get uploaded when the system is used."""
)

source_radio = st.sidebar.radio("Select an Option", params.SESSIONS_LIST)

# Check if the user selected a session
if source_radio:
    # Load and display the selected session data
    session_data = Helper.load_session_data(source_radio)
    if session_data:
        st.write(f"**Session ID:** {session_data['session_id']}")
        st.write(f"**Timestamp:** {session_data['timestamp']}")
        st.write(f"**Total Objects Processed:** {session_data['analytics']['total_objects']}")
        st.write(f"**Metal Objects:** {session_data['analytics']['metal_objects']}")
        st.write(f"**Plastic Objects:** {session_data['analytics']['plastic_objects']}")
        
        # Display the objects and their details
        for obj in session_data["objects"]:
            st.write(f"- Type: {obj['type']}")
            st.write(f"  Confidence: {obj['confidence']}")
            col1, col2 = st.columns(2)
            with col1:
                try:
                    st.image(obj['image_before'], caption='Before Classification', use_column_width=True)
                except Exception as ex:
                    st.error("Error occurred while opening the image.")
                    st.error(ex)

            with col2:
                try:
                    st.image(obj['image_after'], caption='After Classification', use_column_width=True)
                except Exception as ex:
                    st.error("Error occurred while opening the image.")
                    st.error(ex)
            
    else:
        st.write("No data found for the selected session.")




st.markdown("""
  <p style='text-align: center; font-size:16px; margin-top: 32px'>
    Christodoulos Hadjipetrou - ISSEL @2024
  </p>
""", unsafe_allow_html=True)

