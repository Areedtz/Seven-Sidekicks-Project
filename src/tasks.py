from tempfile import NamedTemporaryFile

from celery import Celery

from bpm.bpm_extractor import get_song_bpm
from utilities.filehandler.audio_loader import get_mono_loaded_song
from classification.classifier.profile_data_extractor import get_classifier_data
from classification.extractor.low_level_data_extractor import make_low_level_data_file
from similarity.similarity import _load_song, SongSegment
from loudness.loudness_extractor import get_song_loudness
from utilities.filehandler.audio_loader import get_audio_loaded_song
from utilities.config_loader import load_config


cfg = load_config()

app = Celery('tasks', backend='redis://@' +
             cfg['redis_host'], broker='pyamqp://guest@' + cfg['rmq_host'] + '//')


@app.task
def check_done(x):
    # TODO: Contact database to see if anything has already been done

    if not x['FORCE']:
        x['BPM_DONE'] = True
        x['MER_DONE'] = True
        x['METERING_DONE'] = True
        x['SIMILARITY_DONE'] = True
    else:
        x['BPM_DONE'] = False
        x['MER_DONE'] = False
        x['METERING_DONE'] = False
        x['SIMILARITY_DONE'] = False
    return x


@app.task
def add_bpm(x):
    if not x['BPM_DONE']:
        song = get_mono_loaded_song(x['source_path'])
        bpm, confidence = get_song_bpm(song)
        x['BPM'] = dict({'BPM': bpm, 'confidence': confidence})
        x['BPM_DONE'] = True
    return x


@app.task
def add_emotions(x):
    if not x['MER_DONE']:
        temp_file = NamedTemporaryFile(delete=True)

        make_low_level_data_file(x['source_path'], temp_file.name)
        timbre, relaxed, party, aggressive, happy, sad = get_classifier_data(
            temp_file.name)

        temp_file.close()

        x['timbre'] = dict({
            'value': timbre[0],
            'confidence': timbre[1]
        })
        x['emotions'] = dict({
            'relaxed': dict({
                'value': relaxed[0],
                'confidence': relaxed[1]
            }),
            'party': dict({
                'value': party[0],
                'confidence': party[1]
            }),
            'aggressive': dict({
                'value': aggressive[0],
                'confidence': aggressive[1]
            }),
            'happy': dict({
                'value': happy[0],
                'confidence': happy[1]
            }),
            'sad': dict({
                'value': sad[0],
                'confidence': sad[1]
            })
        })
        x['MER_DONE'] = True
    return x


@app.task
def add_metering(x):
    if not x['METERING_DONE']:
        song = get_audio_loaded_song("loudness/t/test_loudness_extractor/8376-1-"
                                     + "1_Demolition_Man_proud_music_preview.wav")
        max_loudness, integratedLoudness, loudnessRange = get_song_loudness(
            song)
        x['loudness'] = dict({
            'peak': max_loudness,
            'loudness_integrated': integratedLoudness,
            'loudness_range': loudnessRange,
        })
        x['METERING_DONE'] = True
    return x


@app.task
def add_similarity_features(x):
    if not x['SIMILARITY_DONE']:
        _load_song(x['song_id'], x['source_path'], SongSegment())
        x['SIMILARITY_DONE'] = True
    return x


@app.task
def save_to_db(x):
    print(x)
    # TODO: Save to the database

    return
