import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from PIL import Image

st.set_option('deprecation.showPyplotGlobalUse', False)

def load_model():
    model_path = 'model_vgg16.h5'  # Ensure this is the correct path
    return tf.keras.models.load_model(model_path)

def process_audio_file(uploaded_file):
    # Load the model
    model = load_model()

    # Add your processing logic here
    st.audio(uploaded_file, format='audio/wav')

    # Load audio using librosa
    y, sr = librosa.load(uploaded_file, sr=None)

    # Plot waveform
    plt.figure(figsize=(4, 4))
    plt.title('Waveform Visualization')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.plot(np.arange(len(y)) / sr, y)
    st.pyplot()

    # Create and display mel spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    plt.figure(figsize=(4, 4))
    librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
    plt.title('Mel Spectrogram')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    st.pyplot()

    # Save the spectrogram to a temporary file
    spectrogram_path = 'temp_spectrogram.png'
    plt.savefig(spectrogram_path)

    # Preprocess and predict the spectrogram image
    try:
        img = Image.open(spectrogram_path).convert('RGB')  # Convert to RGB
        img = img.resize((256, 256))  # Resize to match model input
        img_array = np.array(img) / 255.0  # Normalize pixel values
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        prediction = model.predict(img_array)
        class_index = np.argmax(prediction)
        class_name = ["AI-Generated Voice", "Real Voice"][class_index]
        st.success("Prediction: " + class_name)
    except Exception as e:
        st.error(f"Error processing image: {e}")

def main():
    st.set_page_config(page_title='Audio Analysis App', page_icon='🔊')
    st.title('A Deep Learning Approach to Analyzing Real vs. AI-Generated Voices Using Mel Spectrogram Analysis')

    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        if st.button('Process Audio'):
            process_audio_file(uploaded_file)

if __name__ == "__main__":
    main()
