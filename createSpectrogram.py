import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def generate_spectrograms(input_directory, output_directory, img_size=(224, 224)):
    """
    Generate spectrogram images from MP3 files and save them in the specified output directory.

    Args:
        input_directory (str): The directory containing MP3 files to process.
        output_directory (str): The directory where the spectrogram images will be saved.
        img_size (tuple): The target size for the spectrogram images (default is 224x224).
    """
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Process each MP3 file recursively
    for subdir, _, files in os.walk(input_directory):
        relative_path = os.path.relpath(subdir, input_directory)
        output_subdir = os.path.join(output_directory, relative_path)
        os.makedirs(output_subdir, exist_ok=True)  # Create corresponding output folder

        for filename in files:
            if filename.endswith(".mp3"):
                file_path = os.path.join(subdir, filename)

                # Load audio file
                y, sr = librosa.load(file_path, sr=None)

                # Compute STFT spectrogram
                D = np.abs(librosa.stft(y))

                # Create figure
                fig, ax = plt.subplots(figsize=(5, 5), dpi=100)

                # Display spectrogram
                img = librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr, cmap='magma', ax=ax)

                # Remove axis and padding
                ax.axis("off")
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

                # Save spectrogram
                temp_output_file = os.path.join(output_subdir, f"{os.path.splitext(filename)[0]}_spectrogram_temp.png")
                fig.savefig(temp_output_file, transparent=True)
                plt.close(fig)

                # Resize to target size (224x224) and remove transparency
                img = Image.open(temp_output_file).convert("RGB")
                img = img.resize(img_size, Image.LANCZOS)
                final_output_file = os.path.join(output_subdir, f"{os.path.splitext(filename)[0]}_spectrogram.png")
                img.save(final_output_file)
                os.remove(temp_output_file)  # Remove temporary image

                print(f"✅ Saved spectrogram: {final_output_file}")

    print("🎉 Spectrogram generation completed!")


# Example usage
input_directory = "preprocessed_dataset"  # Source folder (MP3 files in subdirectories)
output_directory = "spectrogram_dataset"  # Destination folder
generate_spectrograms(input_directory, output_directory)
