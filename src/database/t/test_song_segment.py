from database.song_segment import SongSegment
from database.storinator import Storinator
import datetime


def test_implements_Storinator():
    ss = SongSegment()
    assert isinstance(ss, Storinator)


def test_database_name():
    ss = SongSegment()
    assert ss._dbcol == 'song_segmentation'


# TODO: Add mfcc, chroma, tempogram
def test_add_and_get():
    ss = SongSegment()
    ss.add(1, 0, 5000, None, None, None, None)
    seg = ss.get(1)
    assert seg['song_id'] == 1
    assert seg['time_from'] == 0
    assert seg['time_to'] == 5000
    assert seg['mfcc'] == None
    assert seg['chroma'] == None
    assert seg['tempogram'] == None
    assert seg['similar'] == None


def test_get_all():
    ss = SongSegment()
    ss.add(1, 0, 5000, None, None, None, None)
    seg = ss.get_all()
    assert len(seg) > 0
