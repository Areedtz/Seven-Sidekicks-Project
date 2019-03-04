from database.database import _create_default_document, _augment_document, Database
import datetime


def test_create_default_document():
    default_doc = _create_default_document(10)
    assert default_doc['song_id'] == 10
    assert isinstance(default_doc['last_updated'], datetime.datetime)


def test_augment_document():
    doc1 = {
        "name1": "value1"
    }
    doc2 = {
        "name2": "value2"
    }
    expected = {
        "name1": "value1",
        "name2": "value2",
    }
    assert _augment_document(doc1, doc2) == expected


def test_add_and_get_track_BPM():
    db = Database()
    db.add_track_BPM(1200, 100., 3.)
    track = db.get_track_BPM(1200)
    print(track)
    assert track['song_id'] == 1200
    assert track['bpm'] == 100.
    assert track['confidence'] == 3.


def test_get_track_BPMs():
    db = Database()
    tracks = db.get_track_BPMs()
    assert len(tracks) > 0
