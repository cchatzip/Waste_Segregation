import streamlit as st
import time
import os

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
    st.session_state.session_complete = True  # Whether the session has been completed
if "system_initialized" not in st.session_state:
    st.session_state.system_initialized = False # Variable for initialization of the system files and directories

# Sidebar for session initiation
st.sidebar.header("Initiate a New Recycling Session")

# Container for the session list
session_list_container = st.empty()  # Create an empty container


# Button to start the recycling session
if st.sidebar.button('Start Session'):
    if not st.session_state.session_active and st.session_state.session_complete:
        st.write("Starting new recycling session...")
        st.session_state.session_active = True  # Mark session as active
        st.session_state.session_complete = False  # Reset the session complete flag

        # Empty the session list container when the session starts
        session_list_container.empty()  # This will hide the session list and radio button
        
# Check if the session is active
if not st.session_state.session_complete:
        
        # Add a spinner for visual feedback during long-running processes
        with st.spinner('Processing...'):
            Main_SystemStreamlit.main_system()

#=========================================================================





#=========================Sessions List==================================

st.sidebar.header("Recycling Sessions list")

# st.write(
#     """This page is dedicated on showing the results of the different user sessions when they use the recycling system."""
# )



# User Session sources
usersession_dir = os.path.join('.', 'User_Session')
items = os.listdir(usersession_dir)

if len(items) > 10:
    latest_sessions = items[:10]
else:
    latest_sessions = items


source_radio = st.sidebar.radio("Select a Session to display", latest_sessions)

# Render the session data of the source radio selection only if there is not an active recycling session
if st.session_state.session_complete:

    with session_list_container.container():

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

