from database.track_relaxed import TrackRelaxed
from database.storinator import Storinator
import datetime


def test_implements_Storinator():
    tbpm = TrackRelaxed()
    assert isinstance(tbpm, Storinator)


def test_database_name():
    tbpm = TrackRelaxed()
    assert tbpm._dbname == 'track_relaxed'


def test_add_and_get():
    tbpm = TrackRelaxed()
    tbpm.add(1, 'relaxed', .82)
    track = tbpm.get(1)
    assert track['song_id'] == 1
    assert track['relaxed'] == 'relaxed'
    assert track['confidence'] == .82


def test_get_all():
    tbpm = TrackRelaxed()
    tbpm.add(1, 'relaxed', .82)
    tracks = tbpm.get_all()
    assert len(tracks) > 0
