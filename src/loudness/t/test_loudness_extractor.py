from loudness.loudness_extractor import get_song_loudness
from utilities.filehandler.audio_loader import get_audio_loaded_song


def test_get_song_loudness():
    song = get_audio_loaded_song("loudness/t/test_loudness_extractor/8376-1-" +
                                 "1_Demolition_Man_proud_music_preview.wav")
    max_loudness, integratedLoudness, loudnessRange = get_song_loudness(song)

    assert round(float(max_loudness), 5) == -6.05837
    assert round(float(integratedLoudness), 5) == -9.10699
    assert loudnessRange == 10.448598861694336
