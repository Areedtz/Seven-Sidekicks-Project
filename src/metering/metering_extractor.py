import sys

from typing import Tuple

from essentia import run, Pool
from essentia.standard import RhythmExtractor2013
from essentia.streaming import LoudnessEBUR128, AudioLoader


def get_song_metering(data_file_name) -> Tuple[list, list, float, float]:
    """Extracts the metering data for the given audio

    Parameters
    ----------
    data_file_name
        Raw audio to be analyzed

    Returns
    -------
    Tuple[list, list, float, float]
        A tuple of the song's metering values
    """

    p = Pool()

    a = AudioLoader(filename = data_file_name)
    a.sampleRate >> (p, "sampleRate")
    a.numberChannels >> (p, "numberChannels")
    a.md5 >> (p, "md5")
    a.bit_rate >> (p, "bit_rate")
    a.codec >> (p, "codec")

    b = LoudnessEBUR128(hopSize = 0.1, sampleRate = 44100)
    a.audio >> b.signal
    b.momentaryLoudness >> (p, "momentaryLoudness")
    b.shortTermLoudness >> (p, "shortTermLoudness")
    b.integratedLoudness >> (p, "integratedLoudness")
    b.loudnessRange >> (p, "loudnessRange")

    run(a)

    return p["momentaryLoudness"], p["shortTermLoudness"], p["integratedLoudness"], p["loudnessRange"]

a = get_song_metering(sys.argv[1])

print(min(a[0]))
print(max(a[1]))
print(sum(a[0])/len(a[0]))
print(sum(a[1])/len(a[0]))
print(a[3])