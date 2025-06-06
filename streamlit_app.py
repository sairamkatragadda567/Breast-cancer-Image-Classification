import streamlit as st
import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image
import requests
import h5py

# Class mapping
class_mapping = {
    0: 'Benign',
    1: 'Malignant',
    2: 'Normal',
}

# Function to load the combined model
""" @st.cache(allow_output_mutation=True)
def load_model():
    # URLs for model parts on GitHub
    #base_url = "https://github.com/m3mentomor1/Breast-Cancer-Image-Classification/raw/main/splitted_model/"
    local_model_dir = "C:\Users\saira\Breast-Cancer-Image-Classification\splitted_model/"
    model_parts = [f"{base_url}model.h5.part{i:02d}" for i in range(1, 35)]

    # Download and combine model parts
    model_bytes = b''
    for part_url in model_parts:
        response = requests.get(part_url)
        model_bytes += response.content

    # Create an in-memory HDF5 file
    with h5py.File(BytesIO(model_bytes), 'r') as hf:
        # Load the combined model
        model = tf.keras.models.load_model(hf)
    
    return model
"""
import os
import tempfile

@st.cache_resource(show_spinner="Loading model...")
def load_model():
    # Local directory where your split model parts are saved
    local_model_dir = r"C:\Users\saira\Breast-Cancer-Image-Classification\splitted_model"

    # Generate list of local file paths in order
    model_parts = [os.path.join(local_model_dir, f"model.h5.part{i:02d}") for i in range(1, 35)]

    # Combine all parts into a single byte stream
    model_bytes = b''
    for part_path in model_parts:
        with open(part_path, 'rb') as f:
            model_bytes += f.read()

    # Write the bytes to a temporary .h5 file
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as temp_file:
        temp_file.write(model_bytes)
        temp_file.flush()
        model_path = temp_file.name

    # Load the model from the temp file
    model = tf.keras.models.load_model(model_path)
    return model

# Function to preprocess and make predictions
def predict(image, model):
    # Preprocess the image
    img_array = np.array(image)
    img_array = tf.image.resize(img_array, (256, 256))  # Adjust the size as per your model requirements
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize

    # Make prediction
    predictions = model.predict(img_array)

    # Get the predicted class
    predicted_class = class_mapping[np.argmax(predictions[0])]
    return predicted_class

# Streamlit app
st.title('Breast Cancer Image Classification')
uploaded_file = st.file_uploader("Choose a breast ultrasound image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Load the model
    model = load_model()

    # Make predictions
    predicted_class = predict(image, model)
    st.write(f"Prediction: {predicted_class}")
