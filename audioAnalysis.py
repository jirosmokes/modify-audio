import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import correlate

def create_directory_if_not_exists(directory):
    """Ensure the directory exists, create it if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def preprocess_audio(audio_file):
    """Load and preprocess the audio file (trim silence, normalize)."""
    y, sr = librosa.load(audio_file)
    y_trimmed, _ = librosa.effects.trim(y)  # Trim leading and trailing silence
    y_normalized = librosa.util.normalize(y_trimmed)  # Normalize audio
    return y_normalized, sr


def analyze_audio_stft(audio_file, output_dir, n_fft=2048, hop_length=512):
    """Analyze the STFT of the audio file with enhanced reliability."""
    create_directory_if_not_exists(output_dir)

    # Preprocess the audio file
    y, sr = preprocess_audio(audio_file)

    # Compute STFT with chosen parameters
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, window='hann')

    # Convert to Decibels for visualization
    D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    # Plot the spectrogram
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(D_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Enhanced STFT Spectrogram')

    # Save the plot
    filename = os.path.basename(audio_file).replace('.mp3', '').replace('.wav', '')
    output_path = os.path.join(output_dir, f"stft_spectrogram_{filename}.png")
    plt.savefig(output_path, format='png')
    plt.close()

    print(f"Enhanced STFT Spectrogram saved at: {output_path}")


def analyze_audio_mfcc(audio_file, output_dir, n_mfcc=13, include_delta=True):
    """Analyze the MFCCs of the audio file with enhanced reliability."""
    create_directory_if_not_exists(output_dir)

    # Preprocess the audio file
    y, sr = preprocess_audio(audio_file)

    # Compute MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    if include_delta:
        delta_mfccs = librosa.feature.delta(mfccs)
        delta2_mfccs = librosa.feature.delta(mfccs, order=2)
        combined_mfccs = np.vstack((mfccs, delta_mfccs, delta2_mfccs))
    else:
        combined_mfccs = mfccs

    # Convert to log scale for better visualization
    log_mfccs = librosa.power_to_db(combined_mfccs, ref=np.max)

    # Plot MFCCs
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(log_mfccs, sr=sr, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Enhanced MFCC (with Delta Features)' if include_delta else 'Enhanced MFCC')

    # Save the plot
    filename = os.path.basename(audio_file).replace('.mp3', '').replace('.wav', '')
    output_path = os.path.join(output_dir, f"mfcc_spectrogram_{filename}.png")
    plt.savefig(output_path, format='png')
    plt.close()

    print(f"Enhanced MFCC Spectrogram saved at: {output_path}")


def visualize_loudness(audio_file, threshold_loudness=0.1, output_dir="loudness_images"):
    """Visualize loudness (dBFS) and highlight loudness spikes, saving the plot as a PNG."""
    y, sr = librosa.load(audio_file)

    # Compute RMS (Root Mean Square)
    rms = librosa.feature.rms(y=y)
    loudness_dbfs = 20 * np.log10(rms + 1e-6)  # Convert RMS to dBFS

    # Plot loudness
    plt.figure(figsize=(10, 6))
    plt.plot(loudness_dbfs[0], label='Loudness (dBFS)')
    plt.axhline(y=threshold_loudness, color='r', linestyle='--', label='Threshold')
    plt.title('Loudness (dBFS)')
    plt.legend()

    # Save the plot as PNG
    create_directory_if_not_exists(output_dir)
    filename = os.path.basename(audio_file).replace('.mp3', '').replace('.wav', '')
    output_path = os.path.join(output_dir, f"loudness_plot_{filename}.png")
    plt.savefig(output_path, format='png')  # Save the plot to a PNG file
    plt.close()  # Close the plot to avoid it being displayed interactively

    print(f"Loudness plot saved to: {output_path}")
