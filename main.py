# final_mvp.py
import cv2
from pydub import AudioSegment
import subprocess

# 1️⃣ Extract audio from video
video_file = "carvideo.mp4"
audio_file = "caraudio.wav"
output_audio_file = "panned_audio.wav"
output_video_file = "output_video.mp4"

video_audio = AudioSegment.from_file(video_file, format="mp4")
video_audio.export(audio_file, format="wav")
print("Audio extracted successfully!")

# 2️⃣ Detect car position (simple color threshold for test video)
cap = cv2.VideoCapture(video_file)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

x_positions = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Simple detection: adjust thresholds if needed
    mask = cv2.inRange(frame, (0,0,100), (80,80,255))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        center_x = x + w/2
        normalized_x = center_x / width
        x_positions.append(normalized_x)
    else:
        x_positions.append(0.5)  # default center

cap.release()
print("Car positions detected!")

# 3️⃣ Apply stereo panning based on detected positions
sound = AudioSegment.from_file(audio_file, format="wav")
duration_ms = len(sound)
segment_length = duration_ms / len(x_positions)

output = AudioSegment.silent(duration=0)

for i, x in enumerate(x_positions):
    start = int(i * segment_length)
    end = int((i+1) * segment_length)
    segment = sound[start:end].set_channels(1)
    
    left_vol = 1 - x
    right_vol = x
    left = segment.apply_gain(left_vol * 10 - 10)
    right = segment.apply_gain(right_vol * 10 - 10)
    stereo_segment = AudioSegment.from_mono_audiosegments(left, right)
    output += stereo_segment

output.export(output_audio_file, format="wav")
print("Stereo panning applied!")

# 4️⃣ Merge panned audio back into video
cmd = [
    "ffmpeg",
    "-i", video_file,
    "-i", output_audio_file,
    "-c:v", "copy",
    "-map", "0:v:0",
    "-map", "1:a:0",
    output_video_file
]

subprocess.run(cmd)
print(f"Final video created: {output_video_file}")
