import os
import sys
import re
import csv
import subprocess

# Start of importing the utilities module
sys.path.insert(0, os.path.abspath("../utilities/"))
import utilities.get_song_id as s_id
# End of importing the utilities module

from classification.extractor.low_level_data_extractor import make_low_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data
from similarity.split_song import split_song
from utilities.filehandler.handle_audio import get_MonoLoaded_Song
from utilities.filehandler.handle_path import get_absolute_path
from essentia.standard import MonoWriter

from multiprocessing import Pool


def process_data_and_extract_profiles(segment_id, song_file, song_output_file):
    path = get_absolute_path("{}.wav".format(segment_id))

    writer = MonoWriter(filename=path)(song_file)

    make_low_level_data_file(path, song_output_file)

    timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad = get_classifier_data(song_output_file)

    #removing the segments classifier data file
    #subprocess.run("rm {}".format(song_output_file), shell=True)

    return segment_id, timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad

 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()

    arg = sys.argv[1]

    dirname = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = os.path.join(dirname)
    argument_triples = []

    song_id = s_id.get_song_id(arg)
    
    loaded_song = get_MonoLoaded_Song(arg)

    split_song_list = split_song(loaded_song)

    for i in range(len(split_song_list)):
        song_output_file = "{}{}_{}_output.json".format(
                output_folder_path, i, song_id)

        argument_triples.append((
            song_id,
            split_song_list[i],
            song_output_file))

    csv_output_file = "{}{}_segmented_output.csv".format(
            output_folder_path, song_id)

    # CSV file header
    with open(csv_output_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([song_id, 'Segment ID', 'Timbre', 'Mood Relaxed', 'Mood Party', 'Mood Aggressive', 'Mood Happy', 'Mood Sad'])

    csv_file.close()

    # Multithreaded runthrough of all files
    pool = Pool(8)
    res = pool.starmap(process_data_and_extract_profiles, argument_triples)
    pool.close()

    csv_data = [res]

    with open(csv_output_file, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    csv_file.close()

