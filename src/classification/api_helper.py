import json
from tempfile import NamedTemporaryFile

from bpm.bpm_extractor import get_song_bpm
from classification.classifier.profile_data_extractor import \
    get_classifier_data
from classification.extractor.low_level_data_extractor import \
    make_low_level_data_file
from loudness.loudness_extractor import get_song_loudness
from database.mongo.audio.track_emotion import TrackEmotion
from utilities.filehandler.audio_loader import get_mono_loaded_song
from utilities.filehandler.audio_loader import get_audio_loaded_song


def process_data_and_extract_profiles(
    song_id: str, song_file_path: str):
    """Extracts BPM, moods and loudness values from a song 
    and puts it into the database

    Parameters
    ----------
    song_id
        id of the given song
    song_file_path
        the filepath of the given song
    """

    # Extracting mood & timbre values
    temp_file = NamedTemporaryFile(delete=True)
    make_low_level_data_file(song_file_path, temp_file.name)
    timbre, relaxed, party, aggressive, happy, sad = get_classifier_data(
        temp_file.name)
    temp_file.close()

    # Extracting bpm value
    mono_loaded_song = get_mono_loaded_song(song_file_path)
    bpm_info = get_song_bpm(mono_loaded_song)

    # Extracting loudness value
    audio = get_audio_loaded_song(song_file_path)
    loudness_info = get_song_loudness(audio)

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

    data['peak'] = {
        'value': loudness_info[0],
        'unit': "dbFS"
    }

    data['loudness_integrated'] = {
        'value': loudness_info[1],
        'unit': "LUFS"
    }

    data['loudness_range'] = {
        'value': loudness_info[2],
        'unit': "LU"
    }

    DBConnecter = TrackEmotion()
    DBConnecter.add(song_id, data)

