import tensorflow as tf
import numpy as np
import os
from PIL import Image
import re
import json

def load_ai_model(model_path="overstimulating_audio_detector.h5"):
    """Loads the trained AI model for detecting overstimulating audio."""
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        exit(1)

def natural_sort_key(filename):
    """Extracts numbers from filenames for correct numerical sorting."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", filename)]

def detect_overstimulating_segments(segment_folder, ai_model, segment_length=4.0, threshold=0.75):
    """Detects overstimulating segments from spectrogram images with confidence scores."""
    overstim_results = []

    try:
        segment_files = sorted(os.listdir(segment_folder), key=natural_sort_key)  # Ensure correct order
    except FileNotFoundError:
        print(f"Error: Folder '{segment_folder}' not found.")
        exit(1)

    for i, segment_file in enumerate(segment_files):
        if segment_file.endswith(".png"):
            segment_path = os.path.join(segment_folder, segment_file)

            try:
                # Load and preprocess image
                img = Image.open(segment_path).convert("RGB").resize((224, 224))
                img_array = np.array(img) / 255.0  # Normalize pixel values
                img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

                # Predict overstimulation
                prediction = ai_model.predict(img_array)
                confidence = float(prediction[0])  # Convert NumPy array to float
                is_overstim = confidence > threshold  # Apply threshold

                # Calculate time range
                start_time = round(i * segment_length, 2)
                end_time = round(start_time + segment_length, 2)

                # Append result with confidence score
                overstim_results.append({
                    "segment": segment_file,
                    "start_time": start_time,
                    "end_time": end_time,
                    "overstimulating": is_overstim,
                    "confidence": round(confidence, 4)  # ✅ Confidence added for analysis
                })
            except Exception as e:
                print(f"Error processing {segment_file}: {e}")

    return overstim_results

def save_and_print_results(overstim_results, output_json_path="overstimulating_segments.json"):
    """
    Saves the overstimulating segment detection results to a JSON file and prints the results with confidence scores.

    :param overstim_results: List of dictionaries containing segment information.
    :param output_json_path: Path to save the JSON file.
    """
    try:
        with open(output_json_path, "w") as json_file:
            json.dump(overstim_results, json_file, indent=4)
        print(f"Overstimulating segments detection completed. Results saved to {output_json_path}.")
    except Exception as e:
        print(f"Error saving results to JSON: {e}")

    # Print results with confidence scores
    for segment in overstim_results:
        print(f"Segment: {segment['segment']}, Time Range: {segment['start_time']} - {segment['end_time']} sec, "
              f"Overstimulating: {segment['overstimulating']}, Confidence: {segment['confidence']}")

# Example Usage
# Load AI model
# ai_model = load_ai_model()
# segment_folder = "spectrogram_segments"  # Folder containing segmented spectrogram images
#
# # Detect overstimulating segments
# overstim_results = detect_overstimulating_segments(segment_folder, ai_model)
#
# save_and_print_results(overstim_results)



