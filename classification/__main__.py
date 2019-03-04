import os
import sys
from extractor.high_level_data_extractor import get_high_level_data
from classifier.profile_data_extractor import get_profile_data

from multiprocessing import Pool

local_file_path_list = []

profile = sys.argv[2]

def process_data_and_extract_profiles(local_song_file, local_output_file):
    get_high_level_data(local_song_file, local_output_file)
    dirname = os.path.dirname(__file__)
    profile_output = 'output/profile_output/{}.json'.format(local_song_file)
    profile_output_path = os.path.join(dirname, profile_output)
    get_profile_data(local_output_file, profile_output_path, profile)
    os.system('rm {}'.format(local_output_file))

def get_song_id(filename):
    return filename.split("/")[-1].split("-")[0]

if __name__ == "__main__":
    # Go through all .wav files in the given directory
    dirname = os.path.dirname(__file__)
    argument_tuples = []
    for file in os.listdir(sys.argv[1]):
        if file.endswith(".wav"):
            local_file = (os.path.join(sys.argv[1], file))
            local_file_path = "{}{}_output.json".format('output/', get_song_id(local_file))
            local_dir = os.path.join(dirname, local_file_path)
            local_file_path_list.append(local_dir)
            argument_tuples.append((
                        local_file,
                        local_dir))

    # Multithreaded runthrough of all files
    pool = Pool(8)
    pool.starmap(process_data_and_extract_profiles, argument_tuples)
    pool.close()

    #for file_path in local_file_path_list:
    #    os.system('cat {}'.format(file_path))