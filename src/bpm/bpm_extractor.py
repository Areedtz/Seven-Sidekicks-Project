from typing import Tuple

from essentia.standard import RhythmExtractor2013


def get_song_bpm(audio) -> Tuple[float, float]:
    """Extracts the BPM for the given monoloaded audio file

    Parameters
    ----------
    audio
        Monoloaded audio to be analyzed

    Returns
    -------
    Tuple[float, float]
        A tuple of the BPM and a confidence of that BPM
    """

    rhythm_extractor = RhythmExtractor2013()
    bpm, _, beats_confidence, _, _ = rhythm_extractor(audio)

    return bpm, beats_confidence
