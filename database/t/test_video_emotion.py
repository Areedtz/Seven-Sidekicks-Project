import datetime

from database.storinator import Storinator
from database.video_emotion import VideoEmotion

# vet = Video Emotion Test

def test_implements_Storinator():
    vet = VideoEmotion()
    assert isinstance(vet, Storinator)


def test_database_name():
    vet = VideoEmotion()
    assert vet._dbname == 'video_emotion'


def test_add_and_get():
    vet = VideoEmotion()
    d = {
        "angry": 0.98,
        "disgust": 0.70,
        "fear": 0.3,
        "happy": 0.2,
        "sad": 0.5,
        "surprise": 0.7,
        "neutral": 0.99
    }
    vet.add(1, 2, d)
    ve = vet.get(1, 2)
    assert ve['song_id'] == 1
    assert ve['video_id'] == 2
    assert ve['angry'] == 0.98
    assert ve['disgust'] == 0.70
    assert ve['fear'] == 0.3
    assert ve['happy'] == 0.2
    assert ve['sad'] == 0.5
    assert ve['surprise'] == 0.7
    assert ve['neutral'] == 0.99



def test_get_all():
    vet = VideoEmotion()
    d1 = {
        "angry": 0.98,
        "disgust": 0.70,
        "fear": 0.3,
        "happy": 0.2,
        "sad": 0.5,
        "surprise": 0.7,
        "neutral": 0.99
    }
    d2 = {
        "angry": 0.3,
        "disgust": 0.20,
        "fear": 0.6,
        "happy": 0.7,
        "sad": 0.1,
        "surprise": 0.234,
        "neutral": 0.43
    }
    vet.add(1, 2, d1)
    vet.add(2, 3, d2)

    vet1 = vet.get(1,2)
    vet2 = vet.get(2,3)
    vets = vet.get_all()

    assert len(vets) > 0

    assert vet1['song_id'] == 1
    assert vet1['video_id'] == 2
    assert vet1['angry'] == 0.98
    assert vet1['disgust'] == 0.70

    assert vet2['song_id'] == 2
    assert vet2['video_id'] == 3
    assert vet2['sad'] == 0.1
    assert vet2['surprise'] == 0.234
    assert vet2['neutral'] == 0.43
