from moviepy import VideoFileClip
import os

# Define category folders
categories = ["Chaotic", "High Frequency", "High Intensity", "Abrupt", "Repetitive", "Non-Overstimulating"]

# Base directories
raw_dataset_folder = os.path.join(os.getcwd(), "raw_dataset")
new_dataset_folder = os.path.join(os.getcwd(), "new_dataset")


def ensure_folder_exists(folder_path):
    """Creates a folder if it does not exist."""
    os.makedirs(folder_path, exist_ok=True)


# Create the new_dataset directory
ensure_folder_exists(new_dataset_folder)


def extract_audio_batch():
    """Extracts audio from MP4 files in each category folder and saves them in 'new_dataset'."""

    for category in categories:
        category_path = os.path.join(raw_dataset_folder, category)
        output_category_path = os.path.join(new_dataset_folder, category)
        ensure_folder_exists(output_category_path)  # Ensure the category folder exists in new_dataset

        if not os.path.exists(category_path):
            print(f"Warning: {category_path} does not exist. Skipping...")
            continue

        extracted_files = []

        for filename in os.listdir(category_path):
            if filename.endswith(".mp4"):
                mp4_file = os.path.join(category_path, filename)
                audio_file = os.path.join(output_category_path, os.path.splitext(filename)[0] + ".mp3")

                try:
                    with VideoFileClip(mp4_file) as video_clip:
                        with video_clip.audio as audio_clip:
                            audio_clip.write_audiofile(audio_file)

                    extracted_files.append(audio_file)
                    print(f"Extracted audio saved: {audio_file}")

                except Exception as e:
                    print(f"Error extracting audio from {filename}: {e}")


def remove_audio_batch():
    """Removes audio from MP4 files in each category folder and saves them in 'new_dataset'."""

    for category in categories:
        category_path = os.path.join(raw_dataset_folder, category)
        output_category_path = os.path.join(new_dataset_folder, category)
        ensure_folder_exists(output_category_path)  # Ensure the category folder exists in new_dataset

        if not os.path.exists(category_path):
            print(f"Warning: {category_path} does not exist. Skipping...")
            continue

        processed_files = []

        for filename in os.listdir(category_path):
            if filename.endswith(".mp4"):
                mp4_file = os.path.join(category_path, filename)
                video_without_audio_file = os.path.join(output_category_path, filename)

                try:
                    with VideoFileClip(mp4_file) as video_clip:
                        video_without_audio = video_clip.without_audio()
                        video_without_audio.write_videofile(video_without_audio_file, codec='libx264', audio=False)

                    processed_files.append(video_without_audio_file)
                    print(f"Processed video without audio saved: {video_without_audio_file}")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")


# Run the functions
extract_audio_batch()
# remove_audio_batch()