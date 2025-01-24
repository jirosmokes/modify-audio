import librosa
import numpy as np
import matplotlib.pyplot as plt

def detect_earrape_sounds(
    audio_file, 
    stft_thresh_factor=2.0, 
    mfcc_delta_thresh=0.1, 
    loudness_thresh=-10.0
):
    """
    Detect "earrape" or chaotic sounds in short videos based on loudness, STFT energy, and MFCC variance.

    Parameters:
        audio_file (str): Path to the audio file (MP3, WAV, etc.).
        stft_thresh_factor (float): Multiplier for the dynamic STFT energy threshold (spikes).
        mfcc_delta_thresh (float): Threshold for extreme MFCC delta variance.
        loudness_thresh (float): Threshold for loudness in decibels (dBFS).

    Returns:
        list: Merged time intervals (in seconds) flagged as chaotic or "earrape".
    """
    def compute_loudness(y):
        """Compute loudness in decibels (dBFS)."""
        rms = np.sqrt(np.mean(y**2))
        return 20 * np.log10(rms) if rms > 0 else -np.inf

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

    try:
        # Load the audio file
        y, sr = librosa.load(audio_file, sr=None)
        hop_length = 512  # Hop length for STFT and MFCC
        frame_duration = hop_length / sr

        # Compute STFT
        stft = np.abs(librosa.stft(y, hop_length=hop_length))
        stft_energy = np.mean(stft, axis=0)
        stft_energy = stft_energy / np.max(stft_energy)  # Normalize
        rolling_thresh = np.mean(stft_energy) * stft_thresh_factor

        # Compute MFCC and MFCC delta
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta_var = np.var(mfcc_delta, axis=0)

        # Compute loudness
        loudness = compute_loudness(y)

        # Flag intervals
        flagged_intervals = []
        for i, (energy, delta_var) in enumerate(zip(stft_energy, mfcc_delta_var)):
            if (energy > rolling_thresh and loudness > loudness_thresh) or delta_var < mfcc_delta_thresh:
                flagged_intervals.append((
                    i * frame_duration,
                    (i + 1) * frame_duration
                ))

        # Merge overlapping intervals
        merged_intervals = merge_intervals(flagged_intervals)
        return merged_intervals

    except FileNotFoundError:
        print(f"Error: File not found at {audio_file}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example Usage
audio_file_path = "sampleAudio.mp3"  # Replace with your audio file path
flagged_intervals = detect_earrape_sounds(audio_file_path)

# Display results
if flagged_intervals:
    print("Flagged 'earrape' or chaotic intervals:")
    for start, end in flagged_intervals:
        print(f"- From {start:.2f}s to {end:.2f}s")
else:
    print("No chaotic sounds detected.")

# Optional Visualization
if flagged_intervals:
    y, sr = librosa.load(audio_file_path, sr=None)
    stft = np.abs(librosa.stft(y))
    stft_energy = np.mean(stft, axis=0)
    stft_energy = stft_energy / np.max(stft_energy)
    times = librosa.frames_to_time(range(len(stft_energy)), sr=sr, hop_length=512)

    plt.figure(figsize=(10, 6))
    plt.plot(times, stft_energy, label="STFT Energy")
    
    for start, end in flagged_intervals:
        plt.axvspan(start, end, color="red", alpha=0.3, label="Flagged Interval" if start == flagged_intervals[0][0] else "")

    plt.xlabel("Time (s)")
    plt.ylabel("Normalized Energy")
    plt.title("STFT Energy with Flagged Intervals ('Earrape')")
    plt.legend()
    plt.show()
