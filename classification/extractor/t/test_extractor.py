import os
import sys

from classification.extractor.high_level_data_extractor import make_low_level_data_file

def test_song_data_extraction():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_extractor/8376-1-1_Demolition_Man_proud_music_preview.wav")
    output_filename = os.path.join(dirname, "8376-1-1_output.json")

    make_low_level_data_file(filename, output_filename)

    assert os.path.isfile(output_filename)
    assert os.stat(output_filename) != 0

    os.remove(output_filename)