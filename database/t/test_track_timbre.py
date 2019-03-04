from database.track_timbre import TrackTimbre
from database.storinator import Storinator
import datetime


def test_implements_Storinator():
    tbpm = TrackTimbre()
    assert isinstance(tbpm, Storinator)


def test_database_name():
    tbpm = TrackTimbre()
    assert tbpm._dbname == 'track_timbre'


def test_add_and_get():
    tbpm = TrackTimbre()
    tbpm.add(1, 'bright', .79)
    track = tbpm.get(1)
    assert track['song_id'] == 1
    assert track['timbre'] == 'bright'
    assert track['confidence'] == .79


def test_get_all():
    tbpm = TrackTimbre()
    tbpm.add(1, 'bright', .79)
    tracks = tbpm.get_all()
    assert len(tracks) > 0
