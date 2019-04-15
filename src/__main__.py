#!/usr/local/bin/python3.6

import sys
import os
from multiprocessing import Pool

# Start of importing the utilities module
# Needed due to the fact it imports a module that uses the utility module
#sys.path.insert(0, os.path.abspath("utilities/"))
# End of importing the utilities module

from bpm.bpm_extractor import get_song_bpm
from classification.extractor.low_level_data_extractor import make_low_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data
from database.track_bpm import TrackBPM
from database.track_party import TrackParty
from database.track_relaxed import TrackRelaxed
from database.track_timbre import TrackTimbre
from rest_api.application import app, hostURL, hostPort


def extract_and_save_data_from_song(filename):
    if not filename.endswith((".wav", ".mp3")):
        print("File is not a .wav or .mp3 file. Exiting...")
        exit()

    bpm_database_client = TrackBPM()
    timbre_database_client = TrackTimbre()
    relaxed_database_client = TrackRelaxed()
    party_database_client = TrackParty()

    if not os.path.isdir("output/"):
        os.mkdir("output", 0o755)

    song_id, bpm, bpm_confidence = get_song_bpm(filename)

    output_folder_abs_path = os.path.abspath("output/")
    output_file_name = "{}_output.json".format(song_id)
    output_file_path = os.path.join(output_folder_abs_path, output_file_name)

    make_low_level_data_file(filename, output_file_path)

    timbre, relaxed, party = get_classifier_data(output_file_path)

    bpm_database_client.add(song_id, bpm, bpm_confidence)
    timbre_database_client.add(song_id, timbre[0], timbre[1])
    relaxed_database_client.add(song_id, relaxed[0], relaxed[1])
    party_database_client.add(song_id, party[0], party[1])



def extract_and_save_data_from_songs_in_folder(folder_path):
    files = []
    for file in os.listdir(folder_path):
        if file.endswith((".wav", ".mp3")):
            files.append(os.path.join(folder_path, file))

    pool = Pool(8)
    res = pool.map(extract_and_save_data_from_song, files)
    pool.close()


if __name__ == "__main__":
    app.run(host=hostURL, port=hostPort, debug=True)
"""    if len(sys.argv) < 2:
        exit()

    arg = sys.argv[1]

    if os.path.isfile(arg):
        extract_and_save_data_from_song(arg)

    elif os.path.isdir(arg):
        extract_and_save_data_from_songs_in_folder(arg)

    else:
        print("{} is not a folder or a path. Exiting...".format(arg))
        exit()
"""