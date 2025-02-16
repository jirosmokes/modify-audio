import os

# Set the parent directory containing multiple folders
parent_directory = "raw_dataset"  # Change this to your actual parent directory

# Allowed folder names
allowed_folders = {"Chaotic", "High Frequency", "High Intensity", "Abrupt", "Repetitive"}

# Loop through each folder inside the parent directory
for folder_name in os.listdir(parent_directory):
    folder_path = os.path.join(parent_directory, folder_name)

    # Check if it's a directory and in the allowed list
    if not os.path.isdir(folder_path) or folder_name not in allowed_folders:
        continue

    # Get all files in the folder and sort them
    files = sorted(os.listdir(folder_path))

    # Initialize counter
    counter = 1

    # Rename each file inside the folder
    for file_name in files:
        old_path = os.path.join(folder_path, file_name)

        # Skip directories inside the folder
        if os.path.isdir(old_path):
            continue

        # Get file extension
        file_extension = os.path.splitext(file_name)[1]

        # Generate the expected correct filename
        correct_name = f"{folder_name}-{counter}{file_extension}"
        new_path = os.path.join(folder_path, correct_name)

        # Skip renaming if the filename is already correct
        if file_name == correct_name:
            print(f"Skipping (already correctly named): {file_name}")
            counter += 1
            continue

        # Handle potential file conflicts
        if os.path.exists(new_path):
            print(f"Error: {new_path} already exists! Skipping {file_name}.")
            continue

        # Rename the file
        try:
            os.rename(old_path, new_path)
            print(f'Renamed: {file_name} -> {correct_name}')
        except Exception as e:
            print(f"Error renaming {file_name}: {e}")

        counter += 1

print("Renaming completed for specified folders!")
