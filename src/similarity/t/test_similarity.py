import numpy as np
import falconn

from database.mongo.audio.song_segment import SongSegment
from similarity.similarity import _load_songs, _dist, \
    _create_bucket, _find_matches
from utilities.config_loader import load_config

cfg = load_config()
MATCHES = cfg['similarity_matches']


def test_load_songs(mocker):
    mock_get = mocker.patch.object(SongSegment, 'get_all_by_song_id', autospec=True, return_value=[])
    mock_add = mocker.patch.object(SongSegment, 'add', autospec=True)

    segments = _load_songs(
        [('8376-1-1', "similarity/t/test_split_song" +
          "/8376-1-1_Demolition_Man_" +
          "proud_music_preview.wav")])

    mock_get.assert_called_once()
    mock_add.assert_called()

    assert len(segments) == 18
    assert segments[0][1] == '8376-1-1'
    assert segments[0][2] == 0


def test_create_bucket(mocker):
    mock_get = mocker.patch.object(SongSegment, 'get_all_by_song_id', autospec=True, return_value=[])
    mock_add = mocker.patch.object(SongSegment, 'add', autospec=True)

    segments = _load_songs(
        [('8376-1-1', "similarity/t/test_split_song" +
          "/8376-1-1_Demolition_Man_" +
          "proud_music_preview.wav")])

    mock_get.assert_called_once()
    mock_add.assert_called()

    data = np.array(list(map(lambda x: x[3], segments)))

    segs, table = _create_bucket(data)
    assert np.array_equal(data, segs)
    assert isinstance(table, falconn.LSHIndex)


def test_dist():
    start = ('', '', 0, np.array([0, 0]))
    end = ('', '', 1, np.array([0, 1]))
    assert _dist(start, end) == 1

    end = ('', '', 2, np.array([1, 0]))
    assert _dist(start, end) == 1


def test_find_matches(mocker):
    mock_get = mocker.patch.object(SongSegment, 'get_all_by_song_id', autospec=True, return_value=[])
    mock_add = mocker.patch.object(SongSegment, 'add', autospec=True)

    segments = _load_songs(
        [('8376-1-1', "similarity/t/test_split_song" +
          "/8376-1-1_Demolition_Man_" +
          "proud_music_preview.wav")])

    mock_get.assert_called_once()
    mock_add.assert_called()

    data = np.array(list(map(lambda x: x[3], segments)))

    bucket = _create_bucket(data)

    query_object = bucket[1].construct_query_pool()
    query_object.set_num_probes(25)

    matches = list(map(_find_matches, list(
        map(lambda seg: (seg, query_object), segments))))

    assert len(matches[0]) == 10
