import json
from tempfile import NamedTemporaryFile

from classification.extractor.low_level_data_extractor import make_low_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data


def process_data_and_extract_profiles(song_id, song_file_path, output_file_path):
    temp_file = NamedTemporaryFile(delete=True)

    make_low_level_data_file(song_file_path, temp_file.name)

    timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad = get_classifier_data(temp_file.name)

    temp_file.close()

    # Save file in config directory
    data = {}
    data['timbre'] = {
        'value': timbre[0],
        'confidence': timbre[1]
    }

    data['mood_relaxed'] = {
        'value': mood_relaxed[0],
        'confidence': mood_relaxed[1]
    }

    data['mood_party'] = {
        'value': mood_party[0],
        'confidence': mood_party[1]
    }

    data['mood_aggressive'] = {
        'value': mood_aggressive[0],
        'confidence': mood_aggressive[1]
    }

    data['mood_happy'] = {
        'value': mood_happy[0],
        'confidence': mood_happy[1]
    }

    data['mood_sad'] = {
        'value': mood_sad[0],
        'confidence': mood_sad[1]
    }

    with open(output_file_path + '/' + song_id + '.json', 'w') as outfile:
        json.dump(data, outfile)

    return False
