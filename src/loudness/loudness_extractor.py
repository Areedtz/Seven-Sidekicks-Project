import sys
from typing import Tuple

from essentia import run, Pool
from essentia.standard import RhythmExtractor2013
from essentia.streaming import LoudnessEBUR128


def get_song_loudness(audio) -> Tuple[float, float, float]:
    """Extracts the loudness data for the given audio

    Parameters
    ----------
    audio
        Raw audio that has been loaded into an Audioloader

    Returns
    -------
    Tuple[float, float, float]
        A tuple of the song's loudness values
    """

    # Creating a pool to run the audio through
    p = Pool()

    audio.sampleRate >> (p, "sampleRate")
    audio.numberChannels >> (p, "numberChannels")
    audio.md5 >> (p, "md5")
    audio.bit_rate >> (p, "bit_rate")
    audio.codec >> (p, "codec")

    b = LoudnessEBUR128(hopSize=0.1, sampleRate=44100)
    audio.audio >> b.signal
    b.momentaryLoudness >> (p, "momentaryLoudness")
    b.shortTermLoudness >> (p, "shortTermLoudness")
    b.integratedLoudness >> (p, "integratedLoudness")
    b.loudnessRange >> (p, "loudnessRange")

    run(audio)

    # Essentia had 2 methods of determining the loudness or DBFS of a clip
    # we use the max value of either method
    max_loudness = max(*p["momentaryLoudness"], *p["shortTermLoudness"])

    return max_loudness, p["integratedLoudness"], p["loudnessRange"]
