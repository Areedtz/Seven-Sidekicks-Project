#!/usr/local/bin/python3.6

import sys
import os
from multiprocessing import Pool

from tabulate import tabulate
from essentia.standard import RhythmExtractor2013

from utilities.filehandler.handle_audio import get_MonoLoaded_Song


def get_song_bpm(audio):
    rhythm_extractor = RhythmExtractor2013()
    bpm, _, beats_confidence, _, _ = rhythm_extractor(audio)

    return bpm, beats_confidence

