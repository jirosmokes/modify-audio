import json
import librosa
import soundfile as sf
import numpy as np
from moviepy import VideoFileClip, AudioFileClip  # Fixed import
from scipy.signal import butter, lfilter

def load_overstim_segments(json_file):
    """Loads detected overstimulating segments from a JSON file."""
    try:
        with open(json_file, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        exit(1)

def butter_filter(data, cutoff, fs, order=8, filter_type="low"):
    """Applies a Butterworth filter to reduce unwanted frequencies."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
    return lfilter(b, a, data)

def reduce_loudness(audio, factor=0.1):
    """Reduces loudness by scaling amplitude."""
    return audio * factor

def fade_audio(audio, fade_length):
    """Applies a fade-in and fade-out effect."""
    fade = np.linspace(0, 1, fade_length)
    audio[:fade_length] *= fade  # Fade-in
    audio[-fade_length:] *= fade[::-1]  # Fade-out
    return audio

def compress_audio(audio):
    """Applies dynamic range compression to balance loudness."""
    return np.tanh(audio * 2.5)  # Adjusted to prevent excessive distortion

def retune_audio(input_audio, output_audio, overstim_segments):
    """Processes and retunes only overstimulating segments."""
    y, sr = librosa.load(input_audio, sr=44100)

    processed_segments = []
    for segment in overstim_segments:
        try:
            start_time = float(segment.get("start_time", 0))
            end_time = float(segment.get("end_time", 0))
            segment_file = segment.get("segment", "Unknown")
            overstim_status = segment.get("overstimulating", False)

            if end_time > start_time:
                start_sample = int(start_time * sr)
                end_sample = int(end_time * sr)
                segment_audio = y[start_sample:end_sample].copy()

                if overstim_status:
                    # Apply filtering
                    segment_audio = butter_filter(segment_audio, cutoff=1500, fs=sr, filter_type="low")
                    segment_audio = butter_filter(segment_audio, cutoff=400, fs=sr, filter_type="high")

                    # Apply loudness reduction, fade, and compression
                    segment_audio = reduce_loudness(segment_audio, factor=0.1)
                    fade_length = min(int(0.75 * sr), len(segment_audio) // 2)  # Avoid out-of-bounds errors
                    segment_audio = fade_audio(segment_audio, fade_length)
                    segment_audio = compress_audio(segment_audio)

                    processed_segments.append(f"Segment: {segment_file}, Time: {start_time:.1f} - {end_time:.1f}s, Overstimulating: True")

                # Replace only the segment in the main audio (unmodified if not overstimulating)
                y[start_sample:end_sample] = segment_audio

        except Exception as e:
            print(f"Skipping segment due to error: {e}")

    sf.write(output_audio, y, sr)
    print(f"✅ Retuned audio saved as: {output_audio}")

    print("\n📌 Processed Overstimulating Segments:")
    for segment in processed_segments:
        print(segment)

def attach_audio_to_video(input_video, output_audio, output_video):
    """Attaches retuned audio to video."""
    try:
        video = VideoFileClip(input_video)
        audio = AudioFileClip(output_audio)

        video = video.with_audio(audio)
        video.write_videofile(output_video, codec="libx264", audio_codec="aac")

        print(f"✅ Retuned video saved as: {output_video}")
    except Exception as e:
        print(f"Error processing video: {e}")

# # Example usage
# json_file = "overstimulating_segments.json"
# input_audio = "extracted_audio_boosted.mp3"
# output_audio = "retuned_audio.mp3"
# input_video = "test-videos/tom-test.mp4"
# output_video = "tom-retuned.mp4"
#
# overstim_segments = load_overstim_segments(json_file)
# retune_audio(input_audio, output_audio, overstim_segments)
# attach_audio_to_video(input_video, output_audio, output_video)
