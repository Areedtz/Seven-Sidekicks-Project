#!/usr/local/bin/python3.6

import os
import re
import sys
from multiprocessing import Pool

from typing import Tuple
from tabulate import tabulate

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(__file__ + "../../../"))

import utilities.get_song_id as s_id
from classifier.profile_data_eextractor import get_classifier_data
from extractor.low_level_data_extractor import make_low_level_data_file


def process_data_and_extract_profiles(
    song_id: str, song_file: str, song_output_file: str) -> Tuple[
        str, Tuple, Tuple, Tuple, Tuple, Tuple, Tuple]:
    """Gets lowlevel datafile 
    and uses this to find define moods 
    and returns a tuple with them

    Parameters
    ----------
    song_id
        id of the given song
    song_file
        the filepath of the given song
    song_output_file
        the output file for the lowlevel datafile

    Returns
    -------
    Tuple[str, Tuple, Tuple, Tuple, Tuple, Tuple, Tuple]
        A tuple of the song_id and tuples describing all moods and their probability
    """

    make_low_level_data_file(song_file, song_output_file)

    timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad = get_classifier_data(
        song_output_file)

    return song_id, timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad


if __name__ == "__main__":
    # Go through all .wav files in the given directory
    dirname = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = os.path.join(dirname, "output/")
    argument_triples = []

    for file in os.listdir(sys.argv[1]):
        if file.endswith((".wav", "mp3")):
            song_file = os.path.join(sys.argv[1], file)
            song_id = s_id.get_song_id(song_file)
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
                   headers=[
                       'Song ID', 'Timbre', 'Mood relaxed', 'Mood party',
                       'Mood aggressive', 'Mood happy', 'Mood sad'
                   ],
                   tablefmt='orgtbl'))
