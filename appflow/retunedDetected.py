import json
import librosa
import soundfile as sf
import numpy as np
import moviepy as mp
from scipy.signal import butter, lfilter

def load_overstim_segments(json_file):
    """Loads detected overstimulating segments from a JSON file."""
    with open(json_file, "r") as file:
        return json.load(file)

def butter_filter(data, cutoff, fs, order=8, filter_type="low"):
    """Applies a stronger Butterworth filter (low-pass or high-pass) to reduce unwanted frequencies."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
    return lfilter(b, a, data)

def reduce_loudness(audio, factor=0.1):
    """Drastically reduces loudness by scaling amplitude more aggressively."""
    return audio * factor

def fade_audio(audio, fade_length):
    """Applies an extended fade-in and fade-out effect to smooth transitions."""
    fade = np.linspace(0, 1, fade_length)
    audio[:fade_length] *= fade  # Fade-in
    audio[-fade_length:] *= fade[::-1]  # Fade-out
    return audio

def compress_audio(audio):
    """Applies a stronger dynamic range compression to prevent loud peaks."""
    return np.tanh(audio * 3)  # More aggressive compression

def retune_audio(input_audio, output_audio, overstim_segments):
    """Processes and aggressively retunes only overstimulating segments for safer listening."""
    y, sr = librosa.load(input_audio, sr=44100)

    processed_segments = []
    for segment in overstim_segments:
        try:
            start_time = float(segment["start_time"])
            end_time = float(segment["end_time"])
            segment_file = segment["segment"]
            overstim_status = segment.get("overstimulating", True)

            if overstim_status:  # Apply retuning only if overstimulating is True
                start_sample = int(start_time * sr)
                end_sample = int(end_time * sr)

                # Apply aggressive filtering and modifications
                y[start_sample:end_sample] = butter_filter(y[start_sample:end_sample], cutoff=1500, fs=sr, filter_type="low")  # Reduce sharp highs
                y[start_sample:end_sample] = butter_filter(y[start_sample:end_sample], cutoff=400, fs=sr, filter_type="high")  # Remove deep rumble
                y[start_sample:end_sample] = reduce_loudness(y[start_sample:end_sample], factor=0.1)  # Reduce volume heavily

                # Apply extended fade effect for smoother transitions
                fade_length = int(0.75 * sr)  # 750ms fade
                y[start_sample:end_sample] = fade_audio(y[start_sample:end_sample], fade_length)

                # Apply stronger compression to balance loudness
                y[start_sample:end_sample] = compress_audio(y[start_sample:end_sample])

                processed_segments.append(f"Segment: {segment_file}, Time Range: {start_time:.1f} - {end_time:.1f} sec, Overstimulating: True")

        except (KeyError, ValueError, TypeError) as e:
            print(f"Skipping segment due to error: {e}")

    # Save the modified audio
    sf.write(output_audio, y, sr)
    print(f"Retuned audio saved as: {output_audio}")
    print("\nOverstimulating segments detection completed. Results:")
    for segment in processed_segments:
        print(segment)

def attach_audio_to_video(input_video, output_audio, output_video):

    video = mp.VideoFileClip(input_video)
    audio = mp.AudioFileClip(output_audio)

    # Fix: Use with_audio() instead of set_audio()
    video = video.with_audio(audio)

    video.write_videofile(output_video, codec="libx264", audio_codec="aac")

# Example usage
json_file = "overstimulating_segments.json"  # JSON file storing detected overstimulating time ranges
input_audio = "extracted_audio_boosted.mp3"  # Input MP3 file
output_audio = "retuned_audio.mp3"  # Output MP3 file
input_video = "oggy-test.mp4"  # Input video file
output_video = "retuned_video.mp4"  # Output video file

overstim_segments = load_overstim_segments(json_file)
retune_audio(input_audio, output_audio, overstim_segments)
attach_audio_to_video(input_video, output_audio, output_video)
