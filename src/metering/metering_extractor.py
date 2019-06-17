import sys

from typing import Tuple

from essentia import run, Pool
from essentia.standard import RhythmExtractor2013
from essentia.streaming import LoudnessEBUR128

from utilities.filehandler.audio_loader import get_audio_loaded_song


def get_song_metering(data_file_path) -> Tuple[list, list, float, float]:
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

    audio = get_audio_loaded_song(data_file_path)
    audio.sampleRate >> (p, "sampleRate")
    audio.numberChannels >> (p, "numberChannels")
    audio.md5 >> (p, "md5")
    audio.bit_rate >> (p, "bit_rate")
    audio.codec >> (p, "codec")

    b = LoudnessEBUR128(hopSize = 0.1, sampleRate = 44100)
    audio >> b.signal
    b.momentaryLoudness >> (p, "momentaryLoudness")
    b.shortTermLoudness >> (p, "shortTermLoudness")
    b.integratedLoudness >> (p, "integratedLoudness")
    b.loudnessRange >> (p, "loudnessRange")

    run(audio)

    return p["momentaryLoudness"], p["shortTermLoudness"], p["integratedLoudness"], p["loudnessRange"]

#a = get_song_metering(sys.argv[1])

#print(min(a[0]))
#print(max(a[1]))
#print(sum(a[0])/len(a[0]))
#print(sum(a[1])/len(a[0]))
#print(a[3])