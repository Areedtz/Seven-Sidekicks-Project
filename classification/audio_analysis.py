import os
import sys
import re
import csv
import subprocess
import tempfile

from multiprocessing import Pool
from essentia.standard import MonoWriter

from classification.extractor.low_level_data_extractor import make_low_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data
from similarity.split_song import split_song
from utilities.filehandler.handle_audio import get_MonoLoaded_Song
from utilities.filehandler.handle_path import get_absolute_path
from utilities.get_song_id import get_song_id


def process_data_and_extract_profiles(segment_id, song_file):
    #creating the temporary files
    temp_song = tempfile.NamedTemporaryFile(delete=True)
    temp_classifier = tempfile.NamedTemporaryFile(delete=True)
    
    MonoWriter(filename=temp_song.name)(song_file)

    make_low_level_data_file(temp_song.name, temp_classifier.name)

    #closing and effectively deleting the song tempfile
    temp_song.close()

    timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad = get_classifier_data(temp_classifier.name)

    #closing and effectively deleting the classifier tempfile
    temp_classifier.close()

    return segment_id, timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad


def segment_song_and_return_arguments(filename, song_file):
    dirname = os.path.abspath(os.path.dirname(filename))
    argument_tuples = []

    song_id = get_song_id(song_file)
    
    loaded_song = get_MonoLoaded_Song(song_file)

    split_song_list = split_song(loaded_song)

    for i in range(len(split_song_list)):
        argument_tuples.append((
            i,
            split_song_list[i]))

    return song_id, dirname, argument_tuples

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()

    arg = sys.argv[1]

    song_id, output_folder_path, argument_tuples = segment_song_and_return_arguments(__file__, arg)

    csv_output_file = "{}{}_segmented_output.csv".format(
            output_folder_path, song_id)

    # CSV file header
    with open(csv_output_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([song_id, 'Segment ID', 'Timbre', 'Mood Relaxed', 'Mood Party', 'Mood Aggressive', 'Mood Happy', 'Mood Sad'])

    csv_file.close()

    # Multithreaded runthrough of all files
    pool = Pool(8)
    res = pool.starmap(process_data_and_extract_profiles, argument_tuples)
    pool.close()

    csv_data = [res]

    with open(csv_output_file, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    csv_file.close()