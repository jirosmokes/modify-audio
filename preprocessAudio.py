import os
from pydub import AudioSegment


def load_audio(file_path):
    """
    Load an MP3 audio file into a PyDub AudioSegment.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return None
    return AudioSegment.from_mp3(file_path)


def boost_volume(audio_segment, gain_db=10):
    """
    Boost the volume of the audio by a specified number of decibels.
    """
    return audio_segment + gain_db


def preprocess_audio(input_file, output_folder):
    """
    Preprocess an audio file by boosting volume only (no filters applied).
    The processed file is saved with "-preprocessed" appended to the filename.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output directory if it doesn't exist

    audio = load_audio(input_file)
    if audio is None:
        return

    # Boost volume
    audio = boost_volume(audio, gain_db=15)

    # Get the base filename and append "-preprocessed"
    file_name = os.path.basename(input_file)
    file_name_without_ext = os.path.splitext(file_name)[0]
    output_file = os.path.join(output_folder, f"{file_name_without_ext}-preprocessed.mp3")

    # Export the processed audio
    audio.export(output_file, format="mp3")
    print(f"Processed audio saved to {output_file}")


def process_dataset(input_folder, output_folder):
    """
    Process all audio files in the input folder and save the preprocessed files to the output folder.
    """
    for subfolder in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subfolder)
        if os.path.isdir(subfolder_path):
            output_subfolder = os.path.join(output_folder, subfolder)
            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)  # Create subfolder in output if it doesn't exist

            for file_name in os.listdir(subfolder_path):
                if file_name.endswith(".mp3"):
                    input_file = os.path.join(subfolder_path, file_name)
                    preprocess_audio(input_file, output_subfolder)


input_folder = "new_dataset"  # Folder with 5 subfolders
output_folder = "preprocessed_dataset"  # Folder to save preprocessed files

    # Process the dataset
process_dataset(input_folder, output_folder)