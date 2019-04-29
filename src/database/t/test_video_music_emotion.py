import datetime

from database.storinator import Storinator
from database.video_music_emotion import VideoMusicEmotion

# vet = Video Emotion Test

def test_implements_Storinator():
    vet = VideoMusicEmotion()
    assert isinstance(vet, Storinator)


def test_database_name():
    vet = VideoMusicEmotion()
    assert vet._dbname == 'video_music_emotion'


def test_add_and_get():
    vet = VideoMusicEmotion()

    time = {
        'from1' : 3000,
        'to1' : 4000
    }
    
    bpm = {
        'bpm': 180,
        'bpm_confidence': 3
    }

    timbre = {
        'timbre': 'bright',
        'timbre_confidence': 4
    }

    party = {
        'party': 'party',
        'party_confidence': 20
    }

    relaxed = {
        'relaxed': 'relaxed',
        'relaxed_confidence': 9
    }

    emo = {
        "angry": 0.98,
        "disgust": 0.70,
        "fear": 0.3,
        "happy": 0.2,
        "sad": 0.5,
        "surprise": 0.7,
        "neutral": 0.99
    }

    vet.add(1, 2, bpm, timbre, party, relaxed, time, emo)
    ve = vet.get(1, 2)
    assert ve['song_id'] == 1
    assert ve['video_id'] == 2
    assert ve['from1'] == 3000
    assert ve['to1'] == 4000
    assert ve['angry'] == 0.98
    assert ve['disgust'] == 0.70
    assert ve['fear'] == 0.3
    assert ve['happy'] == 0.2
    assert ve['sad'] == 0.5
    assert ve['surprise'] == 0.7
    assert ve['relaxed'] == 'relaxed'
    assert ve['bpm'] == 180
    assert ve['bpm_confidence'] == 3
    assert ve['timbre'] == 'bright'
    assert ve['party_confidence'] == 20