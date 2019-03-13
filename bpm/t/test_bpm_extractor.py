import os
import sys

# Start of importing the utilities module
sys.path.insert(0, os.path.abspath("utilities/"))

#import get_song_id as s_id
# End of importing the utilities module

from bpm.bpm_extractor import get_song_bpm, s_id


def test_get_song_id():
    assert s_id.get_song_id("8376-1-1_Demolition_Man_proud_music_preview.wav") == "8376-1-1"

def test_get_song_bpm():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, 
        "test_bpm_extractor/8376-1-1_Demolition_Man_proud_music_preview.wav")
    
    song_id, bpm, confidence = get_song_bpm(filename)

    assert song_id == "8376-1-1"
    assert round(bpm, 3) == 139.847
    assert round(confidence, 4) == 2.4134
