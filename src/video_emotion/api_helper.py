import json
import os

from video_emotion.extract_classifier import classify_video
from database.video_emotion_no_song import VideoEmotion2

def process_data_and_extract_emotions(video_id, video_path, time_range, output_file_path):
    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = VideoEmotion2()
    vet.add(video_id, data)
    return True
