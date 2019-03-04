import os

from BPM.BPM_extractor import get_song_id, get_song_BPM


def test_get_song_id():
    assert get_song_id("8376-Demolition_Man_proud_music_preview.wav") == "2200061"

def test_get_song_bpm():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, 
        "test_BPM_extractor/8376-Demolition_Man_proud_music_preview.wav")
    
    song_id, bpm, confidence = get_song_BPM(filename)

    assert song_id == "8376"
    assert round(bpm, 3) == 139.847
    assert round(confidence, 4) == 2.4134
