import json
import os

from video_emotion.extract_classifier import classify_video
from database.video_emotion_no_song import VideoEmotion2 as vid_emote_song
from database.video_emotion import VideoEmotion

def process_data_and_extract_emotions(video_id, video_path, time_range):
    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = vid_emote_song()
    vet.add(video_id, data)
    return True


def process_data_and_extract_emotions_with_song(video_id, video_path, time_range,songID):
    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = VideoEmotion()
    vet.add(video_id, songID, data)
    return True