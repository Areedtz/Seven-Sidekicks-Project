import os
import sys
import re
import csv

# Start of importing the utilities module
sys.path.insert(0, os.path.abspath("../utilities/"))
import get_song_id as s_id
# End of importing the utilities module

from extractor.low_level_data_extractor import make_low_level_data_file
from classifier.profile_data_extractor import get_classifier_data
from similarity.split_song import split_song

from pprint import pprint
from tabulate import tabulate

from multiprocessing import Pool

def process_data_and_extract_profiles(segment_id, song_file, song_output_file):
    make_low_level_data_file(song_file, song_output_file)

    timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad = get_classifier_data(song_output_file)

    return segment_id, timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad


def segment_song_and_extract_profile_data(song_file):
    # Go through all .wav files in the given directory
    dirname = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = os.path.join(dirname, "output/")
    argument_triples = []

    song_id = s_id.get_song_id(song_file)
    
    split_song_list = split_song(song_file)

    for i in range(split_song_list.__len__):
        song_output_file = "{}{}_{}_output.json".format(
                output_folder_path, i, song_id)
                
        argument_triples.append((
            song_id,
            split_song_list[i],
            song_output_file))

        #make_low_level_data_file(split_song_list[i], song_output_file)


    # Multithreaded runthrough of all files
    pool = Pool(8)
    res = pool.starmap(process_data_and_extract_profiles, argument_triples)
    pool.close()

    csv_data = [res]

    csv_output_file = "{}{}_output.csv".format(
            output_folder_path, song_id)

    with open(csv_output_file, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    csv_file.close()
 