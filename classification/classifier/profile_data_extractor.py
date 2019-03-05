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

    timbre = highlevel['timbre']['all']['bright']
    mood_relaxed = highlevel['mood_relaxed']['all']['relaxed']
    mood_party = highlevel['mood_party']['all']['party']

    subprocess.run("rm {}".format(output_file_path), shell=True)

    return timbre, mood_relaxed, mood_party


if __name__ == "__main__":
    data_file = sys.argv[1]

    res = get_classifier_data(data_file)

    pprint(res)