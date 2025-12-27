ffmpeg -i carvideo.mp4 -i panned_audio.wav -c:v copy -map 0:v:0 -map 1:a:0 output_video.mp4
