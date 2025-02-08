from moviepy import VideoFileClip, AudioFileClip
import os


def extract_audio(mp4_file, audio_output_folder, audio_file):
    try:
        # Ensure the audio output folder exists
        if not os.path.exists(audio_output_folder):
            os.makedirs(audio_output_folder)

        # Load the video clip
        video_clip = VideoFileClip(mp4_file)

        # Extract the audio from the video clip
        audio_clip = video_clip.audio

        # Write the audio to the specified file
        audio_clip.write_audiofile(audio_file)

        # Close the video and audio clips
        audio_clip.close()
        video_clip.close()

        return audio_file  # Return the extracted audio file path
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None

def create_video_without_audio(mp4_file, video_output_folder, video_without_audio_file):
    try:
        # Ensure the video output folder exists
        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        # Load the original video clip
        video_clip = VideoFileClip(mp4_file)

        # Remove the audio from the video
        video_without_audio = video_clip.without_audio()

        # Write the final video without audio to the output file
        video_without_audio.write_videofile(video_without_audio_file, codec='libx264', audio=False)

        # Close the video clip
        video_clip.close()

        return video_without_audio_file  # Return the path to the video without audio
    except Exception as e:
        print(f"Error creating video without audio: {e}")
        return None