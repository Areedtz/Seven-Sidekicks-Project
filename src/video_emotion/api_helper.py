from typing import Dict

from video_emotion.extract_classifier import classify_video
from database.mongo.video.video_emotion_no_song import VideoEmotionNS
from database.mongo.video.video_emotion import VideoEmotion


def process_data_and_extract_emotions(video_id: str, video_path: str, time_range:Dict[str,int]) -> bool:
    """Classifies the emotions in the given video

    Parameters
    ----------
    video_id: str
        The id of the video to analyze

    video_path: str
        The path of the video that is to be analyzed

    time_range:Dict[str,int]
        The time range as a dictionary to analyze

    Returns
    -------
    bool
        The boolean describing whether it succeeded
    """

    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = VideoEmotionNS()
    vet.add(video_id, time_range, data)
    return True


def process_data_and_extract_emotions_with_song(video_id: str, video_path: str,
                                                time_range: Dict[str, int],
                                                song_id: str) -> bool:
    """Classifies the emotions in a video and places
    it in the database with a songid

    Parameters
    ----------
    video_id: str
        The id of the video to analyze

    video_path: str
        The path of the video that is to be analyzed

    time_range: Dict[str,int]
        The time range as a dictionary to analyze

    song_id:str
        The song to associate the video with

    Returns
    -------
    bool
        Returns a boolean telling if the function succeeded
    """

    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = VideoEmotion()
    vet.add(video_id, song_id, time_range, data)
    return True
