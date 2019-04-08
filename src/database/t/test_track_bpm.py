from database.track_bpm import TrackBPM
from database.storinator import Storinator
import datetime


def test_implements_Storinator():
    tbpm = TrackBPM()
    assert isinstance(tbpm, Storinator)


def test_database_name():
    tbpm = TrackBPM()
    assert tbpm._dbname == 'track_bpm'


def test_add_and_get():
    tbpm = TrackBPM()
    tbpm.add(1, 100., 3.)
    track = tbpm.get(1)
    assert track['song_id'] == 1
    assert track['bpm'] == 100.
    assert track['confidence'] == 3.


def test_get_all():
    tbpm = TrackBPM()
    tbpm.add(1, 100., 3.)
    tracks = tbpm.get_all()
    assert len(tracks) > 0
