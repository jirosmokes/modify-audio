import librosa
import numpy as np
import matplotlib.pyplot as plt

def detect_earrape_sounds(
    audio_file, 
    stft_thresh_factor=2.0, 
    mfcc_delta_thresh=0.1, 
    loudness_thresh=-10.0, 
    repetition_thresh=0.5, 
    min_repetition_duration=0.5, 
    smoothing_window_size=3,
    flag_margin=0.1  # Margin in seconds to extend the flagged intervals
):
    """
    Detect "earrape" or chaotic sounds and repetitive sounds that may lead to overstimulation in kids.
    
    Parameters:
        audio_file (str): Path to the audio file (MP3, WAV, etc.).
        stft_thresh_factor (float): Multiplier for the dynamic STFT energy threshold (spikes).
        mfcc_delta_thresh (float): Threshold for extreme MFCC delta variance.
        loudness_thresh (float): Threshold for loudness in decibels (dBFS).
        repetition_thresh (float): Correlation threshold for repetitive sounds.
        min_repetition_duration (float): Minimum duration in seconds for repetitive sounds.
        smoothing_window_size (int): Window size for smoothing feature values.
        flag_margin (float): Margin (in seconds) to extend flagged intervals to capture surrounding spikes.
    
    Returns:
        list: Merged time intervals (in seconds) flagged as chaotic or "earrape" and repetitive sounds.
    """
    
    def compute_loudness(y, hop_length, frame_size):
        """Compute loudness in decibels (dBFS) for each frame."""
        loudness = []
        for i in range(0, len(y) - frame_size, hop_length):
            frame = y[i:i+frame_size]
            rms = np.sqrt(np.mean(frame**2))
            loudness.append(20 * np.log10(rms) if rms > 0 else -np.inf)
        return np.array(loudness)

    def smooth_feature(feature, window_size):
        """Apply a simple moving average to smooth a feature.""" 
        return np.convolve(feature, np.ones(window_size)/window_size, mode='same')

    def merge_intervals(intervals):
        """Merge overlapping intervals."""
        if not intervals:
            return []
        intervals.sort()
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            last_end = merged[-1][1]
            if start <= last_end:  # Overlapping intervals
                merged[-1] = (merged[-1][0], max(last_end, end))
            else:
                merged.append((start, end))
        return merged

    def detect_repetitive_sound(y, sr):
        """Detect repetitive sound patterns based on autocorrelation."""
        autocorr = librosa.core.autocorrelate(y)
        autocorr_peak = np.argmax(autocorr[1:]) + 1  # Peak after the first lag
        duration = autocorr_peak / sr
        return duration >= min_repetition_duration and autocorr[autocorr_peak] > repetition_thresh

    try:
        # Load the audio file once and reuse the results
        y, sr = librosa.load(audio_file, sr=None)
        hop_length = 512  # Hop length for STFT and MFCC
        frame_size = 2048  # Frame size for calculating loudness
        frame_duration = hop_length / sr

        # Compute STFT and energy
        stft = np.abs(librosa.stft(y, hop_length=hop_length))
        stft_energy = np.mean(stft, axis=0)
        stft_energy /= np.max(stft_energy)  # Normalize energy
        stft_energy_smoothed = smooth_feature(stft_energy, smoothing_window_size)

        # Compute MFCC and MFCC delta
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta_var = np.var(mfcc_delta, axis=0)
        mfcc_delta_smoothed = smooth_feature(mfcc_delta_var, smoothing_window_size)

        # Compute loudness frame by frame
        loudness = compute_loudness(y, hop_length, frame_size)
        loudness_smoothed = smooth_feature(loudness, smoothing_window_size)

        # Flag intervals for chaotic sounds
        flagged_intervals = []
        stft_thresh = np.mean(stft_energy_smoothed) * stft_thresh_factor
        loudness_thresh_dynamic = np.mean(loudness_smoothed) + loudness_thresh  # Dynamic threshold based on mean loudness

        for i, (energy, delta_var, loud) in enumerate(zip(stft_energy_smoothed, mfcc_delta_smoothed, loudness_smoothed)):
            # Chaotic flagging conditions
            if (energy > stft_thresh and loud > loudness_thresh_dynamic) or delta_var < mfcc_delta_thresh:
                start_time = i * frame_duration
                end_time = (i + 1) * frame_duration
                
                # Extend the flagged interval by a margin (before and after)
                start_time = max(0, start_time - flag_margin)  # Ensure we don't go below 0
                end_time = min(len(y) / sr, end_time + flag_margin)  # Ensure we don't exceed the audio duration
                flagged_intervals.append((start_time, end_time))

        # Detect repetitive sounds
        if detect_repetitive_sound(y, sr):
            flagged_intervals.append((0, len(y) / sr))  # Flag entire audio if repetitive

        # Merge overlapping intervals
        merged_intervals = merge_intervals(flagged_intervals)
        return merged_intervals, stft_energy_smoothed, mfcc_delta_smoothed, loudness_smoothed

    except FileNotFoundError:
        print(f"Error: File not found at {audio_file}")
        return [], [], [], []
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], [], []

def plot_results(flagged_intervals, stft_energy, mfcc_delta_var, loudness, audio_file_path):
    """Helper function to visualize results."""
    if not flagged_intervals:
        return
    
    # Load audio again for visualization
    y, sr = librosa.load(audio_file_path, sr=None)
    hop_length = 512
    times = librosa.frames_to_time(range(len(stft_energy)), sr=sr, hop_length=hop_length)

    plt.figure(figsize=(15, 8))

    # Plot STFT Energy
    plt.subplot(3, 1, 1)
    plt.plot(times, stft_energy, label="STFT Energy")
    plt.title("STFT Energy")
    plt.xlabel("Time (s)")
    plt.ylabel("Normalized Energy")
    for start, end in flagged_intervals:
        plt.axvspan(start, end, color="red", alpha=0.3, label="Chaotic Interval" if start == flagged_intervals[0][0] else "")

    # Plot MFCC Delta Variance
    plt.subplot(3, 1, 2)
    plt.plot(times, mfcc_delta_var, label="MFCC Delta Variance", color="orange")
    plt.title("MFCC Delta Variance")
    plt.xlabel("Time (s)")
    plt.ylabel("Variance")
    for start, end in flagged_intervals:
        plt.axvspan(start, end, color="red", alpha=0.3, label="Chaotic Interval" if start == flagged_intervals[0][0] else "")

    # Plot Loudness
    plt.subplot(3, 1, 3)
    time_loudness = librosa.frames_to_time(range(len(loudness)), sr=sr, hop_length=hop_length)
    plt.plot(time_loudness, loudness, label="Loudness", color="green")
    plt.title("Loudness (dBFS)")
    plt.xlabel("Time (s)")
    plt.ylabel("Loudness (dBFS)")
    for start, end in flagged_intervals:
        plt.axvspan(start, end, color="red", alpha=0.3, label="Chaotic Interval" if start == flagged_intervals[0][0] else "")

    # Display the plot
    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.show()

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

# Plot the results
plot_results(flagged_intervals, stft_energy, mfcc_delta_var, loudness, audio_file_path)
