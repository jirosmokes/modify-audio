from detectFeatures import detect_earrape_sounds, plot_spectrogram_with_flags, preprocess_spectrogram_for_vgg16
import tensorflow as tf
import librosa

# Example Usage
audio_file_path = "sampleAudio.mp3"  # Replace with your audio file path
flagged_intervals, stft_energy, mfcc_delta_var, loudness = detect_earrape_sounds(audio_file_path)

# Display results
if flagged_intervals:
    print("Flagged intervals indicating overstimulating sounds:")
    for start, end in flagged_intervals:
        print(f"Start: {start:.2f} s, End: {end:.2f} s")
else:
    print("No overstimulating sounds detected.")

# Load audio again for visualization
y, sr = librosa.load(audio_file_path, sr=None)

# Plot spectrogram with flagged intervals
D = plot_spectrogram_with_flags(y, sr, flagged_intervals)

# Preprocess the spectrogram for VGG16
spectrogram_for_vgg16 = preprocess_spectrogram_for_vgg16(D)

# Load the VGG16 model and make a prediction
vgg16_model = tf.keras.applications.VGG16(weights='imagenet', include_top=False)
features = vgg16_model.predict(spectrogram_for_vgg16)
print("VGG16 features shape:", features.shape)
