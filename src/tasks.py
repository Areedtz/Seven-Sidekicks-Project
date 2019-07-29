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
from database.sql.audio import AudioDB


cfg = load_config()

app = Celery('tasks', backend='redis://@' +
             cfg['redis_host'], broker='pyamqp://guest@' + cfg['rmq_host'] + '//')


@app.task
def check_done(x):
    db = AudioDB()

    # The following values are set to have support for only
    # partially analyzed audio
    if db.exists(x['audio_id']) and not x['FORCE']:
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

        x['BPM'] = dict({'value': bpm, 'confidence': confidence})
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
        audio_loaded_song = get_audio_loaded_song(x['source_path'])
        max_loudness, integratedLoudness, loudnessRange = get_song_loudness(
            audio_loaded_song)
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
        _load_song(x['audio_id'], x['source_path'], SongSegment(), x['FORCE'])
        x['SIMILARITY_DONE'] = True

    return x


@app.task
def save_to_db(x):
    db = AudioDB()

    if db.exists(x['audio_id']) and not x['FORCE']:
        return
    elif db.exists(x['audio_id']):
        db.update_all(x)
    else:
        db.post_all(x)

    return
