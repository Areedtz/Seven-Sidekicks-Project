import datetime

from database.mongo.database import \
    _create_default_document, _augment_document, Database


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


def test_insert_and_find():
    db = Database()
    db.insert('test', 1, {
        "key": "value"
    })
    track = db.find('test', 1)

    assert track['song_id'] == 1
    assert isinstance(track['last_updated'], datetime.datetime)


def test_get_track_BPMs():
    db = Database()
    db.insert('test', 1, {
        "key": "value"
    })
    tracks = db.find_all('test')

    assert len(tracks) > 0


def test_find_returns_latest_with_songid():
    db = Database()
    db.insert('test', 1, {
        "key": "value"
    })
    db.insert('test', 1, {
        "key": "v"
    })
    track = db.find('test', 1)

    assert track["key"] == "v"
