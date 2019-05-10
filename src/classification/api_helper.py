import json
from tempfile import NamedTemporaryFile

from bpm.bpm_extractor import get_song_bpm
from classification.classifier.profile_data_extractor import \
    get_classifier_data
from classification.extractor.low_level_data_extractor import \
    make_low_level_data_file
from database.track_emotion import TrackEmotion
from utilities.filehandler.handle_audio import get_MonoLoaded_Song


def process_data_and_extract_profiles(
    song_id: str, song_file_path: str):
    """Extracts BPM, moods from a song 
    and puts it into the database

    Parameters
    ----------
    song_id
        id of the given song
    song_file_path
        the filepath of the given song
    """

    temp_file = NamedTemporaryFile(delete=True)

    make_low_level_data_file(song_file_path, temp_file.name)

    timbre, relaxed, party, aggressive, happy, sad = get_classifier_data(
        temp_file.name)

    temp_file.close()

    mono_loaded_song = get_MonoLoaded_Song(song_file_path)

    bpm_info = get_song_bpm(mono_loaded_song)

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

    DBConnecter = TrackEmotion()
    DBConnecter.add(song_id, data)

