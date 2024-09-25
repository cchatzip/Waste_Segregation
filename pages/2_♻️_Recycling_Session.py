import streamlit as st
import time

import params
import Helper
import Main_SystemStreamlit

# Set Streamlit page configuration
st.set_page_config(page_title="Recycling Session", page_icon="♻️")

# Set the main title of the page
st.title("♻️ Recycling Session")


#===============INITIATE A NEW RECYCLING SESSION ====================


# Session state to track whether the system is running
if "session_active" not in st.session_state:
    st.session_state.session_active = False  # Whether the session is currently running
if "session_complete" not in st.session_state:
    st.session_state.session_complete = False  # Whether the session has been completed

# Sidebar for session initiation
st.sidebar.header("Initiate a New Recycling Session")

# Button to start the recycling session
if not st.session_state.session_active and not st.session_state.session_complete:
    if st.sidebar.button('Start Session'):
        st.session_state.session_active = True  # Mark session as active
        st.session_state.session_complete = False  # Reset the session complete flag
        st.sidebar.empty()  # Optionally clear the sidebar

# Check if the session is active
if st.session_state.session_active:
        st.write("Starting new recycling session...")
        
        # Add a spinner for visual feedback during long-running processes
        with st.spinner('Processing...'):
            Main_SystemStreamlit.main_system()

        # Once processing is done
        st.success("Session finished!")
        st.session_state.session_active = False  # Mark session as no longer active
        st.session_state.session_complete = True  # Mark the session as complete

#=========================================================================


#=========================Sessions List==================================

st.sidebar.header("Recycling Sessions list")

st.write(
    """This page is dedicated on showing the results of the different user sessions when they use the recycling system."""
)

source_radio = st.sidebar.radio("Select a Session to display", params.SESSIONS_LIST)

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

