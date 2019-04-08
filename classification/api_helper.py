from tempfile import NamedTemporaryFile

from extractor.low_level_data_extractor import make_low_level_data_file
from classifier.profile_data_extractor import get_classifier_data

def process_data_and_extract_profiles(song_id, song_file):
    # Create temp
    temp_file = NamedTemporaryFile(delete=True)

    #use temp
    make_low_level_data_file(song_file, temp_file.name)

    #use temp
    timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad = get_classifier_data(temp_file.name)

    # Save file in config directory
    return song_id, timbre, mood_relaxed, mood_party, mood_aggressive, mood_happy, mood_sad
    