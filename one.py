from pydub import AudioSegment

# Load MP4 video file (pydub uses ffmpeg)
video = AudioSegment.from_file("carvideo.mp4", format="mp4")

# Export audio to WAV (or MP3)
video.export("caraudio.wav", format="wav")
print("Audio extracted successfully!")
