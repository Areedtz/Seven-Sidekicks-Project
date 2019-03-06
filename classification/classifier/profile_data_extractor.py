import sys
import os
import subprocess
import json
from pprint import pprint


def get_classifier_data(data_file_name):
    dirname = os.path.abspath(os.path.dirname(__file__))
    profile_file = os.path.join(dirname, "timbre_relaxed_party_profile.yaml")

    output_file_path = data_file_name.split(".")[0] + "-model-data.json"

    command = 'essentia_streaming_extractor_music_svm {} {} {}'.format(
        data_file_name, output_file_path, profile_file)

    subprocess.run("cd {} && {}".format(dirname, command), shell=True)

    with open(output_file_path) as f:
        data = json.load(f)

    highlevel = data['highlevel']

    timbre = highlevel['timbre']['value']
    timbre_probability = highlevel['timbre']['probability']
    mood_relaxed = highlevel['mood_relaxed']['value']
    mood_relaxed_probability = highlevel['mood_relaxed']['probability']
    mood_party = highlevel['mood_party']['value']
    mood_party_probability = highlevel['mood_party']['probability']

    subprocess.run("rm {}".format(output_file_path), shell=True)

    return (timbre, timbre_probability), (mood_relaxed, mood_relaxed_probability), (mood_party, mood_party_probability)


if __name__ == "__main__":
    data_file = sys.argv[1]

    res = get_classifier_data(data_file)

    pprint(res)