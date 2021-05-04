import os
import json

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields
from celery import chain

from tasks import check_done, add_bpm, add_emotions, add_metering, \
    add_similarity_features
from utilities.config_loader import load_config
from utilities.get_song_id import get_song_id


cfg = load_config()

app = Flask(__name__)
api = Api(app)


"""
    Models an analysis request for a piece of music including its location
"""
song_fields = api.model('SongModel', {
    'mediesek_id': fields.String(
        description='',
        required=True),
    'source_path': fields.String(
        description='The path of the song to analyze',
        required=True),
    'force': fields.Boolean(
        description='Should every analysis run'),
    'config': fields.Raw(
        description='Config parameters for the analysis')
})


pipeline = chain(
    check_done.s().set(priority=1),
    add_bpm.s().set(priority=2),
    add_emotions.s().set(priority=3),
    add_metering.s().set(priority=4),
    add_similarity_features.s().set(priority=5),
)


def add_to_pipeline(data, song_path):
    if song_path.endswith(("mp3", "wav")):
        id = get_song_id(song_path)
        force = data['force'] if 'force' in data else False
        config = data['config'] if 'config' in data else {}
        song = dict({
            'mediesek_id': data['mediesek_id'],
            'audio_id': id,
            'source_path': song_path,
            'FORCE': force,
            'config': config,
        })

        pipeline.delay(song)


@api.route('/audio')
class AnalyzeSong(Resource):
    @api.expect(song_fields)
    def post(self) -> str:
        """Analyzes a song and outputs the data to the database
        """

        data = request.get_json()
        song_path = data["source_path"]

        if not (os.path.isfile(song_path)):
            if os.path.isdir(song_path):
                api.abort(
                    400,
                    "The given path {} is a folder and not a file"
                    .format(song_path)
                )
            else:
                api.abort(
                    400,
                    "The given file {} can not be found"
                    .format(song_path)
                )

        add_to_pipeline(data, song_path)

        return {'Response': 'The song has been added to the pipeline ' +
                'and will be available once analyzed'}, 201
