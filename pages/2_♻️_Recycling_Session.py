import streamlit as st
import subprocess
import time

import params
import Helper
import Main_System

st.set_page_config(page_title="Recycling Session", page_icon="♻️")

st.title("♻️ Recycling Session")

#TO-DO: CALL THE MAIN SYSTEM SCRIPT FROM STREAMLIT
st.sidebar.header("Initiate a New Recycling Session")
# Button to start the script
if st.button('Start'):
    # Inform the user that the process is starting
    st.info("Starting the Main System Script...")

    # Placeholder for output
    output_placeholder = st.empty()

    # Create a container to display logs
    log_container = st.container()
    log_container.subheader("Real-Time Logs")

    # Create a progress bar
    progress_bar = st.progress(0)
    
    # Run the script using subprocess
    process = subprocess.Popen(
        ['python3', 'Main_System.py'],  # Adjust with the correct path if needed
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Read the output in real-time
    total_lines = 0
    for line in iter(process.stdout.readline, ''):
        total_lines += 1
        # Format and display output
        if "Error" in line or "Exception" in line:
            log_container.error(line.strip())
        elif "Warning" in line:
            log_container.warning(line.strip())
        else:
            log_container.write(line.strip())
        
        # Update progress bar based on some heuristic (total_lines or another metric)
        progress_bar.progress(min(total_lines % 100, 100) / 100)  # Example logic to fill progress bar

        time.sleep(0.2)  # Add a short delay to reduce the frequency of updates

    # Close the process
    process.stdout.close()
    process.wait()

    # Finish progress
    progress_bar.progress(100)
    st.success("Main Script Finished Running Successfully!")

    # Display a final message
    st.balloons()  # Fun addition: display balloons when done






#Sessions List
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

