import sys

from classification.api_helper import process_data_and_extract_profiles
from database.mongo.audio.track_emotion import TrackEmotion
from utilities.filehandler.handle_path import get_absolute_path


def test_api_helper():
    id = "1337"
    file_path = get_absolute_path("classification/t/test_segmented_audio_" +
                                  "analysis/8376-1-1_Demolition_Man_proud_" +
                                  "music_preview.wav")

    process_data_and_extract_profiles(id, file_path)

    DBConnection = TrackEmotion()
    data = DBConnection.get(id)

    assert data['song_id'] == '1337'
    assert int(data['bpm']['value']) == 139
    assert data['timbre']['value'] == 'dark'
    assert data['relaxed']['value'] == 'not_relaxed'
    assert data['party']['value'] == 'not_party'
    assert data['aggressive']['value'] == 'aggressive'
    assert data['happy']['value'] == 'not_happy'
    assert data['sad']['value'] == 'not_sad'
