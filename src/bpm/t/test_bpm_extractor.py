import os
import sys

from bpm.bpm_extractor import get_song_bpm
from utilities.filehandler.handle_audio import get_MonoLoaded_Song


def test_get_song_bpm():
    song = get_MonoLoaded_Song("bpm/t/test_bpm_extractor/8376-1"
                               + "-1_Demolition_Man_proud_music_preview.wav")
    bpm, confidence = get_song_bpm(song)

    assert round(bpm, 3) == 139.847
    assert round(confidence, 4) == 2.4134
