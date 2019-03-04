import os
import sys

from ../classification.extractor.high_level_data_extractor import get_high_level_data
from ../classification.classifier.profile_data_extractor import get_profile_data

def test_get_song_file():
    assert os.path.exists('./test_classification/8376-Demolition_Man_proud_music_preview.wav')

def test_song_extraction():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, 
        "8376-Demolition_Man_proud_music_preview.wav")
    outputfilename = "8376-Demolition_Man_proud_music_preview_output.json"
    
    get_high_level_data(filename, outputfilename)

    get_profile_data(outputfilename)

    assert os.path.exists('./test_classification/8376-Demolition_Man_proud_music_preview_output.json')