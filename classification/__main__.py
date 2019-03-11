import os
import sys
import re

from extractor.high_level_data_extractor import make_high_level_data_file
from classifier.profile_data_extractor import get_classifier_data
from utilities.get_song_id import get_song_id
from pprint import pprint
from tabulate import tabulate

from multiprocessing import Pool


def process_data_and_extract_profiles(song_id, song_file, song_output_file):
    make_high_level_data_file(song_file, song_output_file)

    timbre, mood_relaxed, mood_party = get_classifier_data(song_output_file)
    return song_id, timbre, mood_relaxed, mood_party

if __name__ == "__main__":
    # Go through all .wav files in the given directory
    dirname = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = os.path.join(dirname, "output/")
    argument_triples = []

    for file in os.listdir(sys.argv[1]):
        if file.endswith(".wav"):
            song_file = os.path.join(sys.argv[1], file)
            song_id = get_song_id(song_file)
            song_output_file = "{}{}_output.json".format(
                output_folder_path, song_id)

            argument_triples.append((
                song_id,
                song_file,
                song_output_file))

    # Multithreaded runthrough of all files
    pool = Pool(8)
    res = pool.starmap(process_data_and_extract_profiles, argument_triples)
    pool.close()

    print(tabulate(res,
                   headers=['Song ID', 'Timbre', 'Mood relaxed', 'Mood party'],
                   tablefmt='orgtbl'))
