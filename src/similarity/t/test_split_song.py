from similarity.split_song import split_song

from utilities.filehandler.handle_audio import get_MonoLoaded_Song


def test_split_song():
    song = get_MonoLoaded_Song("similarity/t/test_split_song"
                               + "/8376-1-1_Demolition_Man_"
                               + "proud_music_preview.wav")
    segments = split_song(song)

    assert len(segments) == 19
    
