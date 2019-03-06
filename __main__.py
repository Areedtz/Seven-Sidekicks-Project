import sys
import os
from multiprocessing import Pool

from bpm.bpm_extractor import get_song_bpm
from classification.extractor.high_level_data_extractor import make_high_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data
from database.track_bpm import TrackBPM
from database.track_party import TrackParty
from database.track_relaxed import TrackRelaxed
from database.track_timbre import TrackTimbre


def extract_and_save_data_from_song(filename):
    if not filename.endswith(".wav"):
        print("File is not a .wav file. Exiting...")
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

    make_high_level_data_file(filename, output_file_path)

    timbre, relaxed, party = get_classifier_data(output_file_path)

    bpm_database_client.add(song_id, bpm, bpm_confidence)
    timbre_database_client.add(song_id, timbre[0], timbre[1])
    relaxed_database_client.add(song_id, relaxed[0], relaxed[1])
    party_database_client.add(song_id, party[0], party[1])



def extract_and_save_data_from_songs_in_folder(folder_path):
    files = []
    for file in os.listdir(folder_path):
        if file.endswith(".wav"):
            files.append(os.path.join(folder_path, file))

    pool = Pool(8)
    res = pool.map(extract_and_save_data_from_song, files)
    pool.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()

    arg = sys.argv[1]

    if os.path.isfile(arg):
        extract_and_save_data_from_song(arg)

    elif os.path.isdir(arg):
        extract_and_save_data_from_songs_in_folder(arg)

    else:
        print("{} is not a folder or a path. Exiting...".format(arg))
        exit()
