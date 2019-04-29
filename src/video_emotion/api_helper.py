import json
import os

from video_emotion.extract_classifier import classify_video
from database.video_emotion_no_song import VideoEmotionNS
from database.video_emotion import VideoEmotion

def process_data_and_extract_emotions(video_id, video_path, time_range):
    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = VideoEmotionNS()
    vet.add(video_id, time_range, data)
    return True


def process_data_and_extract_emotions_with_song(video_id, video_path, time_range, song_id):
    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = VideoEmotion()
    vet.add(video_id, song_id, time_range, data)
    return True