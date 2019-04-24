import json
from tempfile import NamedTemporaryFile

from classification.extractor.low_level_data_extractor import make_low_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data
from bpm.bpm_extractor import get_song_bpm

def process_data_and_extract_profiles(song_id, song_file_path, output_file_path):
    temp_file = NamedTemporaryFile(delete=True)

    make_low_level_data_file(song_file_path, temp_file.name)

    timbre, relaxed, party, aggressive, happy, sad = get_classifier_data(temp_file.name)

    temp_file.close()

    bpm_info = get_song_bpm(song_file_path)

    # Save file in config directory
    data = {}
    data['bpm'] = {
        'value': bpm_info[0],
        'confidence': bpm_info[1]
    }

    data['timbre'] = {
        'value': timbre[0],
        'confidence': timbre[1]
    }

    data['relaxed'] = {
        'value': relaxed[0],
        'confidence': relaxed[1]
    }

    data['party'] = {
        'value': party[0],
        'confidence': party[1]
    }

    data['aggressive'] = {
        'value': aggressive[0],
        'confidence': aggressive[1]
    }

    data['happy'] = {
        'value': happy[0],
        'confidence': happy[1]
    }

    data['sad'] = {
        'value': sad[0],
        'confidence': sad[1]
    }

    with open(output_file_path + '/' + song_id + '.json', 'w') as outfile:
        json.dump(data, outfile)

    return False
