import os
import sys

from classification.audio_analysis import process_data_and_extract_profiles
import utilities.get_song_id as s_id
from similarity.split_song import split_song


def test_profile_song_data():
    dirname = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = os.path.join(dirname, "output/")
    filename = os.path.join(
        dirname,
        "test_audio_analysis/8376-1-1_Demolition_Man_proud_music_preview.wav")
    result = []

    song_id = s_id.get_song_id(filename)
    
    split_song_list = split_song(filename)

    for i in range(len(split_song_list)):
        song_output_file = "{}{}_{}_output.json".format(
                output_folder_path, i, song_id)
        
        result.append(
            process_data_and_extract_profiles(
                song_id, 
                split_song_list[i], 
                song_output_file))


    assert result