import os
import sys

def get_profile_data(data_file_name, output_file_path, profile_file):
    command = 'essentia_streaming_extractor_music_svm {} {} {}'.format(data_file_name, output_file_path, profile_file)

    os.system(command)