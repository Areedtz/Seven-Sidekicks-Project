import os
import sys

from metering.metering_extractor import get_song_metering
from utilities.filehandler.audio_loader import get_audio_loaded_song

def test_get_song_metering():
    song = get_audio_loaded_song("metering/t/test_bpm_extractor/8376-1"
                               + "-1_Demolition_Man_proud_music_preview.wav")
    momentaryLoudness, shortTermLoudness, integratedLoudness, loudnessRange = get_song_metering(song)

    assert min(momentaryLoudness) == -64.66297
    assert max(momentaryLoudness) == -5.104908
    assert min(shortTermLoudness) == -23.858686
    assert max(shortTermLoudness) == -7.01184
    assert round(integratedLoudness, 4) == -9.106990814208984
    assert round(loudnessRange, 4) == 10.448598861694336

