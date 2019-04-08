import os
import sys

from classification.audio_analysis import process_data_and_extract_profiles
import utilities.get_song_id as s_id
from similarity.split_song import split_song
from utilities.filehandler.handle_audio import get_MonoLoaded_Song


def test_profile_song_data():
    dirname = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = os.path.join(dirname, "")
    filename = os.path.join(
        dirname,
        "test_audio_analysis/8376-1-1_Demolition_Man_proud_music_preview.wav")

    song_id = s_id.get_song_id(filename)
    
    loaded_song = get_MonoLoaded_Song(filename)

    split_song_list = split_song(loaded_song)

    #for i in range(len(split_song_list)):
    song_output_file = "{}{}_{}_output.json".format(
            output_folder_path, 0, song_id)
        
    (segment_id, timbre, 
     mood_relaxed, mood_party, 
     mood_aggressive, mood_happy, 
     mood_sad) = process_data_and_extract_profiles(
            0, 
            split_song_list[0], 
            song_output_file)

    (segment_id1, timbre1, 
     mood_relaxed1, mood_party1, 
     mood_aggressive1, mood_happy1, 
     mood_sad1) = process_data_and_extract_profiles(
            1, 
            split_song_list[1], 
            song_output_file)

    assert segment_id == 0
    assert segment_id1 == 1
    assert timbre == ('dark', 0.862666606903)
    assert timbre1 != ('dark', 0.862666606903)
