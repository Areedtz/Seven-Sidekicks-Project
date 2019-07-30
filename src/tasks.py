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

db = AudioDB()


@app.task
def check_done(x):
    existing_entry = db.get_all(x['audio_id'])

    if existing_entry is None:
        x['DB_EXISTS'] = False
    else:
        x['DB_EXISTS'] = True

    if existing_entry is not None and not x['FORCE']:
        if existing_entry['bpm'] is None:
            x['BPM_DONE'] = False
        else:
            x['BPM'] = dict({
                'value': existing_entry['bpm'],
                'confidence': existing_entry['bpm_confidence']
            })

            x['BPM_DONE'] = True

        if existing_entry['timbre'] is None:
            x['MER_DONE'] = False
        else:
            x['timbre'] = dict({
                'value': existing_entry['timbre'],
                'confidence': existing_entry['timbre_confidence']
            })
            x['emotions'] = dict({
                'relaxed': dict({
                    'value': existing_entry['relaxed'],
                    'confidence': existing_entry['relaxed_confidence']
                }),
                'party': dict({
                    'value': existing_entry['party'],
                    'confidence': existing_entry['party_confidence']
                }),
                'aggressive': dict({
                    'value': existing_entry['aggressive'],
                    'confidence': existing_entry['aggressive_confidence']
                }),
                'happy': dict({
                    'value': existing_entry['happy'],
                    'confidence': existing_entry['happy_confidence']
                }),
                'sad': dict({
                    'value': existing_entry['sad'],
                    'confidence': existing_entry['sad_confidence']
                })
            })

            x['MER_DONE'] = True

        if existing_entry['peak'] is None:
            x['METERING_DONE'] = False
        else:
            x['loudness'] = dict({
                'peak': existing_entry['peak'],
                'loudness_integrated': existing_entry['loudness_integrated'],
                'loudness_range': existing_entry['loudness_range']
            })

            x['METERING_DONE'] = True
    else:
        x['BPM_DONE'] = False
        x['MER_DONE'] = False
        x['METERING_DONE'] = False

    return x


@app.task
def add_bpm(x):
    if not x['BPM_DONE']:
        song = get_mono_loaded_song(x['source_path'])
        bpm, confidence = get_song_bpm(song)

        x['BPM'] = dict({'value': bpm, 'confidence': confidence})

        if x['DB_EXISTS']:
            db.update_all(x)
        else:
            db.post_all(x)

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

        if x['DB_EXISTS']:
            db.update_all(x)
        else:
            db.post_all(x)

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

        if x['DB_EXISTS']:
            db.update_all(x)
        else:
            db.post_all(x)

        x['METERING_DONE'] = True

    return x


@app.task
def add_similarity_features(x):
    _load_song(x['audio_id'], x['source_path'], SongSegment(), x['FORCE'])

    return x
