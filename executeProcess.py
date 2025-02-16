from extractAudio import extract_audio_batch
from preprocessAudio import process_dataset
from extractAudioFeatures import ensure_folder_exists, plot_audio_features
from createSpectrogram import generate_spectrograms

# extract audio -> preprocess -> plot audio features -> convert spectrogram

nD_folder = "new_dataset"  # Folder with 5 subfolders
pD_folder = "preprocessed_dataset"  # Folder to save preprocessed files
vD_folder = "visualized_dataset"
sD_folder = "spectrogram_dataset"

extract_audio_batch() # step 1
process_dataset(nD_folder, pD_folder) # step 2
ensure_folder_exists(vD_folder) # check
plot_audio_features(pD_folder, vD_folder) # step 3
generate_spectrograms(pD_folder, sD_folder) # step 4