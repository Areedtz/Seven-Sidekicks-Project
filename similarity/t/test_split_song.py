import os

from similarity.split_song import split_song


def test_split_song():
    dirname = os.path.dirname(__file__)
    test_filename = os.path.join(
        dirname, "test_split_song/8376-1-1_Demolition_Man_proud_music_preview.wav")

    segments = split_song(test_filename)

    assert len(segments) == 19
