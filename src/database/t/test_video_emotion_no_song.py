import datetime


from database.storinator import Storinator
from database.video_emotion_no_song import VideoEmotionNS


# vet = Video Emotion Test
def test_implements_Storinator():
    vet = VideoEmotionNS()
    assert isinstance(vet, Storinator)


def test_database_name():
    vet = VideoEmotionNS()
    assert vet._dbcol == 'video_emotion_no_song'


def test_add_and_get():
    vet = VideoEmotionNS()

    timerange = {
        "from1" : 3000,
        "to1" : 4000,
    }

    emotions = {
        "angry": 0.98,
        "disgust": 0.70,
        "fear": 0.3,
        "happy": 0.2,
        "sad": 0.5,
        "surprise": 0.7,
        "neutral": 0.99
    }
    vet.add(1, timerange, emotions)

    ve = vet.get(1)
    assert ve['video_id'] == 1
    assert ve['from1'] == 3000
    assert ve['to1'] == 4000
    assert ve['angry'] == 0.98
    assert ve['disgust'] == 0.70
    assert ve['fear'] == 0.3
    assert ve['happy'] == 0.2
    assert ve['sad'] == 0.5
    assert ve['surprise'] == 0.7
    assert ve['neutral'] == 0.99

def test_all_same_id():
    vet = VideoEmotionNS()

    timerange1 = {
        "from1" : 3000,
        "to1" : 4000,
    }
    
    emotions1 = {
        "angry": 0.98,
        "disgust": 0.70,
        "fear": 0.3,
        "happy": 0.2,
        "sad": 0.5,
        "surprise": 0.7,
        "neutral": 0.99
    }

    timerange2 = {
        "from1" : 4000,
        "to1" : 5000,
    }

    emotions2 = {
        "angry": 0.3,
        "disgust": 0.20,
        "fear": 0.6,
        "happy": 0.7,
        "sad": 0.1,
        "surprise": 0.234,
        "neutral": 0.43
    }
    vet.add(1000, timerange1, emotions1)
    vet.add(1000, timerange2, emotions2)

    all_id_1 = vet.get_by_video_id(1000)
    assert len(all_id_1) > 0


def test_find_by_video_id():
    vet = VideoEmotionNS()

    timerange1 = {
        "from1" : 3000,
        "to1" : 4000,
    }
    
    emotions1 = {
        "angry": 0.98,
        "disgust": 0.70,
        "fear": 0.3,
        "happy": 0.2,
        "sad": 0.5,
        "surprise": 0.7,
        "neutral": 0.99
    }

    timerange2 = {
        "from1" : 3000,
        "to1" : 4000,
    }

    emotions2 = {
        "angry": 0.3,
        "disgust": 0.20,
        "fear": 0.6,
        "happy": 0.7,
        "sad": 0.1,
        "surprise": 0.234,
        "neutral": 0.43
    }
    vet.add(1, timerange1, emotions1)
    vet.add(2, timerange2, emotions2)

    vet1 = vet.get(1)
    vet2 = vet.get(2)
    vets = vet.get_all()

    assert len(vets) > 0

    assert vet1['video_id'] == 1
    assert vet1['angry'] == 0.98
    assert vet1['disgust'] == 0.70

    assert vet2['video_id'] == 2
    assert vet2['sad'] == 0.1
    assert vet2['surprise'] == 0.234
    assert vet2['neutral'] == 0.43
    
