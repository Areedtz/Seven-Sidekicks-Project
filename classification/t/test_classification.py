import os
import sys

from classification.extractor.high_level_data_extractor import make_high_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data


def test_song_data_extraction():
    dirname = os.path.abspath(os.path.dirname(__file__))
    print(dirname)
    filename = os.path.join(
        dirname,
        "./test_classification/8376-1-1_Demolition_Man_proud_music_preview.wav")
    output_filename = os.path.join(dirname, "./8376-1-1_output.json")

    make_high_level_data_file(filename, output_filename)

    assert os.path.isfile(output_filename)
