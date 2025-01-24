from moviepy import VideoFileClip

# Define the input video file and output audio file
mp4_file = "sampleAudios/sampleVideo.mp4"
mp3_file = "sampleAudio.mp3"

# Load the video clip
video_clip = VideoFileClip(mp4_file)

# Extract the audio from the video clip
audio_clip = video_clip.audio

# Write the audio to a separate file
audio_clip.write_audiofile(mp3_file)

# Close the v   ideo and audio clips
audio_clip.close()
video_clip.close()

print("Audio extraction successful!")