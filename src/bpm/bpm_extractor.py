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


if __name__ == "__main__":
    files = []
    for file in os.listdir(sys.argv[1]):
        if file.endswith(".wav"):
            files.append(os.path.join(sys.argv[1], file))

    mono_files = []
    for file in files:
        mono_files.append(get_MonoLoaded_Song(file))
    
    pool = Pool(8)
    res = pool.map(get_song_bpm, mono_files)
    pool.close()

    print(tabulate(res,
                   headers=[ 'BPM', 'Confidence'],
                   tablefmt='orgtbl'))
