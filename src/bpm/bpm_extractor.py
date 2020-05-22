from typing import Tuple

from essentia.standard import RhythmExtractor2013


def get_song_bpm(audio, params={}) -> Tuple[float, float]:
    """Extracts the BPM for the given monoloaded audio file

    Parameters
    ----------
    audio
        Monoloaded audio to be analyzed
    params
        RhythmExtractor2013 parameters

    Returns
    -------
    Tuple[float, float]
        A tuple of the BPM and a confidence of that BPM
    """

    rhythm_extractor = RhythmExtractor2013(**params)
    bpm, _, beats_confidence, _, _ = rhythm_extractor(audio)

    return bpm, beats_confidence
