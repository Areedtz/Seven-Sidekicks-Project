from database.song_seg import SSegmentation
from database.storinator import Storinator
import datetime


def test_implements_Storinator():
    ss = SSegmentation()
    assert isinstance(ss, Storinator)


def test_database_name():
    ss = SSegmentation()
    assert ss._col == 'song_segmentation'


def test_add_and_get():
    ss = SSegmentation()
    ss.add(1, 0, 5000)
    seg = ss.get(1)
    assert seg['song_id'] == 1
    assert seg['time_from'] == 0
    assert seg['time_to'] == 5000


def test_get_all():
    ss = SSegmentation()
    ss.add(1, 0, 5000)
    seg = ss.get_all()
    assert len(seg) > 0
