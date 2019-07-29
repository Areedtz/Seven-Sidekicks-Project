import sys
import os
import json
import _thread
from bson.json_util import dumps

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields
from celery import chain

from tasks import check_done, add_bpm, add_emotions, add_metering, add_similarity_features, save_to_db
import classification.api_helper as music_emotion_classifier
from utilities.config_loader import load_config
from utilities.get_song_id import get_song_id


cfg = load_config()

app = Flask(__name__)
api = Api(app)


"""
    Models an analysis request for a piece of music including its location
"""
song_fields = api.model('SongModel', {
    'source_path': fields.String(
        description='The path of the song to analyze',
        required=True),
    'force': fields.Boolean(
        description='Should every analysis run',
        required=False)
})


pipeline = chain(
    check_done.s().set(priority=6),
    add_bpm.s().set(priority=5),
    add_emotions.s().set(priority=4),
    add_metering.s().set(priority=3),
    add_similarity_features.s().set(priority=2),
    save_to_db.s().set(priority=1)
)


def add_to_pipeline(data, song_path):
    if song_path.endswith(("mp3", "wav")):
        id = get_song_id(song_path)
        song = dict({
            'audio_id': id,
            'source_path': song_path,
            'FORCE': data['force'],
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

        if os.path.isfile(song_path):
            add_to_pipeline(data, song_path)
        else:  # Is folder
            for outer_name in os.listdir(song_path):
                outer_filename = os.path.join(song_path, outer_name)

                if os.path.isfile(outer_filename):
                    add_to_pipeline(data, outer_filename)
                else:
                    for inner_name in os.listdir(outer_filename):
                        inner_filename = os.path.join(
                            outer_filename, inner_name)

                        if os.path.isfile(inner_filename):
                            add_to_pipeline(data, inner_filename)

        return {'Response': 'The song has been added to the pipeline and will be available once analyzed'}, 201
