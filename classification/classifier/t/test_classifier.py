import os
import sys

from classification.classifier.profile_data_extractor import get_classifier_data

def test_profile_song_data():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_classifier/8376-1-1_output.json")

    song_data = get_classifier_data(filename)

    assert song_data != None
    assert song_data[0] == ("dark", 0.728462159634)
    assert song_data[1] == ("not_relaxed", 0.980210959911)
    assert song_data[2] == ("not_party", 0.643296301365)
