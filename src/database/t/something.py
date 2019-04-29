import datetime

from database.storinator import Storinator
from database.video_emotion_no_song import VideoEmotionNS

def test_all_same_id():
    vet = VideoEmotionNS()

    d11 = {
        "from1" : 3000,
        "to1" : 4000,
    }
    
    d12 = {
        "angry": 0.98,
        "disgust": 0.70,
        "fear": 0.3,
        "happy": 0.2,
        "sad": 0.5,
        "surprise": 0.7,
        "neutral": 0.99
    }

    d21 = {
        "from1" : 3000,
        "to1" : 4000,
    }

    d22 = {
        "angry": 0.3,
        "disgust": 0.20,
        "fear": 0.6,
        "happy": 0.7,
        "sad": 0.1,
        "surprise": 0.234,
        "neutral": 0.43
    }
    vet.add(1, d11, d12)
    vet.add(1, d21, d22)

    something = vet.get_all_same_id(1)
    print(something)

test_all_same_id()
