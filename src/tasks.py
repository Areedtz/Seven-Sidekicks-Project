from celery import Celery
from bpm.bpm_extractor import get_song_bpm
from utilities.filehandler.handle_audio import get_MonoLoaded_Song
from classification.classifier.profile_data_extractor import get_classifier_data
from similarity.similarity import _load_song, SongSegment
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
        song = get_MonoLoaded_Song(x['source_path'])
        bpm, confidence = get_song_bpm(song)
        x['BPM'] = dict({'BPM': bpm, 'confidence': confidence})
        x['BPM_DONE'] = True
    return x


@app.task
def add_emotions(x):
    if not x['MER_DONE']:
        data = get_classifier_data(
            x['source_path']
        )
        x['timbre'] = dict({
            'timbre': data[0][0],
            'confidence': data[0][1],
        })
        x['MER_DONE'] = True
    return x


@app.task
def add_metering(x):
    if not x['METERING_DONE']:
        # TODO: When metering is done, add here
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
