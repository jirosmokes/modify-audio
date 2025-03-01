from moviepy import VideoFileClip, AudioFileClip
import os
from pydub import AudioSegment
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def extract_audio(mp4_path, output_mp3):
    """Extracts audio from an MP4 file and saves it as an MP3."""
    with VideoFileClip(mp4_path) as video_clip:
        with video_clip.audio as audio_clip:
            audio_clip.write_audiofile(output_mp3)
    print(f"Extracted audio saved: {output_mp3}")


def boost_volume(input_mp3, output_mp3, gain_db=20):
    """Boosts the volume of an MP3 file."""
    audio = AudioSegment.from_mp3(input_mp3) + gain_db
    audio.export(output_mp3, format="mp3")
    print(f"Boosted audio saved: {output_mp3}")


def generate_full_spectrogram(input_mp3, output_img):
    """Generates the full spectrogram from the boosted MP3 file and saves it."""
    y, sr = librosa.load(input_mp3, sr=None)
    D = np.abs(librosa.stft(y))
    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr, cmap='magma', ax=ax)
    ax.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(output_img, transparent=True)
    plt.close(fig)
    print(f"Full spectrogram saved: {output_img}")


def segment_spectrogram(input_mp3, output_folder, segment_length=4, img_size=(224, 224)):
    """Segments the spectrogram into chunks of 4 seconds and saves each as a resized image."""
    y, sr = librosa.load(input_mp3, sr=None)
    segment_samples = int(segment_length * sr)
    num_segments = len(y) // segment_samples

    for i in range(num_segments + 1):
        start = i * segment_samples
        end = start + segment_samples
        if start >= len(y):
            break

        segment = y[start:end]
        D = np.abs(librosa.stft(segment))
        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
        librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr, cmap='magma', ax=ax)
        ax.axis("off")
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        temp_output = os.path.join(output_folder, f"segment_{i}.png")
        fig.savefig(temp_output, transparent=True)
        plt.close(fig)

        img = Image.open(temp_output).convert("RGB").resize(img_size, Image.LANCZOS)
        img.save(temp_output)
        print(f"Segment {i} spectrogram saved: {temp_output}")


def attach_boosted_audio(mp4_path, boosted_mp3, output_mp4):
    """Attaches the boosted audio back to the original video."""
    with VideoFileClip(mp4_path) as video_clip:
        new_audio = AudioFileClip(boosted_mp3)
        final_video = video_clip.with_audio(new_audio)
        final_video.write_videofile(output_mp4, codec="libx264", audio_codec="aac")
    print(f"Final video with boosted audio saved: {output_mp4}")


def process_video(mp4_path, output_mp3, full_spectrogram_img, output_folder, output_mp4):
    """Extracts, boosts, generates spectrograms, and reattaches boosted audio to the video."""
    extract_audio(mp4_path, output_mp3)
    boosted_mp3 = output_mp3.replace(".mp3", "_boosted.mp3")
    boost_volume(output_mp3, boosted_mp3)
    generate_full_spectrogram(boosted_mp3, full_spectrogram_img)
    segment_spectrogram(boosted_mp3, output_folder)
    attach_boosted_audio(mp4_path, boosted_mp3, output_mp4)
    return boosted_mp3, full_spectrogram_img, output_mp4


# # Example usage
# # Define file paths
# mp4_file = "test-videos/tom-test.mp4"  # Replace with your video file path
# output_mp3 = "extracted_audio.mp3"
# full_spectrogram_img = "full_spectrogram.png"
# output_segments_folder = "spectrogram_segments"
# output_mp4 = "test-videos/tom-test-boosted.mp4"
#
# # Ensure the output folder exists
# if not os.path.exists(output_segments_folder):
#     os.makedirs(output_segments_folder)
#
# # Process the video
# boosted_audio, full_spectrogram, final_video = process_video(mp4_file, output_mp3, full_spectrogram_img,
#                                                              output_segments_folder, output_mp4)
#
# print("Processing complete!")
# print(f"Boosted Audio: {boosted_audio}")
# print(f"Full Spectrogram: {full_spectrogram}")
# print(f"Segmented Spectrograms saved in: {output_segments_folder}")
# print(f"Final Video with Boosted Audio: {final_video}")
