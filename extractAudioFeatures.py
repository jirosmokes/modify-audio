import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def ensure_folder_exists(folder_path):
    """Creates a folder if it does not exist."""
    os.makedirs(folder_path, exist_ok=True)


def extract_and_visualize_features(mp3_file, output_folder):
    try:
        # Load audio file
        y, sr = librosa.load(mp3_file, sr=None)

        # Compute STFT
        stft = np.abs(librosa.stft(y))
        stft_mean = np.mean(stft, axis=1)

        # Compute MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)

        # Compute Loudness (RMS Energy)
        rms = librosa.feature.rms(y=y)[0]

        # Ensure output folder exists
        ensure_folder_exists(output_folder)

        # Generate plot filename
        filename = os.path.splitext(os.path.basename(mp3_file))[0] + "_features.png"
        plot_path = os.path.join(output_folder, filename)

        # Plot and save waveforms
        plt.figure(figsize=(12, 6))

        # STFT Waveform
        plt.subplot(3, 1, 1)
        plt.plot(stft_mean, color="blue")
        plt.title("STFT Waveform")
        plt.xlabel("Frequency Bins")
        plt.ylabel("Magnitude")
        plt.grid()

        # MFCC Waveform
        plt.subplot(3, 1, 2)
        plt.plot(mfcc_mean, color="red")
        plt.title("MFCC Waveform")
        plt.xlabel("MFCC Coefficients")
        plt.ylabel("Amplitude (dB)")
        plt.grid()

        # Loudness Waveform
        plt.subplot(3, 1, 3)
        plt.plot(rms, color="green")
        plt.title("Loudness Waveform (RMS)")
        plt.xlabel("Frames")
        plt.ylabel("Amplitude")
        plt.grid()

        plt.tight_layout()
        plt.savefig(plot_path)  # Save as image
        plt.close()

        print(f"Feature visualization saved: {plot_path}")

    except Exception as e:
        print(f"Error processing {mp3_file}: {e}")


def plot_audio_features(input_folder, output_folder):
    """Recursively processes all MP3 files in the input folder and creates matching subdirectories in visualized_dataset."""
    for subdir, _, files in os.walk(input_folder):
        relative_path = os.path.relpath(subdir, input_folder)
        output_subdir = os.path.join(output_folder, relative_path)
        ensure_folder_exists(output_subdir)

        for file in files:
            if file.endswith(".mp3"):
                input_file = os.path.join(subdir, file)
                extract_and_visualize_features(input_file, output_subdir)


# Define input and output folders
input_folder = "preprocessed_dataset"
visualized_folder = "visualized_dataset"
ensure_folder_exists(visualized_folder)

# Process all MP3 files and save to visualized_dataset with subdirectories
plot_audio_features(input_folder, visualized_folder)