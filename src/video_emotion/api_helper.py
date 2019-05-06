from typing import Dict

from video_emotion.extract_classifier import classify_video
from database.video_emotion_no_song import VideoEmotionNS
from database.video_emotion import VideoEmotion


def process_data_and_extract_emotions(video_id: int, video_path: str, time_range:Dict[str,int]) -> bool:
    """Clasifies the emotions in a video

    Parameters
    ----------
    video_id
        The id of the video to analyze

    video_path
        The path of the video that is to be analyzed

    time_range
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


def process_data_and_extract_emotions_with_song(video_id, video_path, 
                                                time_range, song_id):
    """Clasifies the emotions in a video and places it in the database with a songid

        Parameters
        ----------
        video_id
            The id of the video to analyze

        video_path
            The path of the video that is to be analyzed

        time_range
            The time range as a dictionary to analyze

        song_id
            The song to associate the video with

        Returns
        -------
        string
            Returns a csv of the emotions in the emotion set
        """

    data = classify_video(video_path, (time_range['From'], time_range['To']))
    vet = VideoEmotion()
    vet.add(video_id, song_id, time_range, data)
    return True