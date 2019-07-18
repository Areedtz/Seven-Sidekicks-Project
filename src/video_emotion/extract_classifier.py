import sys
from typing import Dict

from video_emotion.facial_recognition.facial_recognition import analyze_video
from video_emotion.emotionTagger.face_emotion_extraction import classify_faces


def classify_video(video_path: str, time_range=None):
    """Classifies the emotions in a given video

    Parameters
    ----------
    video_path:str
        The path of the video that is to be analyzed

    time_range:Dict[str:int]
        The time range to analyze in as a dictionary of type string:int

    Returns
    -------
    string
        Returns a csv of the emotions in the emotion set
    """

    faces = analyze_video(video_path, time_range)
    angry_sum =\
        disgust_sum =\
        fear_sum =\
        happy_sum =\
        sad_sum =\
        surprise_sum =\
        neutral_sum = 0.0
    number_of_faces = 0
    realFaces = []
    for key, value in faces.items():
        for face in value:
            realFaces.append(face)
    faces = classify_faces(realFaces)

    for emotions in faces:
        angry_sum += emotions[0]
        disgust_sum += emotions[1]
        fear_sum += emotions[2]
        happy_sum += emotions[3]
        sad_sum += emotions[4]
        surprise_sum += emotions[5]
        neutral_sum += emotions[6]
        number_of_faces = number_of_faces + 1

    return {
        "angry": angry_sum / number_of_faces,
        "disgust": disgust_sum / number_of_faces,
        "fear": fear_sum / number_of_faces,
        "happy": happy_sum / number_of_faces,
        "sad": sad_sum / number_of_faces,
        "surprise": surprise_sum / number_of_faces,
        "neutral": neutral_sum / number_of_faces
    }


def find_emotions_cutoffs(emotions: [float]) -> str:
    """Finds the emotional cutoffs for a set of emotions as a list

    Parameters
    ----------
    emotions:str
        An array of emotions

    Returns
    -------
    string
        Returns the cutoffs underscore-separated with the id first
    """

    emotions2 = {
        "angry": emotions[0],
        "disgust": emotions[1],
        "fear": emotions[2],
        "happy": emotions[3],
        "sad": emotions[4],
        "surprise": emotions[5],
        "neutral": emotions[6]
    }

    string = ""
    for key, value in emotions2.items():
        if value > 0.3:
            string = string + key + "_" + str(value.round(decimals=2)) + "_"

    return string
