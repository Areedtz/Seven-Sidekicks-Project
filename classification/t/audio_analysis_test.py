import os
import sys

from classification.audio_analysis import segment_song_and_extract_profile_data

def test_profile_song_data():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_audio_analysis/8376-1-1_Demolition_Man_proud_music_preview.wav")

    segment_song_and_extract_profile_data(filename)

    assert song_data != None