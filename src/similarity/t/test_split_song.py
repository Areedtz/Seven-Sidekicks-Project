from similarity.split_song import split_song

from utilities.filehandler.audio_loader import get_mono_loaded_song


def test_split_song():
    song = get_mono_loaded_song("similarity/t/test_split_song"
                               + "/8376-1-1_Demolition_Man_"
                               + "proud_music_preview.wav")
    segments = split_song(song)

    assert len(segments) == 19

