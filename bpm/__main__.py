import sys
import os

from multiprocessing import Pool
from tabulate import tabulate

from bpm_extractor import get_song_BPM


if __name__ == "__main__":
    # Go through all .wav files in the given directory
    files = []
    for file in os.listdir(sys.argv[1]):
        if file.endswith(".wav"):
            files.append(os.path.join(sys.argv[1], file))

    # Multithreaded runthrough of all files
    pool = Pool(8)
    res = pool.map(get_song_BPM, files)
    pool.close()

    # Create a neat table of the data
    table = tabulate(
        res,
        headers=['Song ID', 'BPM', 'Confidence'],
        tablefmt='orgtbl')

    print(table)
