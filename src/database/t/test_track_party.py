from database.track_party import TrackParty
from database.storinator import Storinator
import datetime


def test_implements_Storinator():
    tbpm = TrackParty()
    assert isinstance(tbpm, Storinator)


def test_database_name():
    tbpm = TrackParty()
    assert tbpm._dbname == 'track_party'


def test_add_and_get():
    tbpm = TrackParty()
    tbpm.add(1, 'party', 0.9)
    track = tbpm.get(1)
    assert track['song_id'] == 1
    assert track['party'] == 'party'
    assert track['confidence'] == 0.9


def test_get_all():
    tbpm = TrackParty()
    tbpm.add(1, 'party', 0.9)
    tracks = tbpm.get_all()
    assert len(tracks) > 0
