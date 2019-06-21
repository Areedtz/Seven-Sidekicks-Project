import datetime
from database.mongo.audio.track_emotion import TrackEmotion
from database.mongo.storinator import Storinator


def test_implements_Storinator():
    temo = TrackEmotion()

    assert isinstance(temo, Storinator)


def test_database_name():
    temo = TrackEmotion()

    assert temo._col == 'track_emotion'


def test_add_and_get():
    temo = TrackEmotion()
    temo.add("1",
             {
                 'bpm':
                 {
                     'value': 100.0,
                     'confidence': 3.0
                 },
                 'timbre':
                 {
                     'value': 'bright',
                     'confidence': 0.79
                 },
                 'relaxed':
                 {
                     'value': 'relaxed',
                     'confidence': 0.82
                 },
                 'party':
                 {
                     'value': 'party',
                     'confidence': 0.9
                 },
                 'aggressive':
                 {
                     'value': 'aggressive',
                     'confidence': 0.84
                 },
                 'happy':
                 {
                     'value': 'happy',
                     'confidence': 0.56
                 },
                 'sad':
                 {
                     'value': 'sad',
                     'confidence': 0.68
                 }
             }
             )
    track = temo.get("1")

    assert track['song_id'] == "1"
    assert track['bpm']['value'] == 100.0
    assert track['bpm']['confidence'] == 3.0
    assert track['timbre']['value'] == 'bright'
    assert track['timbre']['confidence'] == 0.79
    assert track['relaxed']['value'] == 'relaxed'
    assert track['relaxed']['confidence'] == 0.82
    assert track['party']['value'] == 'party'
    assert track['party']['confidence'] == 0.9
    assert track['aggressive']['value'] == 'aggressive'
    assert track['aggressive']['confidence'] == 0.84
    assert track['happy']['value'] == 'happy'
    assert track['happy']['confidence'] == 0.56
    assert track['sad']['value'] == 'sad'
    assert track['sad']['confidence'] == 0.68


def test_get_all():
    temo = TrackEmotion()
    temo.add("1",
             {
                 'bpm':
                 {
                     'value': 100.0,
                     'confidence': 3.0
                 },
                 'timbre':
                 {
                     'value': 'bright',
                     'confidence': 0.79
                 },
                 'relaxed':
                 {
                     'value': 'relaxed',
                     'confidence': 0.82
                 },
                 'party':
                 {
                     'value': 'party',
                     'confidence': 0.9
                 },
                 'aggressive':
                 {
                     'value': 'aggressive',
                     'confidence': 0.84
                 },
                 'happy':
                 {
                     'value': 'happy',
                     'confidence': 0.56
                 },
                 'sad':
                 {
                     'value': 'sad',
                     'confidence': 0.68
                 }

             }
             )
    tracks = temo.get_all()

    assert len(tracks) > 0

