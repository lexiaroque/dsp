import streamlit as st
from pydub import AudioSegment
from io import BytesIO

# Set the title and page layout
st.title("Audio Player App")

# Create a file upload widget in the sidebar
audio_file = st.sidebar.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg", "m4a"])

# Initialize variables to hold audio data and display status
audio_data = None
audio_format = None
play_audio = False

# Check if an audio file was uploaded
if audio_file is not None:
    try:
        # Read the uploaded audio file and store it in audio_data
        audio_data = audio_file.read()
        audio_format = audio_file.type

        # Display audio information
        st.sidebar.text("Uploaded Audio:")
        st.sidebar.audio(audio_data, format=audio_format)
        play_audio = True
    except Exception as e:
        st.write("Error reading the uploaded audio file.")
        st.write(f"Error details: {str(e)}")

# Display the audio player
st.header("Audio Player")

if play_audio:
    try:
        # Use pydub to convert audio_data to a compatible format for playback
        st.audio(audio_data, format=audio_format)
    except Exception as e:
        st.write("Error playing the audio.")
        st.write(f"Error details: {str(e)}")
else:
    st.write("Please upload an audio file to play.")

# Optionally, display audio duration and other information
if audio_data:
    audio = AudioSegment.from_file(BytesIO(audio_data), format=audio_format)
    audio_duration = len(audio) / 1000  # Convert to seconds
    st.write(f"Audio Duration: {audio_duration:.2f} seconds")

# Optionally, you can add more functionality or styling to the app
