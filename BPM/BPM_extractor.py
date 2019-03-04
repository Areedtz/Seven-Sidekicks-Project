import sys
import os

from multiprocessing import Pool
from tabulate import tabulate

from essentia.standard import MonoLoader, RhythmExtractor2013


def get_song_id(filename):
    return filename.split("/")[-1].split("-")[0]

def get_song_BPM(filename):
    loader = MonoLoader(filename=filename)
    audio = loader()
    
    rhythm_extractor = RhythmExtractor2013()
    bpm, _, beats_confidence, _, _= rhythm_extractor(audio)
    
    song_id = get_song_id(filename)

    return song_id, bpm, beats_confidence


if __name__ == "__main__":
    files = []
    for file in os.listdir(sys.argv[1]):
        if file.endswith(".wav"):
            files.append(os.path.join(sys.argv[1], file))

    pool = Pool(8)
    res = pool.map(get_song_BPM, files)
    pool.close()

    print(tabulate(res, headers=['Song ID', 'BPM', 'Confidence'], tablefmt='orgtbl'))